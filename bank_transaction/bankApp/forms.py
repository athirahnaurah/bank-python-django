from django import forms
from .models import Accounts, Transactions

class AccountForm(forms.ModelForm): 
    class Meta:
        model = Accounts
        fields = ['account_id','name']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['account', 'transaction_date', 'description', 'debit_credit_status', 'amount']
    
    transaction_date = forms.DateTimeField(
        label='Tanggal dan Waktu',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control datepicker'}),
    )

    description_choices = [
        ('Setor Tunai', 'Setor Tunai'),
        ('Tarik Tunai', 'Tarik Tunai'),
        ('Bayar Listrik', 'Bayar Listrik'),
        ('Beli Pulsa', 'Beli Pulsa'),
    ]

    description = forms.ChoiceField(
        choices=description_choices,
        label='Deskripsi',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    # Menentukan pilihan opsi untuk Status
    status_choices = [
        ('D', 'Debit'),
        ('C', 'Credit'),
    ]

    debit_credit_status = forms.ChoiceField(
        choices=status_choices,
        label='Status',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )


class ReportForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['account']
    # AccountId = forms.IntegerField(
    #     label='Nomor Nasabah',
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    # )
    StartDate = forms.DateTimeField(
        label='Tanggal Awal Cetak',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
    )
    EndDate = forms.DateTimeField(
        label='Tanggal Akhir Cetak',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
    )

