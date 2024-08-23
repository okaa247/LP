from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from shortuuidfield import ShortUUIDField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

# Create your models here.




class UserRegistration(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, default='000', null=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    fullname = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=False, unique=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    lga = models.CharField(max_length=200, blank=True, null=True)
    ward = models.CharField(max_length=200, blank=True, null=True)
    pollingunit = models.CharField(max_length=200, blank=True, null=True)
    userimage = models.ImageField(upload_to='user')
    created_at = models.DateTimeField(default=timezone.now)
    membership_id = ShortUUIDField(unique=True, editable=False, max_length=20)
    MEMBERSHIP_STATUS = [
        ('approved', 'Approved'),
        ('pending', 'pending'),
    ]
    user_status = models.CharField(max_length=20, choices=MEMBERSHIP_STATUS, default='pending')

    groups = models.ManyToManyField(
        Group,
        related_name='user_registration_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_registration_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class PollingUnit(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name


class Ward(models.Model):
    name = models.CharField(max_length=100, null=True)
    pollingunit = models.ManyToManyField(PollingUnit)
    chapter_registered = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    members = models.ManyToManyField(UserRegistration, through='WardMembership', related_name='myward')
    
    def __str__(self):
        return self.name



class WardMembership(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    membership_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    ROLE_CHOICES = [
        ('dormant', 'Dormant'),
        ('active', 'Active'),
        ('ward_leader', 'Ward Leader'),
        ('ward_secretary', 'Ward Secretary'),
        ('ward_treasurer', 'Ward Treasurer'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='dormant')

    def __str__(self):
        return f'{self.user} - {self.ward} - {self.role}'





@receiver(post_save, sender=UserRegistration)
def create_ward_membership(sender, instance, created, **kwargs):
    if instance.user_status == 'approved':
        # Fetch or create the Ward corresponding to the name in UserRegistration
        ward, _ = Ward.objects.get_or_create(name=instance.ward)

        # Create or get the WardMembership
        WardMembership.objects.get_or_create(
            user=instance,
            membership_id=instance.membership_id,
            defaults={'ward': ward}  # Use the ward from UserRegistration
        )





class LGA(models.Model):
    name = models.CharField(max_length=100)
    wards = models.ManyToManyField(Ward)
    created_at = models.DateTimeField(default=timezone.now)


class LGAMembership(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='lgward', blank=True, null=True)
    lga = models.ForeignKey(LGA, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    ROLE_CHOICES = [
        ('active', 'Active'),
        ('ward_leader', 'Ward Leader'),
        ('ward_secretary', 'Ward Secretary'),
        ('ward_treasurer', 'Ward Treasurer'),
        ('lga_coordinator', 'LGA Coordinator'),
        ('lga_secretary', 'LGA Secretary'),
        ('lga_treasurer', 'LGA Treasurer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='active')

    def __str__(self):
        return self.user.fullname
    


# @receiver(post_save, sender=WardMembership)
# def create_lga_membership(sender, instance, created, **kwargs):
#     if created:
#         # Fetch the LGA corresponding to the lga name in UserRegistration
#         lga_name = instance.user.lga
#         if lga_name:
#             lga, _ = LGA.objects.get_or_create(name=lga_name)
            
#             # Create or get the LGAMembership
#             LGAMembership.objects.get_or_create(
#                 user=instance.user,
#                 lga=lga
#             )




class MyState(models.Model):
    name = models.CharField(max_length=100)
    lgas = models.ManyToManyField(LGA)
    created_at = models.DateTimeField(default=timezone.now)


class StateMembership(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='statewards', blank=True, null=True)
    state = models.ForeignKey(MyState, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    ROLE_CHOICES = [
        ('active', 'Active'),
        ('ward_leader', 'Ward Leader'),
        ('ward_secretary', 'Ward Secretary'),
        ('ward_treasurer', 'Ward Treasurer'),
        ('lga_coordinator', 'LGA Coordinator'),
        ('lga_secretary', 'LGA Secretary'),
        ('lga_treasurer', 'LGA Treasurer'),
        ('state_coordinator', 'State Coordinator'),
        ('state_secretary', 'State Secretary'),
        ('state_treasurer', 'State Treasurer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='active')

    def __str__(self):
        return self.user.fullname





class National(models.Model):
    name = models.CharField(max_length=100)
    states = models.ManyToManyField(MyState)


class NationalMembership(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='natwards', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    ROLE_CHOICES = [
        ('active', 'Active'),
        ('ward_leader', 'Ward Leader'),
        ('ward_secretary', 'Ward Secretary'),
        ('ward_treasurer', 'Ward Treasurer'),
        ('lga_coordinator', 'LGA Coordinator'),
        ('lga_secretary', 'LGA Secretary'),
        ('lga_treasurer', 'LGA Treasurer'),
        ('state_coordinator', 'State Coordinator'),
        ('state_secretary', 'State Secretary'),
        ('state_treasurer', 'State Treasurer'),
        ('national_coordinator', 'National Coordinator'),
        ('national_secretary', 'National Secretary'),
        ('national_treasurer', 'National Treasurer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='active')
    
    def __str__(self):
        return self.user.fullname


@receiver(post_save, sender=WardMembership)
def create_lga_state_national_memberships(sender, instance, created, **kwargs):
    if created:
        user = instance.user

        # Create or get the LGA Membership
        lga_name = user.lga
        if lga_name:
            lga, _ = LGA.objects.get_or_create(name=lga_name)
            LGAMembership.objects.get_or_create(user=user, lga=lga)

        # Create or get the State Membership
        state_name = user.state
        if state_name:
            state, _ = MyState.objects.get_or_create(name=state_name)
            StateMembership.objects.get_or_create(user=user, state=state)

        # Create or get the National Membership
        national, _ = National.objects.get_or_create(name="Nigeria")  # Assuming there's a single national entity
        NationalMembership.objects.get_or_create(user=user)




class PollingUnitAgent(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='agent')
    polling_unit = models.ForeignKey(PollingUnit, on_delete=models.CASCADE, related_name='polling_unit_agents')
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    AGENT_STATUS = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
    ]
    agent_status = models.CharField(max_length=20, choices=AGENT_STATUS, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.polling_unit.name}"

    def save(self, *args, **kwargs):
        # Check the number of approved agents for the same polling unit
        if self.agent_status == 'approved':
            approved_agents_count = PollingUnitAgent.objects.filter(
                polling_unit=self.polling_unit,
                agent_status='approved'
            ).count()
            
            if approved_agents_count >= 10:
                raise ValidationError("Cannot approve more than 10 agents for this polling unit.")
        
        super().save(*args, **kwargs)




# class Incident(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#     ]
#     reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incidents')
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     media_path = models.CharField(max_length=255, blank=True, null=True)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title




