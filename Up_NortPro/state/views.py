from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from Registration.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.





class StateLGAListView(LoginRequiredMixin, TemplateView):
    # template_name = 'state_leader/state_lga_list.html'
    template_name = 'state_leader/abia_state.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.statewards.filter(role__in=['state_coordinator', 'state_secretary', 'state_treasurer']).exists():
            # Get the logged-in user's state
            user_state_membership = get_object_or_404(StateMembership, user=user)
            user_state = user_state_membership.state

            # Get all LGAs in the user's state
            lgas_in_state = user_state.lgas.all()

            # Calculate the number of LGAMembership for each LGA
            lga_membership_counts = LGAMembership.objects.filter(lga__in=lgas_in_state).values('lga__name').annotate(count=Count('id'))

            # Total users in the state (sum of all LGAMembership in the state)
            total_users_in_state = LGAMembership.objects.filter(lga__in=lgas_in_state).count()

            context['lgas'] = lgas_in_state
            context['lga_membership_counts'] = lga_membership_counts
            context['total_users_in_state'] = total_users_in_state
            context['state_name'] = user_state.name

        else:
            messages.error(self.request, 'You do not have permission to view this page.')
            return redirect('home')
        
        return context

        




class StateUserSearchView(View):
    def get(self, request):
        # Ensure the user is either a state secretary, state treasurer, or state coordinator
        state_membership = get_object_or_404(StateMembership, user=request.user, role__in=['state_secretary', 'state_treasurer', 'state_coordinator'])

        # Get the wards under the state
        state = state_membership.state
        lgas = state.lgas.all()

        # Filter users based on the LGA and membership_id if provided
        lga = request.GET.get('lga')
        membership_id = request.GET.get('membership_id')
        users = UserRegistration.objects.filter(state=state.name)

        if lga:
            users = users.filter(lga=lga)
        if membership_id:
            users = users.filter(membership_id=membership_id)

        # Precompute the LGA membership for each user
        user_lga_memberships = []
        for user in users:
            try:
                lga_membership = LGAMembership.objects.filter(user=user, lga__name=user.lga).first()
            except LGAMembership.DoesNotExist:
                lga_membership = None

            user_lga_memberships.append({
                'user': user,
                'lga_membership': lga_membership
            })

        context = {
            'users': users,
            'lgas': lgas,
            'selected_lga': lga,
            'membership_id': membership_id,
            'user_lga_memberships': user_lga_memberships,
        }
        return render(request, 'state_leader/lga_statusupdate.html', context)

    def post(self, request):
        # Get the user and the new role
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')

        user_to_update = get_object_or_404(UserRegistration, id=user_id)
        lga_membership = get_object_or_404(LGAMembership, user=user_to_update, lga__name=user_to_update.lga)

        # Update the role in LGAMembership
        lga_membership.role = new_role
        lga_membership.save()

        messages.success(request, f"{user_to_update.fullname}'s role has been updated to {new_role}.")
        return redirect('lga_status_update')











class UserSearchAndRoleUpdateView(LoginRequiredMixin, View):
    template_name = 'state_leader/role_update.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        query = request.GET.get('q')
        state_membership = StateMembership.objects.filter(user=user, role__in=['state_coordinator', 'state_secretary', 'state_treasurer']).first()

        if not state_membership:
            messages.error(request, 'You do not have permission to view this page.')
            return redirect('home')

        state = state_membership.state
        results = None

        if query:
            results = UserRegistration.objects.filter(
                Q(lga__icontains=query) |
                Q(ward__icontains=query) |
                Q(email__icontains=query) |
                Q(membership_id__icontains=query),
                state=state.name
            ).distinct()

        return render(request, self.template_name, {'results': results, 'query': query})

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('new_role')

        user = get_object_or_404(UserRegistration, id=user_id)
        lga = LGA.objects.get(name=user.lga)

        lga_membership, created = LGAMembership.objects.get_or_create(user=user, lga=lga)
        lga_membership.role = new_role
        lga_membership.save()

        messages.success(request, f"{user.fullname}'s role has been updated to {new_role}.")
        return redirect('user_search_and_role_update')








