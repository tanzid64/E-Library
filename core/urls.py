from django.urls import path
from .views import HomeView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', HomeView.as_view(), name='category_wise_post'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)