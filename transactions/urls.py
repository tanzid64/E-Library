from django.urls import path
from .views import DepositView, PurchaseView, BorrowBookView, ReturnBookView
urlpatterns = [
    path("deposit/", DepositView.as_view(), name="deposit_money"),
    path("purchase/<int:id>", PurchaseView.as_view(), name="buy_now"),
    path("borrow/<int:id>", BorrowBookView.as_view(), name="borrow_book"),
    path("return/<int:id>", ReturnBookView.as_view(), name="return_book"),
]