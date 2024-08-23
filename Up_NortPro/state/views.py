from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from Registration.models import *
from django.contrib import messages

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

        



# class StateLGAUserSearchView(LoginRequiredMixin, TemplateView):
#     template_name = 'state_leader/state_lga_user_search.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user

#         # Check if the user has the required role
#         if user.statewards.filter(role__in=['state_coordinator', 'state_secretary', 'state_treasurer']).exists():
#             state_membership = get_object_or_404(StateMembership, user=user)
#             state = state_membership.state

#             # Fetch all LGAs in the state
#             lgas_in_state = state.lgas.all()
#             context['lgas'] = lgas_in_state

#             # Handle search filtering
#             selected_lga_id = self.request.GET.get('lga')
#             membership_id = self.request.GET.get('membership_id')
#             lga_users = []

#             if selected_lga_id:
#                 selected_lga = get_object_or_404(LGA, id=selected_lga_id, name__in=lgas_in_state)
#                 context['selected_lga'] = selected_lga

#                 # Filter users by LGA and membership_id
#                 lga_users = LGAMembership.objects.filter(lga=selected_lga)
#                 if membership_id:
#                     lga_users = lga_users.filter(user__membership_id__icontains=membership_id)

#             context['lga_users'] = lga_users
#         else:
#             messages.error(self.request, "You do not have permission to view this page.")
#             return redirect('home')

#         return context

#     def post(self, request, *args, **kwargs):
#         if 'change_role' in request.POST:
#             membership_id = request.POST.get('membership_id')
#             new_role = request.POST.get('new_role')

#             # Update the role in LGAMembership
#             lga_membership = get_object_or_404(LGAMembership, user__membership_id=membership_id)
#             lga_membership.role = new_role
#             lga_membership.save()

#             messages.success(request, f"Role updated successfully for {lga_membership.user.fullname}.")
#             return redirect('state_lga_user_search')

#         return super().post(request, *args, **kwargs)











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




