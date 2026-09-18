from django.urls import path

from .views import (
    MeView,
    SyncUserView,
    UserBatchLookupView,
    UserByEmailView,
    UserDetailView,
    UserInternalStatusView,
    UserListView,
    UserLookupView,
    UserRoleView,
    UserStatusView,
)

urlpatterns = [
    path('sync/', SyncUserView.as_view(), name='user-sync'),
    path('me/', MeView.as_view(), name='me' ),
    path('internal/<uuid:user_id>/status/', UserInternalStatusView.as_view(), name='user-internal-status'),
    path('<uuid:user_id>/status/', UserStatusView.as_view(), name='user-status'),
    path('<uuid:user_id>/role/', UserRoleView.as_view(), name='user-role'),
    path('search/', UserByEmailView.as_view(), name='user-by-email'),
    path('batch/', UserBatchLookupView.as_view(), name='user-batch-lookup'),
    path('', UserListView.as_view(), name='user-list'),
    path('<uuid:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('lookup/', UserLookupView.as_view(), name='user-lookup'),
]