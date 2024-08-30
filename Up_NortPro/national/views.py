from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView, View, ListView
from Registration.models import *
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
# Create your views here.




class NationalMembershipView(UserPassesTestMixin, TemplateView):
    # template_name = 'national_leader/national_membership.html'
    template_name = 'national_leader/super_admin1.html'

    def test_func(self):
        # Check if the user has the required roles
        user = self.request.user
        national_membership = NationalMembership.objects.filter(user=user).first()
        if national_membership:
            return national_membership.role in ['national_coordinator', 'national_secretary', 'national_treasurer']
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Query all states
        states = MyState.objects.all()

        # Prepare the data to display
        state_data = []
        for state in states:
            lgas = state.lgas.all()
            lga_count = lgas.count()

            ward_count = 0
            polling_unit_count = 0
            for lga in lgas:
                wards = lga.wards.all()
                ward_count += wards.count()
                for ward in wards:
                    polling_unit_count += ward.pollingunit.all().count()

            user_count = StateMembership.objects.filter(state=state).count()

            state_data.append({
                'state': state,
                'lga_count': lga_count,
                'ward_count': ward_count,
                'polling_unit_count': polling_unit_count,
                'user_count': user_count,
            })

        context['state_data'] = state_data
        return context





class LGAMembershipView(UserPassesTestMixin, TemplateView):
    template_name = 'national_leader/lga_membership.html'

    def test_func(self):
        # Check if the user has the required roles
        user = self.request.user
        national_membership = NationalMembership.objects.filter(user=user).first()
        state_membership = StateMembership.objects.filter(user=user).first()

        if national_membership and national_membership.role in ['national_coordinator', 'national_secretary', 'national_treasurer']:
            return True
        elif state_membership and state_membership.role in ['state_coordinator', 'state_secretary', 'state_treasurer']:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        state_id = self.kwargs.get('state_id')
        state = get_object_or_404(MyState, id=state_id)

        # Query all LGAs within the state
        lgas = state.lgas.all()

        # Prepare the data to display
        lga_data = []
        for lga in lgas:
            wards = lga.wards.all()
            ward_count = wards.count()

            polling_unit_count = 0
            for ward in wards:
                polling_unit_count += ward.pollingunit.all().count()

            user_count = LGAMembership.objects.filter(lga=lga).count()

            lga_data.append({
                'lga': lga,
                'ward_count': ward_count,
                'polling_unit_count': polling_unit_count,
                'user_count': user_count,
            })

        context['state'] = state
        context['lga_data'] = lga_data
        return context





class WardMembershipView(UserPassesTestMixin, TemplateView):
    template_name = 'national_leader/ward_membership.html'

    def test_func(self):
        # Check if the user has the required roles
        user = self.request.user
        national_membership = NationalMembership.objects.filter(user=user).first()
        state_membership = StateMembership.objects.filter(user=user).first()
        lga_membership = LGAMembership.objects.filter(user=user).first()

        if national_membership and national_membership.role in ['national_coordinator', 'national_secretary', 'national_treasurer']:
            return True
        elif state_membership and state_membership.role in ['state_coordinator', 'state_secretary', 'state_treasurer']:
            return True
        elif lga_membership and lga_membership.role in ['lga_coordinator', 'lga_secretary', 'lga_treasurer']:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lga_id = self.kwargs.get('lga_id')
        lga = get_object_or_404(LGA, id=lga_id)

        # Query all wards within the LGA
        wards = lga.wards.all()

        # Prepare the data to display
        ward_data = []
        for ward in wards:
            polling_unit_count = ward.pollingunit.all().count()
            user_count = WardMembership.objects.filter(ward=ward).count()

            ward_data.append({
                'ward': ward,
                'polling_unit_count': polling_unit_count,
                'user_count': user_count,
            })

        context['lga'] = lga
        context['ward_data'] = ward_data
        context['state_id'] = lga.mystate_set.first().id
        return context







