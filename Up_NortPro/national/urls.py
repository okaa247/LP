from django.urls import path
from .views import *

urlpatterns = [
    # path('lga-list/', StateLGAListView.as_view(), name='state_lga_list'),
    path('national-membership/', NationalMembershipView.as_view(), name='national_membership'),
    path('state/<int:state_id>/lgas/', LGAMembershipView.as_view(), name='lga_membership'),
    
]


