from django.db import transaction
from django.db.models import F

from rest_framework import exceptions, serializers

from . import models
from apio.api_exceptions import *
from dehaat.settings import ACCEPTED, CONFIRMED, DELIVERED, CANCELLED


class OrderLineSerializer(serializers.ModelSerializer):
    """
    Serializer to output basic info values and related product.
    """

    class Meta:
        model = models.OrderLine
        fields = ['product', 'units', 'confirmed_price']
        read_only_fields = ['user', 'confirmed_price']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer to output connected orderlines, read, create and update orders, and product stock.
    """

    # An orderline defines the product to buy. An order cannot be accepted with nothing to buy. So, orderlines
    # are mandatory in this serializer for create.
    orderlines = OrderLineSerializer(many=True)

    class Meta:
        model = models.Order
        fields = ['id', 'orderlines', 'status']
        read_only_fields = ['id', 'status']

    def validate(self, attrs):
        """
        This validates the post request as a whole and not just a field. During read, the validator
        practically skips. During post, each orderline unit is validated. If an orderline has more units
        than available product units, the order is not accepted.
        """
        exception_body = []
        for orderline in attrs.get('orderlines', []):
            product = orderline['product']

            # If orderline has less units than available, all good.
            if orderline['units'] <= product.units:
                continue

            # else error is accumulated
            if product.units > 0:
                exception_body.append({product.name: 'Only {0} units available.'.format(str(product.units))})
            else:
                exception_body.append({product.name: 'Out of stock'})

        # If any orderline has problem, reject order.
        if exception_body:
            raise exceptions.PermissionDenied({'errors': exception_body})

        return attrs

    def create(self, validated_data):
        """
        Runs after validation to create an order and associated orderlines. Prices are not locked as prices can
        always change despite being accepted. Until the order is confirmed by our agent, the prices are NOT locked in.
        If an 'accepted' order is shown on UI, the client should show prices from the associated product of an orderline.
        """
        orderlines = validated_data.pop('orderlines', None)
        if not (orderlines and len(orderlines)):
            raise EmptyOrderException

        # Create order and associated orderlines
        order = models.Order.objects.create(**validated_data)
        for orderline in orderlines:
            order.orderlines.create(**orderline)

        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Runs a custom validation during 'confirmation' of an order. It validates two things-
    1. The required number of units for each orderline must be in stock.
    2. The customer should have enough balance to actually buy.

    After validation, Orderline prices are locked in from the current standing price of the locked and orderlines
    are locked and no longer modified. Product units count is decremented by the number of orderline unit.
    """
    class Meta:
        model = models.Order
        fields = ['status']

    def _validate_units_and_balance_in_orderlines(self, orderlines, customer):
        exception_body = []
        req_bal = 0

        for orderline in orderlines:
            product = orderline.product

            # Step 1: The orderline units required should be less than/equal to product units in stock.
            if orderline.units <= product.units:

                # Accumulate the current standing price to verify for balance
                req_bal += orderline.units * product.price
                continue

            # If reaches here, it means we are in unit count error.
            if product.units > 0:
                exception_body.append({product.name: 'Only {0} units available.'.format(str(product.units))})
            else:
                exception_body.append({product.name: 'Out of stock'})

        if exception_body:
            raise exceptions.PermissionDenied({'errors': exception_body})

        # Step 2: If the customer has paid cash and has enough balance, then the order goes through.
        try:
            last_ledger = customer.ledgers.latest('transaction_date')
            if last_ledger.post_balance < req_bal:
                raise Exception
        except Exception as e:
            raise NoLedgerBalance

    def update(self, instance, validated_data):
        """
        Actual updation of an order to confirmed/cancellation/delivery status happens here. There are only
        two valid transitions acceptable-
        1. From accepted to confirmed.
        2. From confirmed to cancelled/delivered.
        """

        # If an order is cancelled or delivered, it cannot be modified.
        if instance.status == CANCELLED or instance.status == DELIVERED:
            raise exceptions.PermissionDenied('This order cannot be modified.')

        # If an order is already confirmed but UI/agent sends another confirmation request by mistake,
        # we deny it as each confirmation is a big operation that includes generating invoices/ledger entries.
        if instance.status == validated_data['status'] == CONFIRMED:
            raise exceptions.PermissionDenied('This order is already confirmed.')

        if instance.status == ACCEPTED and validated_data['status'] == CONFIRMED:
            # 1. Transition: accepted -> confirmed
            instance.status = validated_data.get('status')
        elif instance.status == CONFIRMED and validated_data['status'] in [CANCELLED, DELIVERED]:
            # 2. Transition: confirmed -> cancelled/delivered and return
            instance.status = validated_data.get('status')
            instance.save(update_fields=['status'])
            return instance
        else:
            # In case of any invalid transition, reject it.
            raise exceptions.PermissionDenied('There seems to be some discrepancy. Please contact your agent.')

        # Get exclusive lock on all relevant data rows
        orderlines = instance.orderlines.select_for_update().select_related('product').all()

        # Do order and product update in a single transaction
        with transaction.atomic():

            # Validate that order can be approved.
            self._validate_units_and_balance_in_orderlines(orderlines, instance.user)

            for orderline in orderlines:

                # Decrement product stock count by orderline(buying) requirement
                product = orderline.product
                product.units = F('units') - orderline.units
                product.save(update_fields=['units'])

                # Lock current standing price into the orderline, calculate sub total and lock it.
                product_price = product.price
                orderline.confirmed_price = product_price
                orderline.locked = CONFIRMED
                orderline.sub_total = product_price * F('units')
                orderline.save(update_fields=['confirmed_price', 'locked', 'sub_total'])

        # Mark order as confirmed.
        instance.save(update_fields=['status'])
        return instance
