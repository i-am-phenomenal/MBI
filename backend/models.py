from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.

class PaymentMethod(models.Model): 
    id = models.CharField(max_length=50, primary_key=True, editable=False)
    type = models.CharField(max_length=50, default="card")
    cardNumber = models.CharField(max_length=50, db_column="card_number")
    expiryMonth = models.IntegerField(db_column="expiry_month")
    expiryYear = models.IntegerField(db_column="expiry_year")
    cvv = models.CharField(max_length=3)
    insertedAt = models.DateTimeField(db_column="inserted_at")
    updatedAt = models.DateTimeField(auto_now=True, db_column="updated_at")


class Manager(AbstractBaseUser,PermissionsMixin, models.Model):
    id = models.CharField(max_length=50, primary_key=True, editable=False)
    emailId= models.CharField(max_length=50, db_column="email_id", unique=True)
    firstName = models.CharField(max_length=50, db_column="first_name")
    lastName = models.CharField(max_length=50, db_column="last_name")
    password = models.CharField(max_length=200)
    dateOfBirth = models.DateField(db_column="date_of_birth")
    company = models.CharField(max_length=50) 
    cardDetails = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)

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

class Product(models.Model):
    id = models.CharField(max_length=100, db_column="product_id", primary_key=True, editable=False)
    productName = models.CharField(max_length=50, db_column="product_name")
    insertedAt = models.DateTimeField(db_column="inserted_at")
    updatedAt = models.DateTimeField(auto_now=True, db_column="updated_at")

class Price(models.Model):
    id = models.CharField(max_length=100, primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    currency = models.CharField(max_length=10)
    unitAmount = models.IntegerField(default=0, db_column="unit_amount")
    billingScheme = models.CharField(max_length=20, default="per_unit", db_column="billing_scheme")
    interval = models.CharField(max_length=10, default="month")
    intervalCount = models.IntegerField(default=1, db_column="interval_count")
    insertedAt = models.DateTimeField(db_column="inserted_at")
    updatedAt = models.DateTimeField(auto_now=True, db_column="updated_at")

class Subscription(models.Model): 
    id = models.CharField(max_length=100, primary_key=True, editable=False)
    customer = models.ForeignKey(Manager, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    insertedAt = models.DateTimeField(db_column="inserted_at")
    updatedAt = models.DateTimeField(auto_now=True, db_column="updated_at")

# Subscription -> Card details  -> Cancel and resume Subscription -> Update Card details 