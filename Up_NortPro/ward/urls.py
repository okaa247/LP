from django.urls import path
from .views import *

urlpatterns = [
    path('ward-pending-status-list/', WardPendingStatusView.as_view(), name='pending_status'),
    path('ward-members/', ward_members_view, name='ward_members'),
    # path('filter-users/', filter_users_by_ward_and_pollingunit, name='filter_users'),
]