import datetime
from django.contrib.auth.models import User

from apio.api_exceptions import *
from .models import Ledger


class LedgerList:
    """
    This provides all ledgers belonging to a user. It also has query string params
    for filtering on from and to dates. You must provide both fields to properly query.
    Specifying just one field not currently supported.
    """
    def query_set_all(self):
        user = User.objects.filter(id=self.kwargs.get('id')).first()
        start = self.request.GET.get('from')
        stop = self.request.GET.get('to')
        if start or stop:
            try:
                start = datetime.datetime.strptime(start, "%d-%m-%Y").date()
                stop = datetime.datetime.strptime(stop, "%d-%m-%Y").date()
            except (TypeError, ValueError) as e:
                # handling for invalid format or missing field
                raise InvalidDateException
            except Exception as e:
                # handling for any rare error that may come in any special circumstance
                raise NotFoundException
            # if both dates specified and valid, return the filtered result
            return Ledger.objects.filter(customer=user, transaction_date__range=[start, stop])
        # if no query string provided, return all
        return Ledger.objects.filter(customer=user)
