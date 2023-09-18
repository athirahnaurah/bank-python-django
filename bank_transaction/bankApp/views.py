from django.shortcuts import render, redirect
from rest_framework import generics
from .forms import AccountForm, TransactionForm, ReportForm
from django.contrib.auth.forms import UserCreationForm
from .models import Accounts, Transactions
from .serializers import AccountsSerializer, TransactionsSerializer
from django.db import IntegrityError

# Create your views here.
def add_account(request):
    account = AccountsSerializer(data=request.data)
 
    # validating for already existing data
    if Accounts.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
 
    if account.is_valid():
        account.save()
        return Response(account.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

class AccountCreateView(generics.CreateAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer

class TransactionsCreateView(generics.CreateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer

def account_list(request):
    accounts = Accounts.objects.all()
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
             try:
                form.save()
                return redirect("nasabah")
             except IntegrityError as e:
                print(f"IntegrityError: {e}")
                form.add_error('account_id', 'ID sudah ada dalam database.')
        else:
            print(form.errors)
    else:
        form = AccountForm()
        context = {
            'form': AccountForm(), 
            'accounts': accounts
        }
        return render(request, "account.html", context=context)

def transaction(request):
    transactions = Transactions.objects.all()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("transaksi")
        else:
            print(form.errors)
    else:
        form = TransactionForm()
    context = {
            'form': TransactionForm(),
            'transactions': transactions
        }
    return render(request, "transactions.html",context=context)

def point(request):
    accounts = Accounts.objects.all()
    data_point = []

    for account in accounts:
        transactions_pulsa = Transactions.objects.filter(account=account,description='Beli Pulsa')
        transactions_listrik = Transactions.objects.filter(account=account, description='Bayar Listrik')
        total_point = 0

        for transaction in transactions_listrik:
            nominal = transaction.amount
            if (transaction.amount - 50_000 != 0 or transaction.amount <= 50_000 ) :
                total_point += 0
                nominal -= 50_000

            if (transaction.amount - 50_000 != 0  or transaction.amount <= 100_000) :
                if (nominal >= 50_000):
                    total_point += 50_000 // 2000
                    nominal -= 50_000
                else:
                    total_point += (nominal) // 2000
            if transaction.amount > 100_000:
                total_point += (nominal / 2000)*2

        for transaction in transactions_pulsa:
            nominal = transaction.amount
            if (transaction.amount - 10_000 != 0 or transaction.amount <= 10_000 ) :
                total_point += 0
                nominal -= 10_000
            if (transaction.amount - 10_000 != 0  or transaction.amount <= 30_000):
                if (nominal >= 20_000):
                    total_point += 20_000 // 1000
                    nominal -= 20_000
                else:
                    total_point += (nominal) // 1000
                # total_point += (transaction.amount - 10000) // 1000
            if transaction.amount > 30_000:
                total_point += (nominal // 1000)*2
        
        data_point.append({
                'account_id': account.account_id,
                'name': account.name,
                'point': total_point,
            })
        # print("data", data_point)
    context = {'points': data_point}
    return render(request,"point.html", context=context)

def report(request):
    data_report = []
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            account_id = form.cleaned_data['account']
            start_date = form.cleaned_data['StartDate']
            end_date = form.cleaned_data['EndDate']
            try:
                transactions = Transactions.objects.filter(
                    account_id=account_id,
                    transaction_date__range=(start_date, end_date)
                )
                if transactions.exists():

                    print("transaksi",transactions)
                    balance = transactions.first().amount
                    print("balance:",balance)

                    for index, transaction in enumerate(transactions):
                        if index == 0:
                            data_report.append({
                                'date': transaction.transaction_date,
                                'description': transaction.description,
                                'status': transaction.debit_credit_status,
                                'amount':transaction.amount,
                                'balance': balance
                            })
                        else:
                            if transaction.debit_credit_status == 'D':
                                balance -= transaction.amount
                            elif transaction.debit_credit_status == 'C':
                                balance += transaction.amount
                            data_report.append({
                                'date': transaction.transaction_date,
                                'description': transaction.description,
                                'status': transaction.debit_credit_status,
                                'amount':transaction.amount,
                                'balance': balance
                            })
                else:
                    print("Tidak ditemukan transaksi")
            except Transactions.DoesNotExist:
                print("ID tidak ditemukan")
            
            print(data_report)
            context = {
                'form': form,
                'transactions': data_report,
            }
            return render(request, "report.html", context=context)
    else:
        form = ReportForm()
        print("else")
    
    context = {
        'form': form,
    }
    
    return render(request, "report.html", context=context)



