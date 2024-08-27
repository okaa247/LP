from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from Registration.models import *

# Create your views here.



class NationalMembershipView(UserPassesTestMixin, TemplateView):
    # template_name = 'national_leader/national_membership.html'
    template_name = 'national_leader/super_admin.html'

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

        if national_membership:
            return national_membership.role in ['national_coordinator', 'national_secretary', 'national_treasurer']
        elif state_membership:
            return state_membership.role in ['state_coordinator', 'state_secretary', 'state_treasurer']
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


