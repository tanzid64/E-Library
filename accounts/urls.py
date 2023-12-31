from django.urls import path
from .views import UserLoginView, UserLogoutView, UserRegistrationView, UserProfileView, UserProfileUpdateView, UserPasswordUpdateView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/edit', UserProfileUpdateView.as_view(), name='edit_profile'),
    path('profile/edit_password', UserPasswordUpdateView.as_view(), name='edit_pass'),
    path('register/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    # path('profile/history/', TransactionHistoryView.as_view(), name='transaction_history'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)