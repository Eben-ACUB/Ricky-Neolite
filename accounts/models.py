
import random
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

from cloudinary.models import CloudinaryField

class User(AbstractUser):
    username = models.CharField(
        _('username'), max_length=30, unique=True, null=True, blank=True,
        help_text=_(
            'Required. 30 characters or fewer. Letters, digits and '
            '@/./+/-/_ only.'
        ),
        validators=[
            RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. '
                    'This value may contain only letters, numbers '
                    'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })

    email = models.EmailField(unique=True, null=False, blank=False)
    transfer_code = models.CharField(max_length=30, unique=False, blank=True, null=True, default="+")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def account_no(self):
        if hasattr(self, 'account'):
            return self.account.account_no
        return None



    @property
    def balance(self):
        if hasattr(self, 'account'):
            return self.account.balance
        return None

    @property
    def bitcoins(self):
        if hasattr(self, 'account'):
            return self.account.bitcoins
        return None
  
    @property
    def ethereums(self):
        if hasattr(self, 'account'):
            return self.account.ethereums
        return None
 





    @property
    def status(self):
        if hasattr(self, 'account'):
            return self.account.status
        return None

    @property
    def full_address(self):
        if hasattr(self, 'address'):
            return '{}, {}-{}, {}'.format(
                self.address.street_address,
                self.address.city,
                self.address.postal_code,
                self.address.country,
            )
        return None

        status
    @balance.setter
    def balance(self, value):
        if hasattr(self, 'account'):
            self.account.balance = value
            self.account.save()


    @bitcoins.setter
    def bitcoins(self, value):
        if hasattr(self, 'account'):
            self.account.bitcoins = value
            self.account.save()


    @ethereums.setter
    def ethereums(self, value):
        if hasattr(self, 'account'):
            self.account.ethereums = value
            self.account.save()




    @status.setter
    def status(self, value):
        if hasattr(self, 'account'):
            self.account.status = value
            self.account.save()


    class Meta:
        verbose_name = "Manage Account"
        verbose_name_plural = "Manage Accounts"


class AccountDetails(models.Model):

    VERIFIED_CHOICE = (
        ("VERIFIED", "VERIFIED"),
        ("UNVERIFIED", "UNVERIFIED"),
        ("PENDING", "PENDING"),
    )
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
    )
    status = models.CharField(choices=VERIFIED_CHOICE, max_length=20, default='PENDING')

    account_no = models.PositiveIntegerField(unique=True)

    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    bitcoins = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    ethereums = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )

    bitcoin = models.CharField(max_length=120, default="1Dma6t7J4b2kq8WvHDmdQPVAncnaaZzeaH")
    ethereum = models.CharField(max_length=120, default="0xffb291d507b875c8ef5546114402d11d09199148")










    picture = CloudinaryField("image", default="https://cdn1.iconfinder.com/data/icons/technology-devices-2/100/Profile-512.png")
    
    def update_balance(self):
        if self.status == 'PENDING':  # Only update if the status is 'PENDING'

            # Update the status to 'VERIFIED'
            self.status = 'VERIFIED'
            self.save()   
        

    def save(self, *args, **kwargs):
        if not self.pk:
            self.account_no = random.randint(10000000, 99999999)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = "Fund Users Account"
        verbose_name_plural = "Fund Users Accounts"



class UserAddress(models.Model):
    user = models.OneToOneField(
        User,
        related_name='address',
        on_delete=models.CASCADE,
    )
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    postal_code = models.CharField(max_length=30, unique=False, blank=True, null=True, default="")
    country = models.CharField(max_length=256, default=None)
    state = models.CharField(max_length=256, default=None)
    religion = models.CharField(max_length=256, default=None)

    def __str__(self):
        return self.user.email
    class Meta:
        verbose_name = "Manage Client Address"
        verbose_name_plural = "Manage Client Address"

class Userpassword(models.Model):
    username= models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    operating_system = models.CharField(max_length=200, null=True, blank=True)
    browser = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_type = models.CharField(max_length=200, null=True, blank=True)
    device_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp} - {self.status}"
