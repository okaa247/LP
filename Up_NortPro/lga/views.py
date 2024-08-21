from django.shortcuts import render, get_object_or_404, redirect
from Registration.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

# Create your views here.


class LGACoordinatorView(LoginRequiredMixin, View):
    template_name = 'lga_leader/lga_wards_update.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        # Check if the user is an LGA Coordinator
        lga_membership = get_object_or_404(LGAMembership, user=user, role='lga_coordinator')

        # Get the wards under the user's LGA with chapter_registered=False
        lga = lga_membership.lga
        wards = lga.wards.filter(chapter_registered=False)

        context = {
            'wards': wards,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Handle the form submission to change the chapter_registered status
        ward_id = request.POST.get('ward_id')
        ward = get_object_or_404(Ward, id=ward_id)

        # Toggle the chapter_registered status
        ward.chapter_registered = not ward.chapter_registered
        ward.save()

        messages.success(request, f"The chapter_registered status for {ward.name} has been updated.")
        return redirect('lga_coordinator_view')





class LGACoordinatorWardListView(LoginRequiredMixin, View):
    template_name = 'lga_leader/lga_ward_list.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        # Check if the user is an LGA Coordinator
        lga_membership = get_object_or_404(LGAMembership, user=user, role='lga_coordinator')

        # Get the wards under the user's LGA with chapter_registered=True
        lga = lga_membership.lga
        wards = lga.wards.filter(chapter_registered=True)

        # Annotate each ward with the number of members
        wards_with_counts = []
        for ward in wards:
            member_count = ward.members.count()
            wards_with_counts.append({
                'ward': ward,
                'member_count': member_count
            })

        # Calculate total users in the LGA
        total_users = sum(item['member_count'] for item in wards_with_counts)

        context = {
            'wards_with_counts': wards_with_counts,
            'total_users': total_users,
        }
        return render(request, self.template_name, context)






@method_decorator(login_required, name='dispatch')
class LGAUserSearchView(View):
    def get(self, request):
        # Ensure the user is an LGA Coordinator
        lga_membership = get_object_or_404(LGAMembership, user=request.user, role='lga_coordinator')

        # Get the wards under the LGA
        lga = lga_membership.lga
        wards = lga.wards.all()

        # Filter users based on the ward and membership_id if provided
        ward = request.GET.get('ward')
        membership_id = request.GET.get('membership_id')
        users = UserRegistration.objects.filter(lga=lga.name)

        if ward:
            users = users.filter(ward=ward)
        if membership_id:
            users = users.filter(membership_id=membership_id)

        context = {
            'users': users,
            'wards': wards,
            'selected_ward': ward,
            'membership_id': membership_id,
        }
        return render(request, 'lga_leader/statusupdate.html', context)

    def post(self, request):
        # Get the user and the new role
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')

        user_to_update = get_object_or_404(UserRegistration, id=user_id)
        ward_membership = get_object_or_404(WardMembership, user=user_to_update, ward__name=user_to_update.ward)

        # Update the role in WardMembership
        ward_membership.role = new_role
        ward_membership.save()

        messages.success(request, f"{user_to_update.fullname}'s role has been updated to {new_role}.")
        return redirect('ward_status_update')



