from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
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
from django.db.utils import IntegrityError
from django.http import JsonResponse


from django.db import transaction, IntegrityError
from .models import Ward, UserRegistration as User

User = get_user_model()





class Signup(View):
    def get(self, request):
        return render(request, 'user/signup.html')

    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        
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
        return render(request, 'user/emailverify.html')
    
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
        return render(request, 'user/register.html')
    
    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'User not authenticated')
            return redirect('reverify')
         
        # Retrieve the logged-in user 
        user = request.user
        # Retrieve the username entered in the form
        # entered_username = request.POST.get('username')
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
        
        # if entered_username != request.user.username:
        #     messages.error(request, 'username_mismatch')
        #     return redirect('register')

        
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

        user.fullname = fullname
        user.phone_number = phone_number
        user.state = state
        user.lga = lga
        user.ward = ward
        user.pollingunit = pollingunit
        user.userimage = userimage
        user.save()

        messages.success(request, 'Registration successfully')
        return redirect('login')

      




class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page or home
        else:
            return render(request, 'user/login.html', {'error': 'Invalid credentials'})



class Home(View):
    def get(self, request):
  
        return render(request, 'index.html',)
    



class State(View):
    def get(self, request):
  
        return render(request, 'state.html',)
















class GetUserInfo(View):
    def get(self, request):
        membership_id = request.GET.get('membership_id')
        try:
            user = User.objects.get(membership_id=membership_id)
            data = {
                'fullname': user.fullname,
            }
        except User.DoesNotExist:
            data = {
                'fullname': None,
            }
        return JsonResponse(data)

class CreateWard(View):
    def get(self, request):
        return render(request, 'ward/create_ward.html')

    @transaction.atomic
    def post(self, request):
        role = request.POST.get('role')
        membership_id = request.POST.get('membership_id')

        if not membership_id:
            messages.error(request, 'Name and Membership ID are required.')
            return render(request, 'ward/create_ward.html')

        try:
            user = User.objects.get(membership_id=membership_id)

            # Debugging: Print user information and input data
            print(f"User: {user}")
            print(f"Role: {role}, Membership ID: {membership_id}")

            # Check if the user exists before creating the ward
            if not user:
                messages.error(request, 'User with this Membership ID does not exist.')
                return render(request, 'ward/create_ward.html')

            # Ensure data integrity with atomic transaction
            with transaction.atomic():
                ward = Ward.objects.create(
                    role=role,
                    user=user,
                    fullname=user.fullname,
                    membership_id=membership_id,
                    created_at=timezone.now(),
                    updated_at=timezone.now()
                )
                ward.save()

            messages.success(request, 'Ward created successfully.')
            return redirect('ward_list')
        except User.DoesNotExist:
            messages.error(request, 'User with this Membership ID does not exist.')
            return render(request, 'ward/create_ward.html')
        except IntegrityError as e:
            messages.error(request, f'Integrity Error: {e}')
            return render(request, 'ward/create_ward.html')
        except Exception as e:
            messages.error(request, f'Unexpected Error: {e}')
            return render(request, 'ward/create_ward.html')







class CreateWardMembershipView(View):
    def get(self, request):
        return render(request, 'create_ward_membership.html')

    def post(self, request):
        membership_id = request.POST.get('membership_id')
        role = request.POST.get('role')
        ward_name = request.POST.get('ward_name')

        if not membership_id or not role or not ward_name:
            messages.error(request, 'All fields are required.')
            return render(request, 'create_ward_membership.html')

        try:
            user = UserRegistration.objects.get(membership_id=membership_id)
        except UserRegistration.DoesNotExist:
            messages.error(request, 'User with this membership ID does not exist.')
            return render(request, 'create_ward_membership.html')

        if user.user_status != 'approved':
            messages.error(request, 'User is not approved yet.')
            return render(request, 'create_ward_membership.html')

        ward, created = Ward.objects.get_or_create(name=ward_name)
        
        try:
            ward_membership, created = WardMembership.objects.get_or_create(
                user=user,
                ward=ward,
                defaults={'membership_id': membership_id, 'role': role}
            )
            if not created:
                messages.warning(request, 'This user is already a member of the ward.')
            else:
                messages.success(request, 'Ward membership created successfully.')
        except IntegrityError:
            messages.error(request, 'There was an error creating the ward membership.')
        
        return render(request, 'create_ward_membership.html')

