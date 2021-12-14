import uuid

from django.db import models


class Accounts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, default="default_name")
    overdraft = models.BooleanField(default=False)
    current_balance = models.BigIntegerField(default=0)


class Transactions(models.Model):
    donor_uid = models.ForeignKey(Accounts, on_delete=models.PROTECT, related_name='donor_uid')
    recipient_uid = models.ForeignKey(Accounts, on_delete=models.PROTECT, related_name='recipient_uid')
    amount_of_transaction = models.PositiveBigIntegerField()
