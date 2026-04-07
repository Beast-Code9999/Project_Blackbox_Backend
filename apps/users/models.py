from django.db import models
# Abstract User and Base User 
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.
class UserManager(BaseUserManager):
    """
    Custom manager which uses email instead of username
    Tella django how to create users for this model
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create user with extra_fields enabled where python captures any additional keyword arguements and passed to the model
        """
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email) # lowercase the domain
        user = self.model(email=email, **extra_fields) # self.model = User class
        user.set_password(password) # hash password
        user.save(using=self._db) # user=self._db writes to correct database
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        superusers need is_staff and is_superuser set to True
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Has everything that Django default User has
    e.g. hashing, permissions, is_active, date_joined etc
    However, we are simply removing username and adding email + name    
    """

    # Override the default related names to avoid clashing with
    # Django's built-in auth.User model. 
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='blackbox_users'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='blackbox_users'
    )

    username = None # removes from model    
    email = models.EmailField(unique=True) # o two users can share the same email
    name = models.CharField(max_length=50)
    USERNAME_FIELD = 'email' # tells django to use email as login field instead of username
    REQUIRED_FIELDS = [] # Fields are prompted when created superuser through CMD, password and email are already handled separately
    objects = UserManager() # attach custom manager

    def __str__(self):
        # What's displayed when user object is printed
        return self.email
