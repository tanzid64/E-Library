from django import forms
from .models import Transaction
# class TransactionForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = [
#             'amount',
#             'transaction_type'
#         ]

#     def __init__(self, *args, **kwargs):
#         self.account = kwargs.pop('account') # account value ke pop kore anlam
#         super().__init__(*args, **kwargs)
#         self.fields['transaction_type'].disabled = True # ei field disable thakbe
#         self.fields['transaction_type'].widget = forms.HiddenInput() # user er theke hide kora thakbe

#     def save(self, commit=True):
#         self.instance.profile = self.profile
#         return super().save()


# class DepositForm(TransactionForm):
#     def clean_amount(self): # amount field ke filter korbo
#         min_deposit_amount = 100
#         amount = self.cleaned_data.get('amount') # user er fill up kora form theke amra amount field er value ke niye aslam, 50
#         if amount < min_deposit_amount:
#             raise forms.ValidationError(
#                 f'You need to deposit at least {min_deposit_amount} $'
#             )

#         return amount
class DepositForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        fields = ['amount']
        def clean_amount(self):
            min_deposit_amount = 100
            amount = self.cleaned_data.get('amount')
            if amount < min_deposit_amount:
                raise forms.ValidationError(
                    f'You need to deposit at least {min_deposit_amount} $'
                )

            return amount