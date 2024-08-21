from django.urls import path
from .views import *

urlpatterns = [
    path('ward-pending-status-list/', WardPendingStatusView.as_view(), name='pending_status'),
    path('ward-members/', ward_members_view, name='ward_members'),
    path('agents/', PollingUnitAgentListView.as_view(), name='polling_unit_agent_list'),
    path('approved-agents/', ApprovedPollingUnitAgentsView.as_view(), name='approved_polling_unit_agents'),


    # path('filter-users/', filter_users_by_ward_and_pollingunit, name='filter_users'),
]