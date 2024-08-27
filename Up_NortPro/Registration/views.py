from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views import View
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from Up_NortPro.settings import EMAIL_HOST_USER
from django.contrib import messages, auth
from django.utils import timezone
from datetime import timedelta
from django.db.utils import IntegrityError
from django.http import JsonResponse

from django.db import transaction, IntegrityError
from .models import Ward, UserRegistration as User
User = get_user_model()

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.core.exceptions import MultipleObjectsReturned
from django.urls import reverse
from django.http import JsonResponse


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
        
        pollingunit, created = PollingUnit.objects.get_or_create(name=pollingunit)
        ward, created = Ward.objects.get_or_create(name=ward)
        ward.pollingunit.add(pollingunit)

        lga, created = LGA.objects.get_or_create(name=lga)
        lga.wards.add(ward)

        state, created = MyState.objects.get_or_create(name=state)
        state.lgas.add(lga)

        national, created = National.objects.get_or_create(name='Nigeria')
        national.states.add(state)

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

            # Check if the user has a role in StateMembership that requires redirection
            try:
                state_membership = StateMembership.objects.get(user=user)
                if state_membership.role in ['state_coordinator', 'state_secretary', 'state_treasurer']:
                    return redirect('state_lga_list')  # Redirect to the LGA list view
            except StateMembership.DoesNotExist:
                pass  # If no state membership exists, fall through to the default behavior

            return redirect('home')  # Default redirect to the home page
        else:
            return render(request, 'user/login.html', {'error': 'Invalid credentials'})



def Logout(request):
    logout(request)
    messages.success(request, 'Signed out successfully')
    return redirect('login')


    



class Home(View):
    template_name = 'index.html'  # Template to render for GET requests

    def post(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, "You need to log in to perform this action.")
            return redirect('login')  # Redirect to the login page

        user = request.user

        # Check if the user is approved
        if user.user_status != 'approved':
            messages.error(request, "Your status is not approved yet, kindly wait for approval.")
            return redirect('home')  

        # Check if the user has an 'active' role in WardMembership
        active_membership = WardMembership.objects.filter(user=user, role='active').first()
        if not active_membership:
            messages.error(request, "You must be an active member to become a Polling Unit Agent. Kindly wait for the approval!")
            return redirect('home')  

        # Get the user's ward and polling unit
        ward = get_object_or_404(Ward, name=user.ward)
        polling_unit = get_object_or_404(PollingUnit, name=user.pollingunit)

        # Check if the user is already an agent
        existing_agent = PollingUnitAgent.objects.filter(user=user, polling_unit=polling_unit, ward=ward).first()
        if existing_agent:
            messages.info(request, "You are already registered as an agent for this polling unit.")
            return redirect('home')  

        try:
            # Create the PollingUnitAgent instance
            agent = PollingUnitAgent.objects.create(
                user=user,
                polling_unit=polling_unit,
                ward=ward,
                agent_status='pending'  
            )
            agent.save()
            messages.success(request, "You have been successfully registered as a Polling Unit Agent.")
            return redirect('home') 
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('home') 

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)  







# class GetUserInfo(View):
#     def get(self, request):
#         membership_id = request.GET.get('membership_id')
#         try:
#             user = User.objects.get(membership_id=membership_id)
#             data = {
#                 'fullname': user.fullname,
#             }
#         except User.DoesNotExist:
#             data = {
#                 'fullname': None,
#             }
#         return JsonResponse(data)




       



class ForgotPassword(View):
  def get(self, request):
    # messages.success(request, 'Proceed to reset your password')
    return render(request, 'user/forgot-password.html')

  def post(self, request):
    email = request.POST.get('email')

    if not email:
       messages.error(request, 'Email can not be blank')
       return redirect('forgot-password')
    #    return JsonResponse({"email":"Email can not be blank"}, status=400)

    try:
      user = User.objects.get(email=email)
      if not user.is_email_verified:
        messages.error(request, 'Email not verified')
        # return JsonResponse({"reverify":"Email not verified"}, status=400)
        return redirect('reverify')
    except User.DoesNotExist:
      messages.error(request, 'User with this email address does not exist')
    #   return JsonResponse({"signup":"User with this email address does not exist"}, status=400)
      return redirect('signup')

    # Generate a one-time use token for password reset
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # Construct the password reset link
    reset_link = f"http://{request.get_host()}{reverse('reset-password', args=(uid, token))}".strip('/')

    # Send the password reset link to the user's email
    send_mail(
      'Password Reset',
      f'Use this link to reset your password: {reset_link}',
      'emchadexglobal@gmail.com',
      [email],
      fail_silently=False,
    )
    messages.success(request, 'Password reset link sent!')
    # return JsonResponse({"success": 'Password reset link sent to you mail'}, status=200)
    return render(request, 'user/forgot-password.html')
    





class PasswordReset(View):
    def get(self, request, uidb64, token):
        try:
            # Decode the user ID from base64
            uid = force_str(urlsafe_base64_decode(uidb64))
            # Get the user based on the decoded ID
            user = User.objects.get(pk=uid)

            # Check if the token is valid for the user
            if default_token_generator.check_token(user, token):
                # Render the password reset form
                messages.success(request, 'Reset your password here')
                # return JsonResponse({"success": 'Reset your password here'}, status=200)
                return render(request, 'user/reset-password.html', {'validlink': True, 'uidb64': uidb64, 'token': token})
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, MultipleObjectsReturned):
            pass

        # If the link is invalid,
        messages.error(request, 'Reset-link is used. Add your email for a new one.')
        # return JsonResponse({"used":"Reset-link is used. Add your email for a new one."}, status=400) 
        return render(request, 'user/forgot-password.html')
    


    def post(self, request, uidb64, token):
        # Handle the form submission to set a new password
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # if not password:
        #     return JsonResponse({"password":"Password can not be blank"}, status=400)
        
        # if not confirm_password:
        #     return JsonResponse({"confirm_password":"Confirm your password"}, status=400)
 
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            # return JsonResponse({"missmatch":"Passwords do not match, enter again!"}, status=400)
            return render(request, 'user/reset-password.html')

        # Set the new password
        user.set_password(password)
        user.save()

        # Redirect to the login page
        messages.success(request, 'Password reset success!  Login')
        # return JsonResponse({"success":"Password reset successful!  Login"}, status=200)
        return redirect('login')