class PollingUnitView(UserPassesTestMixin, TemplateView):
    template_name = 'national_leader/pollingunit_list.html'

    def test_func(self):
        user = self.request.user
        national_membership = NationalMembership.objects.filter(user=user).first()
        state_membership = StateMembership.objects.filter(user=user).first()
        lga_membership = LGAMembership.objects.filter(user=user).first()
        ward_membership = WardMembership.objects.filter(user=user).first()

        if national_membership and national_membership.role in ['national_coordinator', 'national_secretary', 'national_treasurer']:
            return True
        elif state_membership and state_membership.role in ['state_coordinator', 'state_secretary', 'state_treasurer']:
            return True
        elif lga_membership and lga_membership.role in ['lga_coordinator', 'lga_secretary', 'lga_treasurer']:
            return True
        elif ward_membership and ward_membership.role in ['ward_leader', 'ward_secretary', 'ward_treasurer']:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ward_id = self.kwargs.get('ward_id')
        ward = get_object_or_404(Ward, id=ward_id)

        # Get the LGA associated with the ward
        lga = ward.lga_set.first()

        # Query all polling units within the Ward
        polling_units = ward.pollingunit.all()

        # Prepare the data to display
        pollingunit_data = []
        for pollingunit in polling_units:
            # Filter users by polling unit and only count those with user_status = 'approved'
            user_count = UserRegistration.objects.filter(
                pollingunit=pollingunit.name, 
                user_status='approved'
            ).count()

            pollingunit_data.append({
                'pollingunit': pollingunit,
                'user_count': user_count,
            })

        context['ward'] = ward
        context['pollingunit_data'] = pollingunit_data
        context['lga'] = lga  # Add LGA to the context
        return context





class PollingUnitUsersView(UserPassesTestMixin, TemplateView):
    template_name = 'national_leader/pollingunit_users_list.html'

    def test_func(self):
        user = self.request.user
        national_membership = NationalMembership.objects.filter(user=user).first()
        state_membership = StateMembership.objects.filter(user=user).first()
        lga_membership = LGAMembership.objects.filter(user=user).first()
        ward_membership = WardMembership.objects.filter(user=user).first()

        if national_membership and national_membership.role in ['national_coordinator', 'national_secretary', 'national_treasurer']:
            return True
        elif state_membership and state_membership.role in ['state_coordinator', 'state_secretary', 'state_treasurer']:
            return True
        elif lga_membership and lga_membership.role in ['lga_coordinator', 'lga_secretary', 'lga_treasurer']:
            return True
        elif ward_membership and ward_membership.role in ['ward_leader', 'ward_secretary', 'ward_treasurer']:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pollingunit_name = self.kwargs.get('pollingunit_name')
        
        # Fetch the polling unit and its associated approved users
        pollingunit = get_object_or_404(PollingUnit, name=pollingunit_name)
        approved_users = UserRegistration.objects.filter(pollingunit=pollingunit.name, user_status='approved')
        
        context['pollingunit'] = pollingunit
        context['approved_users'] = approved_users
        return context





class StateMembershipUpdateView(UserPassesTestMixin, View):
    template_name = 'national_leader/state_role_update.html'

    def test_func(self):
        user = self.request.user
        national_membership = NationalMembership.objects.filter(user=user).first()
        return national_membership and national_membership.role in ['national_coordinator', 'national_secretary', 'national_treasurer']

    def get(self, request, *args, **kwargs):
        state_filter = request.GET.get('state')
        member_id_filter = request.GET.get('membership_id')

        memberships = StateMembership.objects.select_related('user', 'state').all()

        if state_filter:
            memberships = memberships.filter(state__name__icontains=state_filter)
        
        if member_id_filter:
            memberships = memberships.filter(user__membership_id__icontains=member_id_filter)
        
        states = MyState.objects.all()

        return render(request, self.template_name, {
            'state_memberships': memberships,
            'states': states,
            'selected_state': state_filter,
            'membership_id': member_id_filter,
        })

    def post(self, request, *args, **kwargs):
        membership_id = request.POST.get('membership_id')
        new_role = request.POST.get('role')

        membership = get_object_or_404(StateMembership, id=membership_id)
        membership.role = new_role
        membership.save()

        return redirect('state_membership_update')






# Helper function to check if the user has the required role
def is_national_staff(user):
    national_roles = ['national_coordinator', 'national_secretary', 'national_treasurer']
    return user.natwards.filter(role__in=national_roles).exists()

@method_decorator(user_passes_test(is_national_staff), name='dispatch')
class NationalUserListView(ListView):
    model = StateMembership
    # template_name = 'national_leader/national_user_list.html'
    template_name = 'national_leader/app-contact.html'
    context_object_name = 'state_memberships'

    def get_queryset(self):
        # Fetch StateMemberships, ordered by state name, with National roles at the top
        national_roles = ['national_coordinator', 'national_secretary', 'national_treasurer']
        state_roles = ['state_coordinator', 'state_secretary', 'state_treasurer']

        national_memberships = NationalMembership.objects.filter(role__in=national_roles)
        state_memberships = StateMembership.objects.filter(role__in=state_roles).order_by('state__name')

        # Concatenate the two querysets
        combined_queryset = list(national_memberships) + list(state_memberships)
        return combined_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['national_roles'] = ['national_coordinator', 'national_secretary', 'national_treasurer']
        return context


