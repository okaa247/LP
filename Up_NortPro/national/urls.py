from django.urls import path
from .views import *

urlpatterns = [
    # path('lga-list/', StateLGAListView.as_view(), name='state_lga_list'),
    path('national-membership/', NationalMembershipView.as_view(), name='national_membership'),
    path('state/<int:state_id>/lgas/', LGAMembershipView.as_view(), name='lga_membership'),
    path('lga/<int:lga_id>/wards/', WardMembershipView.as_view(), name='ward_membership'),
    path('ward/<int:ward_id>/pollingunits/', PollingUnitView.as_view(), name='pollingunit_list'),
    path('pollingunit/<str:pollingunit_name>/users/', PollingUnitUsersView.as_view(), name='pollingunit_users'),
    path('state-memberships-update/', StateMembershipUpdateView.as_view(), name='state_membership_update'),
    path('executives/', NationalUserListView.as_view(), name='executive_list'),


]


