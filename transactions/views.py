from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DepositForm
from django.views.generic import CreateView
from django.views import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from .constants import DEPOSIT, PURCHASE, BORROW_BOOK, RETURN_BOOK
from book.models import Book
from .models import Transaction
from django.urls import reverse_lazy
# Create your views here.
def send_transaction_email(user, amount, subject, template, **kwargs):
        if kwargs['book_name']:
            book_name = kwargs['book_name']
        else:
            book_name = None
        message = render_to_string(template,{
            'user': user,
            'amount': amount,
            'book_name': book_name
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, 'text/html')
        send_email.send()

class DepositView(LoginRequiredMixin, CreateView):
    template_name = 'deposit.html'
    form_class = DepositForm
    success_url = reverse_lazy('profile')
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
        transaction_obj.transaction_type = DEPOSIT
        transaction_obj.balance_after_transaction = profile.balance
        transaction_obj.save()
        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        send_transaction_email(self.request.user, amount, 'Deposit Message', 'deposit_mail.html')
        return super().form_valid(form)

class PurchaseView(LoginRequiredMixin, View):
    def get(self, request, id):
        book = Book.objects.get(pk=id)
        buyer = self.request.user.profile
        if book.quantity > 0:
            if buyer.balance >= book.price:
                buyer.balance -= book.price
                buyer.save()
                messages.success(self.request, 'Purchase Successfull')
                book.quantity -=1
                book.save()
                transaction = Transaction(
                    profile = buyer,
                    amount = book.price,
                    balance_after_transaction = buyer.balance,
                    transaction_type = PURCHASE,
                    book = book
                )
                transaction.save()
                send_transaction_email(self.request.user, book.price, 'Purchase Confirmation Email', 'buy_book_mail.html', book_name = book.name)
                return redirect('profile')
            else:
                messages.error(self.request, "Your current balance is lower than book price. Deposit Money.")
                return redirect('deposit_money')
        else:
            messages.error(self.request, "Sorry, this book out of stock.")
            return redirect('details_book', pk=id)

class BorrowBookView(LoginRequiredMixin, View):
    def get(self, request, id):
        book = Book.objects.get(pk=id)
        buyer = self.request.user.profile

        # Check if the user has already borrowed the same book and it's not returned
        existing_borrow_book = Transaction.objects.filter(profile=buyer, book=book, is_returned=False).first()

        if existing_borrow_book:
            messages.error(self.request, 'You have already borrowed this book. You cannot borrow the same book twice at the same time.')
            return redirect('details_book', pk=id)
        else:
            if book.quantity > 0:
                if buyer.balance >= book.price:
                    buyer.balance -= book.price
                    buyer.save()

                    book.quantity -= 1
                    book.save()

                    transaction = Transaction(
                        profile=buyer,
                        amount=book.price,
                        balance_after_transaction=buyer.balance,
                        transaction_type=BORROW_BOOK,
                        book=book
                    )
                    transaction.save()

                    messages.success(self.request, f'You have successfully borrowed {book.name} book.')
                    send_transaction_email(self.request.user, book.price, 'Borrow Book Confirmation', 'borrow_book_mail.html', book_name = book.name)
                    return redirect('profile')
                else:
                    messages.error(self.request, "Your current balance is lower than the book price. Deposit Money.")
                    return redirect('deposit_money')
            else:
                messages.error(self.request, "Sorry, this book is out of stock.")
                return redirect('details_book', pk=id)

class ReturnBookView(LoginRequiredMixin, View):
    def get(self, request, id):
        book = Book.objects.get(pk=id)
        buyer = self.request.user.profile
        borrowed_book = Transaction.objects.get(profile=buyer, book=book)
        if not borrowed_book.is_returned:
            borrowed_book.is_returned = True
            borrowed_book.save()
            buyer.balance += book.price
            buyer.save()
            messages.success(self.request, 'Return Successfull')
            book.quantity +=1
            book.save()
            transaction = Transaction(
                profile = buyer,
                amount = book.price,
                balance_after_transaction = buyer.balance,
                transaction_type = RETURN_BOOK,
                book = book
            )
            transaction.save()
            return redirect('profile')
        else:
            messages.error(self.request, 'Already Returned')
            return redirect('profile')







