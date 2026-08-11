from django.urls import path

from .views import MeView, SyncUserView, UserStatusView

urlpatterns = [
    path('sync/', SyncUserView.as_view(), name='user-sync'),
    path('me/', MeView.as_view(), name='me' ),
    path('<uuid:user_id>/status/', UserStatusView.as_view(), name='user-status'),
]