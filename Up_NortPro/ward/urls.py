from django.urls import path
from .views import *

urlpatterns = [
    path('ward-pending-status-list/', WardPendingStatusView.as_view(), name='pending_status'),
    # path('filter-users/', filter_users_by_ward_and_pollingunit, name='filter_users'),
]