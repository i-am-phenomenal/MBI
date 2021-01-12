from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.

class Manager(AbstractBaseUser,PermissionsMixin, models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emailId= models.CharField(max_length=50, db_column="email_id", unique=True)
    firstName = models.CharField(max_length=50, db_column="first_name")
    lastName = models.CharField(max_length=50, db_column="last_name")
    password = models.CharField(max_length=200)
    dateOfBirth = models.DateField(db_column="date_of_birth")
    company = models.CharField(max_length=50) 

    isAdmin = models.BooleanField(default=False, db_column="is_admin")
    isStaff = models.BooleanField(default=False, db_column="is_staff")
    isActive = models.BooleanField(default=False, db_column="is_active")
    isSuperuser = models.BooleanField(default=False, db_column="is_superuser")
    
    insertedAt = models.DateTimeField(db_column="inserted_at")
    updatedAt = models.DateTimeField(auto_now=True, db_column="updated_at")

    USERNAME_FIELD = 'emailId'
    REQUIRED_FIELDS = ('password', 'company', "dateOfBirth")

    def get_short_name(self):
        return self.emailId

    def get_full_name(self):
        return  self.emailId

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def natural_key(self):
        return self.emailId

    @property
    def is_staff(self):
        return self.isStaff

    @property
    def is_superuser(self):
        return self.isSuperuser

    @property
    def is_active(self):
        return self.isActive