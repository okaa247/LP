from django.urls import path
from .views import *

urlpatterns = [
    path('lga-list/', StateLGAListView.as_view(), name='state_lga_list'),
    # path('lga-user-search/', StateLGAUserSearchView.as_view(), name='state_lga_user_search'),

    path('lga-role-update/', UserSearchAndRoleUpdateView.as_view(), name='user_search_and_role_update'),
    # path('ward-pending-status-list/', WardPendingStatusView.as_view(), name='pending_status'),
]


