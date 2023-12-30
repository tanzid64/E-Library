from django.urls import path
from .views import AddBookView, BookDetailsView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('add/', AddBookView.as_view(), name='add_book'),
    path('details/<int:pk>', BookDetailsView.as_view(), name='details_book'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
