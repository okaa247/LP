from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('register/', Register.as_view(), name='register'),
     path('signup/', Signup.as_view(), name='signup'),
    path('verifier/', Verify.as_view(), name='verifyit'),
    path('reverify/', ReverifyOtp.as_view(), name='reverifyit'),
    # path('login/', LoginView.as_view(), name='login'),
]
