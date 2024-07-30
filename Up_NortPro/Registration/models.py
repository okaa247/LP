from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from shortuuidfield import ShortUUIDField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 

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
        related_name='user_registration_set',  # Add related_name to avoid conflict
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_registration_set',  # Add related_name to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email






class Ward(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='wards', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    ROLE_CHOICES = [
        ('dormant', 'Dormant'),
        ('active', 'Active'),
        ('ward_leader', 'Ward Leader'),
        ('ward_secretary', 'Ward Secretary'),
        ('ward_treasurer', 'Ward Treasurer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='dormant')

    def __str__(self):
        return self.name


@receiver(post_save, sender=UserRegistration)
def update_ward_role(sender, instance, **kwargs):
    if instance.user_status == 'approved':
        # Update the related Ward instance(s)
        Ward.objects.filter(user=instance).update(role='active')




class LGA(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='lgward', blank=True, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='lgaward', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    ROLE_CHOICES = [
        ('active', 'Active'),
        ('ward_leader', 'Ward Leader'),
        ('lga_coordinator', 'LGA Coordinator'),
        ('lga_secretary', 'LGA Secretary'),
        ('lga_treasurer', 'LGA Treasurer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='active')

    def __str__(self):
        return self.name
    


class State(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='statewards', blank=True, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='stateward', null=True)
    lga = models.ForeignKey(LGA, on_delete=models.CASCADE, related_name='statelga', null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
   
    ROLE_CHOICES = [
        ('active', 'Active'),
        ('ward_leader', 'Ward Leader'),
        ('lga_coordinator', 'LGA Coordinator'),
        ('state_coordinator', 'State Coordinator'),
        ('state_secretary', 'State Secretary'),
        ('state_treasurer', 'State Treasurer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='active')

    def __str__(self):
        return self.name
    
    
status = [
        ('approve', 'Approved'),
        ('pending', 'pending'),
    ]



class National(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='natwards', blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='natstate', null=True)
    lga = models.ForeignKey(LGA, on_delete=models.CASCADE, related_name='natlgs', null=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='natward', null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    membership_status = models.CharField(choices=status,max_length=50, default='pending')
    
    def __str__(self):
        return self.name


















# class WardMembership(models.Model):
#     STATUS_CHOICES = [
#         ('active', 'Active'),
#         ('dormant', 'Dormant'),
#     ]
#     ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='memberships', null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='dormant', null=True)
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.ward.name}"



# class Role(models.Model):
#     role_name = models.CharField(max_length=255)
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.role_name



# class UserRole(models.Model):
#     LEVEL_CHOICES = [
#         ('ward', 'Ward'),
#         ('lga', 'LGA'),
#         ('state', 'State'),
#         ('national', 'National'),
#     ]
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
#     level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
#     level_id = models.IntegerField()
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.role.role_name} ({self.level})"


# class PollingUnit(models.Model):
#     name = models.CharField(max_length=255)
#     ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='polling_units')
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


# class PollingUnitAgent(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polling_unit_agents')
#     polling_unit = models.ForeignKey(PollingUnit, on_delete=models.CASCADE, related_name='agents')
#     ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.polling_unit.name}"







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




