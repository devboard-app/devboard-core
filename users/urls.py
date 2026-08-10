from django.urls import path

from .views import SyncUserView

urlpatterns = [
    path('sync/', SyncUserView.as_view(), name='user-sync'),
    
]