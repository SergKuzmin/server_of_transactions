# Create your views here.
from django.forms.models import model_to_dict
from rest_framework import serializers

from .models import Accounts
from .models import Transactions


def check_balance(data):
    if data['current_balance'] < 0 and (not data['overdraft']):
        raise serializers.ValidationError("current_balance must be positive if overdraft is False")


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'

    def validate(self, data):
        check_balance(data)
        return data


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'

    def validate(self, data: dict):
        donor_data = model_to_dict(data['donor_uid'])
        donor_data['current_balance'] -= data['amount_of_transaction']
        donor = AccountSerializer(data=donor_data)
        if donor.is_valid():
            donor.update(instance=data['donor_uid'], validated_data=donor_data)
        else:
            raise serializers.ValidationError("current_balance must be positive if overdraft is False")

        recipient_data = model_to_dict(data['recipient_uid'])
        recipient_data['current_balance'] += data['amount_of_transaction']
        AccountSerializer().update(instance=data['recipient_uid'], validated_data=recipient_data)
        return data


def get_pagination_serializer(item):
    class Serializer(serializers.Serializer):
        count = serializers.IntegerField(min_value=0)
        next = serializers.URLField(allow_null=True)
        previous = serializers.URLField(allow_null=True)
        result = serializers.ListField(child=item)
    return Serializer()

