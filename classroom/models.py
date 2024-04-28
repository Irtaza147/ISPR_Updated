from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_regularuser = models.BooleanField(default=False)

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Firmware(models.Model):
    name = models.CharField(max_length=255)
    device_model = models.CharField(max_length=100)
    current_version = models.CharField(max_length=20)
    firmware_file = models.FileField(upload_to='firmwares/', blank=True, null=True)

    def __str__(self):
        return self.name


class ScrapedData(models.Model):
    model_name = models.CharField(max_length=100)
    firmware_version = models.CharField(max_length=100)
    source_url = models.URLField()
    download_link = models.CharField(max_length=255, null=True, blank=True)
    tenda_download_link = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
     return f"{self.model_name} - {self.firmware_version}"



class SearchData(models.Model):
    Model_name = models.CharField(max_length=100)
    Firmware_version = models.CharField(max_length=100)
    Source_url = models.URLField()
    Download_link = models.CharField(max_length=255, null=True, blank=True)
    Tenda_download_link = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
     return f"{self.Model_name} - {self.Firmware_version}"























class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_color = models.CharField(max_length=100)
    comment = models.TextField(max_length=5000, blank=True)
    cost_per_day = models.IntegerField(null=True, blank=True)
    is_payed = models.BooleanField(default=False)
    price = models.TextField(max_length=5000, blank=True)
    device = models.TextField(max_length=5000, blank=True)
    days_spent = models.CharField(null=True, blank=True, max_length=1000)
    total_cost = models.IntegerField(null=True, blank=True)
    register_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=100)
    reg_date = models.DateTimeField(auto_now_add=True)
    exit_date = models.DateTimeField(null=True, blank=True)    

class ImageUploadForm(models.Model):
    image = models.ImageField(upload_to="myimage")
    date = models.DateTimeField(auto_now_add=True)