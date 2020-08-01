from django.contrib.auth.models import User, Group

from rest_framework import exceptions, serializers

from apio.api_exceptions import InvalidRoleException
from dehaat.settings import CUSTOMER_GROUP, ALL_GROUP_NAMES


class UserAccountSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(slug_field='name', queryset=Group.objects)
    password = serializers.CharField(default='')

    class Meta:
        model = User
        fields = ['username', 'groups', 'password']

    def validated_password(self, value):
        if value not in ALL_GROUP_NAMES:
            raise InvalidRoleException

    def validate(self, attrs):
        group = attrs.get('groups')

        # To create a new user that is admin/agent, password is mandatory.
        if group.name != CUSTOMER_GROUP and not attrs.get('password'):
            raise exceptions.ValidationError('Assign Password')

        return attrs
