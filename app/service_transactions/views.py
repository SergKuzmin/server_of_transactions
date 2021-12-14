# Create your views here.
from django.core.exceptions import ValidationError
from django.http import Http404
from django.http import HttpResponseBadRequest
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Accounts
from .models import Transactions
from .serializers import AccountSerializer
from .serializers import TransactionSerializer
from .serializers import get_pagination_serializer

limit = openapi.Parameter('limit', openapi.IN_QUERY, description="limit of element per page", type=openapi.TYPE_INTEGER)
offset = openapi.Parameter('offset', openapi.IN_QUERY, description="item offset", type=openapi.TYPE_INTEGER)


class AccountView(APIView):
    @swagger_auto_schema(operation_description="GET /account/{id}/",
                         responses={200: AccountSerializer()})
    def get(self, request, pk):
        try:
            account_obj = Accounts.objects.get(pk=pk)
            account = AccountSerializer(instance=account_obj)
            return Response(
                data=account.data,
                status=status.HTTP_200_OK,
            )
        except Accounts.DoesNotExist:
            raise Http404(f"Account with pk {pk} does not exist")
        except ValidationError:
            return HttpResponseBadRequest('pk must be uuid structure')


class AccountsView(APIView, LimitOffsetPagination):
    @swagger_auto_schema(request_body=AccountSerializer,
                         operation_description="Add Account",
                         responses={201: AccountSerializer()})
    def post(self, request):
        account = AccountSerializer(data=request.data)
        if account.is_valid():
            account.save()
            return Response(
                data=account.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(account.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Get Accounts",
                         manual_parameters=[limit, offset],
                         responses={200: get_pagination_serializer(AccountSerializer())})
    def get(self, request, format=None):
        accounts_obj = Accounts.objects.all()
        results = self.paginate_queryset(accounts_obj, request, view=self)
        accounts = AccountSerializer(results, many=True)
        return self.get_paginated_response(accounts.data)


class TransactionsView(APIView, LimitOffsetPagination):
    @swagger_auto_schema(request_body=TransactionSerializer,
                         operation_description="Make transaction",
                         responses={201: TransactionSerializer()})
    def post(self, request):
        transaction = TransactionSerializer(data=request.data)
        if transaction.is_valid():
            transaction.save()
            return Response(
                data=transaction.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(transaction.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Get Transactions",
                         manual_parameters=[limit, offset],
                         responses={200: get_pagination_serializer(TransactionSerializer())})
    def get(self, request, format=None):
        accounts_obj = Transactions.objects.all()
        results = self.paginate_queryset(accounts_obj, request, view=self)
        transactions = TransactionSerializer(results, many=True)
        return self.get_paginated_response(transactions.data)
