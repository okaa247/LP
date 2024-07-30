from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from Up_NortPro.settings import EMAIL_HOST_USER
from django.contrib import messages, auth
from .models import *
from django.utils import timezone
from datetime import timedelta

User = get_user_model()




class Signup(View):
    def get(self, request):
        return render(request, 'user/signup.html')

    def post(self, request):
        email = request.POST['email']
        username = request.POST['username']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exist')

        user = User.objects.create_user(email=email, username=username)

        generate_verification = random.randint(100000, 999999)
        user.otp = generate_verification
        user.otp_created_at = timezone.now()  # Store the timestamp when OTP was generated
        user.save()

        subject = "OTP Verification"
        body = f"Your verification code is: {generate_verification}"
        from_email = EMAIL_HOST_USER
        to_email = email
        send_now = send_mail(subject, body, from_email, [to_email])
        
        if send_now:
            messages.success(request, 'Successfully sent OTP. Verify your email here.')
            return redirect('verify')
        messages.error(request, 'Sign up')
        return render(request, 'user/signup.html')





class Verify(View):
    def get(self, request):
        return render(request, 'user/verify.html')
    
    def post(self, request):
        entered_otp = request.POST.get('otp')
        if not entered_otp:
            messages.error(request, 'Please enter the OTP.')
            return redirect('reverify')
        
        try:
            user = User.objects.get(otp=entered_otp, is_email_verified=False)
            if user.otp_created_at >= timezone.now() - timedelta(minutes=5):
                user.is_email_verified = True
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Success, You are logged in. Create your account here.')
                return redirect('register')
            else:
                messages.error(request, 'Ooops! OTP expired.')
                return redirect('reverify')
        except User.DoesNotExist:
            messages.error(request, 'Invalid OTP or user not found. Please sign up.')
            return redirect('signup')




class ReverifyOtp(View):
    def get(self, request):
        return render(request, 'user/reverify-otp.html')

    def post(self, request):
        
        entered_email = request.POST.get('email')

        try:
            user = User.objects.get(email=entered_email, is_email_verified=False)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email address.')
            return redirect('reverify')

        
        new_otp = random.randint(100000, 999999)
        user.otp = new_otp
        user.otp_created_at = timezone.now()
        user.save()

        subject = "New OTP Verification"
        body = f"Your new verification code is: {new_otp}"
        from_email = EMAIL_HOST_USER  # Update with your email host user
        to_email = entered_email
        send_now = send_mail(subject, body, from_email, [to_email])

        if send_now:
            messages.success(request, 'New OTP sent successfully.')
            return redirect('verify')  # Redirect to the OTP verification page
        else:
            messages.error(request, 'Failed to send new OTP.')
            return redirect('reverify')




class Register(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'User not authenticated')
            return redirect('reverify')
        return render(request, 'user/page-register2.html')
    
    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'User not authenticated')
            return redirect('reverify')
         
        # Retrieve the logged-in user 
        user = request.user
        # Retrieve the username entered in the form
        entered_username = request.POST.get('username')
        entered_email = request.POST.get('email')

        fullname = request.POST.get('fullname')
        phone_number = request.POST.get('phone_number')
        state = request.POST.get('state')
        lga = request.POST.get('lga')
        ward = request.POST.get('ward')
        pollingunit = request.POST.get('pollingunit')
        userimage = request.FILES.get('userimage')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if entered_email != request.user.email:
            messages.error(request, 'email_mismatch')
            return redirect('register')
        
        if entered_username != request.user.username:
            messages.error(request, 'username_mismatch')
            return redirect('register')

        
        if password and confirm_password:
            if password == confirm_password:
                user.set_password(password)
                user.save(update_fields=['password'])
            else:
                messages.error(request, 'Passwords did not match')
                return redirect('register')
        else:
            messages.warning(request, 'No password provided')
            return redirect('register')      
        user = UserRegistration.objects.create(
            fullname= fullname,
            phone_number=phone_number,
            state=state,
            lga=lga,
            ward=ward,
            pollingunit=pollingunit,
            userimage=userimage
        )
        user.save()
        return redirect('login')
      





class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page or home
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})


class Home(View):
    def get(self, request):
  
        return render(request, 'index.html',)
    




# class RegistrationView(View):
#     def get(self, request):
#         return render(request, 'register.html')

#     def post(self, request):
#         email = request.POST['email']
#         username = request.POST['username']
#         fullname = request.POST['fullname']
#         password = request.POST['password']
#         phone_number = request.POST['phone_number']
    
#         if User.objects.filter(email=email).exists():
#             messages.error(request, 'Email already exists')
#             return redirect('register')
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Username alradey exists')
#             return redirect('register')

#         user = User.objects.create_user(
#             email=email,
#             username=username,
#             fullname=fullname,
#             phone_number=phone_number,
#             password=password
#         )
#         user.save()
#         return redirect('login')

