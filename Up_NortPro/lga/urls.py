from django.urls import path
from .views import *

urlpatterns = [
      path('lga-coordinator/', LGACoordinatorView.as_view(), name='lga_coordinator_view'),
      path('lga-coordinator/wards/', LGACoordinatorWardListView.as_view(), name='lga_coordinator_ward_list'),
      path('ward-status-update/', LGAUserSearchView.as_view(), name='ward_status_update'),

]
