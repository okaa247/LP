from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('register/', Register.as_view(), name='register'),
     path('signup/', Signup.as_view(), name='signup'),
    path('verify/', Verify.as_view(), name='verify'),
    path('reverify/', ReverifyOtp.as_view(), name='reverify'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout, name='logout'),
    path('forgot/', ForgotPassword.as_view(), name='forgot-password'),
    path('reset/<str:uidb64>/<str:token>/', PasswordReset.as_view(), name='reset-password'), 


    # path('wards/get_user_info/', GetUserInfo.as_view(), name='get_user_info'),

    

]



