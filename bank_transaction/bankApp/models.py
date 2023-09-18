from django.db import models

# Create your models here.
class Accounts(models.Model):
    account_id = models.IntegerField(primary_key=True,unique=True)
    name = models.CharField(max_length=50)

class Transactions(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField()
    description = models.CharField(max_length=255)
    debit_credit_status = models.CharField(max_length=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
