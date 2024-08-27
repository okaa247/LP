from django.urls import path
from .views import *

urlpatterns = [
    path('lga-list/', StateLGAListView.as_view(), name='state_lga_list'),
    path('lga-status-update/', StateUserSearchView.as_view(), name='lga_status_update'),

    path('lga-role-update/', UserSearchAndRoleUpdateView.as_view(), name='user_search_and_role_update'),
]


