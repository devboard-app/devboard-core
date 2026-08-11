from django.urls import path

from .views import MeView, SyncUserView

urlpatterns = [
    path('sync/', SyncUserView.as_view(), name='user-sync'),
    path('me/', MeView.as_view(), name='me' ),
]