from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from Registration.models import *
from functools import wraps

# Create your views here.




def ward_leader_required(view_func):
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



@method_decorator([login_required, ward_leader_required], name='dispatch')
class WardPendingStatusView(LoginRequiredMixin, View):
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






login_required
ward_leader_required
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



