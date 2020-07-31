#########################################################################
# All APIExceptions should be customized for clear messaging.
# Also, not all Exceptions have been added. This is only a representative.
#########################################################################

from rest_framework import status
from rest_framework.exceptions import APIException

from dehaat.settings import ALL_GROUP_NAMES


class InvalidDateException(APIException):
    default_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Provide both valid dates in format: DD-MM-YYYY'


class NotFoundException(APIException):
    default_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not Found'


class NoLedgerBalance(APIException):
    default_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = 'Customer does not have enough balance.'


class EmptyOrderException(APIException):
    default_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Your order is empty. No empty orders allowed.'


class InvalidRoleException(APIException):
    default_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid role. Allowed roles are {0}, {1} and {2}. '.format(*ALL_GROUP_NAMES)
