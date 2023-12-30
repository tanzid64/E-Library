from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DepositForm
from django.views.generic import CreateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from .constants import DEPOSIT, PURCHASE, BORROW_BOOK, RETURN_BOOK
# Create your views here.
def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template,{
            'user': user,
            'amount': amount
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, 'text/html')
        send_email.send()

class DepositView(LoginRequiredMixin, CreateView):
    template_name = 'deposit.html'
    form_class = DepositForm
    
    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        profile = self.request.user.profile
        profile.balance += amount
        profile.save(
            update_fields=[
                'balance'
            ]
        )
        transaction_obj = form.save(commit=False)
        transaction_obj.profile = profile
        transaction_obj.save()
        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        send_transaction_email(self.request.user, amount, 'Deposit Message', 'deposit_mail.html')
        return super().form_valid(form)
