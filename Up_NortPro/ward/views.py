from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from Registration.models import *
from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.




def ward_leader_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        try:
            # Check if the user is a ward_leader
            membership = WardMembership.objects.get(user=user, role='ward_leader')
        except WardMembership.DoesNotExist:
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper



@method_decorator([login_required, ward_leader_required], name='dispatch')
class WardPendingStatusView(View):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            messages.error(request, "User not authenticated")
            return redirect('login')

        # Get all users with the same ward and user_status = 'pending'
        ward_pending_status_list = UserRegistration.objects.filter(
            ward=user.ward,
            user_status='pending'
        )
        context = {
            'ward_pending_status_list': ward_pending_status_list,
        }
        return render(request, 'ward_leader/pending_status_list.html', context)

    def post(self, request):
        # Fetch the user whose status is to be changed
        user_id = request.POST.get('user_id')
        new_status = request.POST.get('user_status')
        
        user_to_update = get_object_or_404(UserRegistration, id=user_id)
        user_to_update.user_status = new_status
        user_to_update.save()

        messages.success(request, f"{user_to_update.fullname}'s status has been updated to {new_status}.")
        return redirect('pending_status')



def ward_leader_required_function(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        user = request.user
        try:
            # Check if the user is a ward_leader
            membership = WardMembership.objects.get(user=user, role='ward_leader')
        except WardMembership.DoesNotExist:
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
        return view_func(self, request, *args, **kwargs)
    return wrapper


login_required
ward_leader_required_function
def ward_members_view(request):
    # Get the ward associated with the logged-in user
    user_ward_membership = get_object_or_404(WardMembership, user=request.user)
    user_ward = user_ward_membership.ward

    # Get all members of the same ward
    ward_members = WardMembership.objects.filter(ward=user_ward)

    if request.method == 'POST':
        # Loop through each member to update their role
        for member in ward_members:
            role = request.POST.get(f'role_{member.id}')
            if role and role != member.role:
                member.role = role
                member.save()
                messages.success(request, f"Role updated for {member.user.fullname}")

        return redirect('ward_members')

    return render(request, 'ward_leader/ward_members.html', {
        'ward_members': ward_members,
        'user_ward': user_ward
    })





# @login_required
# def create_polling_unit_agent(request):
#     if request.method == "POST":
#         user = request.user

#         if user.user_status != 'approved':
#             return JsonResponse({'success': False, 'message': 'Your status is not approved.'})

#         ward = get_object_or_404(Ward, name=user.ward)
#         polling_unit = get_object_or_404(PollingUnit, name=user.pollingunit)

#         existing_agent = PollingUnitAgent.objects.filter(user=user, polling_unit=polling_unit, ward=ward).first()
#         if existing_agent:
#             return JsonResponse({'success': False, 'message': 'You are already registered as an agent for this polling unit.'})

#         try:
#             PollingUnitAgent.objects.create(
#                 user=user,
#                 polling_unit=polling_unit,
#                 ward=ward,
#                 agent_status='pending'
#             )
#             return JsonResponse({'success': True, 'message': 'You have been successfully registered as a Polling Unit Agent.'})
#         except ValidationError as e:
#             return JsonResponse({'success': False, 'message': str(e)})

#     return JsonResponse({'success': False, 'message': 'Invalid request method.'})











# def create_polling_unit_agent(request):
#     if request.method == "POST":
#         # Get the currently logged-in user
#         user = request.user

#         # Check if the user is approved
#         if user.user_status != 'approved':
#             messages.error(request, "Your status is not approved.")
#             return redirect('some_page')  # Redirect to an appropriate page

#         # Get the user's ward and polling unit
#         ward = get_object_or_404(Ward, name=user.ward)
#         polling_unit = get_object_or_404(PollingUnit, name=user.pollingunit)

#         # Check if the user is already an agent
#         existing_agent = PollingUnitAgent.objects.filter(user=user, polling_unit=polling_unit, ward=ward).first()
#         if existing_agent:
#             messages.info(request, "You are already registered as an agent for this polling unit.")
#             return redirect('some_page')  # Redirect to an appropriate page

#         try:
#             # Create the PollingUnitAgent instance
#             agent = PollingUnitAgent.objects.create(
#                 user=user,
#                 polling_unit=polling_unit,
#                 ward=ward,
#                 agent_status='pending'  # Or 'approved' if you want to auto-approve
#             )
#             agent.save()
#             messages.success(request, "You have been successfully registered as a Polling Unit Agent.")
#             return redirect('home')  # Redirect to an appropriate page
#         except ValidationError as e:
#             messages.error(request, str(e))
#             return redirect('some_page')  # Redirect to an appropriate page

#     return render(request, 'index.html')  # Render the form if the request method is not POST







# def filter_users_by_ward_and_pollingunit(request):
#     # Retrieve query parameters for filtering
#     ward_id = request.GET.get('ward')
#     pollingunit_id = request.GET.get('pollingunit')

#     # Filter users based on ward and polling unit
#     users = UserRegistration.objects.filter(ward=ward_id)
    
#     if ward_id and pollingunit_id:
#         users = UserRegistration.objects.filter(ward=ward_id, pollingunit=pollingunit_id)
#     elif ward_id:
#         users = UserRegistration.objects.filter(ward=ward_id)
#     elif pollingunit_id:
#         users = UserRegistration.objects.filter(pollingunit=pollingunit_id)
#     else:
#         users = UserRegistration.objects.all()  # No filters applied, return all users

#     # Retrieve all wards and polling units for dropdown options
#     wards = Ward.objects.all()
#     polling_units = PollingUnit.objects.all()

#     # Pass the filtered users and dropdown options to the template
#     context = {
#         'users': users,
#         'wards': wards,
#         'polling_units': polling_units,
#     }

#     return render(request, 'filter_users.html', context)



