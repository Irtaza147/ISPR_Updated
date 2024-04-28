from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib import messages
from packaging import version
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView 
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .forms import UserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core import serializers
from django.conf import settings
import os
from .models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from datetime import datetime, date
from django.core.exceptions import ValidationError
from . import models
import operator
import itertools
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.hashers import make_password
from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from django.http import HttpResponseServerError
from subprocess import run,PIPE
from .forms import FirmwareForm
from .models import Firmware
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import Firmware
from .forms import FirmwareForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.http import HttpResponse
from .utils import crawl_website
from .signal import search_website
from django.core.cache import cache
from multiprocessing import Process
import pandas as pd
from django.http import JsonResponse
from .models import ScrapedData
from .models import SearchData



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']

            if role == 'admin':
                user.is_admin = True
            elif role == 'vendor':
                user.is_vendor = True
            elif role == 'regular':
                user.is_regularuser = True

            user.save()
            login(request, user)
            return redirect('home')  # Replace with the URL you want to redirect to after signup
    else:
        form = SignupForm()

    return render(request, 'dashboard/signup.html', {'form': form})

def edit_firmware(request, firmware_id):
    firmware_record = get_object_or_404(Firmware, id=firmware_id)

    if request.method == 'POST':
        form = FirmwareForm(request.POST, request.FILES, instance=firmware_record)
        if form.is_valid():
            # Use form's save method to handle updates and file changes
            form.save()
            return redirect('firmware_records')
    else:
        form = FirmwareForm(instance=firmware_record)

    return render(request, 'dashboard/edit_records.html', {'form': form, 'firmware_record': firmware_record})

def delete_firmware(request, firmware_id):
    firmware_record = get_object_or_404(Firmware, id=firmware_id)
    firmware_record.delete()
    return redirect('firmware_records')

def firmware_records(request):
    firmware_records = Firmware.objects.all()

    context = {
        'firmware_records': firmware_records,
    }

    return render(request, 'dashboard/show_record.html', context)


def delete_record(request, record_id):
    firmware_record = get_object_or_404(Firmware, id=record_id)

    if request.method == 'POST':
        firmware_record.delete()
        return redirect('firmware_records')

    return render(request, 'dashboard/show_record.html', {'firmware_record': firmware_record})




def home(request):
    return render(request, 'dashboard/Welcome.html')

def delete_all_scraped_data(request):
    if request.method == 'POST':
        # Delete all records in the ScrapedData model
        ScrapedData.objects.all().delete()
        # Redirect to the 'crawler' URL
        return redirect('crawler')  # Assuming 'crawler' is the name of your URL pattern
    return render(request, 'dashboard/Crawler.html')


def crawler(request):
    if request.method == 'POST':
        website_url = request.POST.get('website_url')  # Retrieve the URL from the form data
        if website_url:
            if cache.get('crawl_in_progress'):
                # Crawl is already in progress, return an error response
                message = 'Crawl in progress. Please wait.'
                return render(request, 'dashboard/Crawler.html', {'message': message})

            try:
                # Set flag to indicate crawl is in progress
                cache.set('crawl_in_progress', True)
                print(website_url)
                
                # Attempt to crawl the website
                crawl_website(website_url)  # Pass the URL to the function to start the scraper
                message = "Crawling process initiated successfully."

                # Clear the flag to indicate crawl is completed
                cache.delete('crawl_in_progress')
            except Exception as e:
                # Handle any errors that occur during crawling
                message = f"An error occurred: {str(e)}"
                # Log the error for further debugging if needed
                print("Error occurred during crawling:", e)
                # Clear the flag in case of error
                cache.delete('crawl_in_progress')
                # Return a server error response with the error message
                return HttpResponseServerError(message)
            
            try:
                # Retrieve scraped data from the database
                scraped_data = ScrapedData.objects.all()
                if not scraped_data:
                    message = "No scraped data found."
                    return render(request, 'dashboard/Crawler.html', {'message': message})
                else:
                    # Pass data to template context along with the message
                    return render(request, 'dashboard/Crawler.html', {'message': message, 'scraped_data': scraped_data})
            except Exception as e:
                message = f"An error occurred: {str(e)}"
                return HttpResponseServerError(message)
        else:
            # If URL is empty, render the form page again with an error message
            message = "Please provide a valid website URL."
            return render(request, 'dashboard/Crawler.html', {'message': message})
        
    else:
        # Render the form page initially
        return render(request, 'dashboard/Crawler.html')
    



def dashboard(request):
    return render(request,'dashboard/dashboard.html')

def admin_login(request):
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials. Please enter Only Admin credentials on this page.")
                return redirect('admin_login')
        else:
            messages.error(request, "This user is not found in database")
            return redirect('admin_login') 
     return render(request, 'dashboard/Admin_login.html')

def vendor_login(request):
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_vendor:
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials. Please enter Only Vendor credentials on this page.")
                return redirect('vendor_login')
        else:
            messages.error(request, "This user is not found in database")
            return redirect('vendor_login') 
     return render(request, 'dashboard/vendor_login.html')

def user_login(request):
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
         if user.is_regularuser:
        # Successful login for a regular user
           auth.login(request, user)
           return redirect('dashboard')
         else:
        # Incorrect credentials or user doesn't have the is_regularuser role
           messages.error(request, "Invalid credentials. Please enter Only User credentials on this page.")
           return redirect('user_login')  # Assuming 'user_login' is the correct URL name      
        else:
            messages.error(request, "This user is not found in database")
            return redirect('user_login') 
     return render(request, 'dashboard/user.html')

        

def logout_view(request):
    logout(request)
    return redirect('/')                


def add_Firmware(request):
    if request.method == 'POST':
        form = FirmwareForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect or do something else upon successful form submission
            return redirect('firmware_records')
        else:
            # Form is not valid, handle the error
            print(form.errors)
    else:
        form = FirmwareForm()

    choice = {'form': form}
    return render(request, 'dashboard/add_record.html', choice)



def download_prompt_view(request):
    # Logic to retrieve download prompt message and download link
    # For example, you might pass these as context variables
    download_prompt = "Do you want to download the newer version (V1.60)? [yes/no]"
    download_link = "http://example.com/download"

    return render(request, 'dashboard/download_prompt.html', {'download_prompt': download_prompt, 'download_link': download_link})


def save_record(request):
    if request.method == 'POST':
        form = FirmwareForm(request.POST, request.FILES)
        if form.is_valid():
            device_model = form.cleaned_data['device_model']  # Get the device model from the form data
            # Get the firmware version entered by the user
            user_firmware_version = form.cleaned_data['current_version']
             # Callback function to handle the scraped data


            def handle_scraped_data(scraped_data):
                if scraped_data:
                    scraped_version = scraped_data['firmware_version']
                    # Compare versions after converting them to a comparable format
                    if version.parse(scraped_version) == version.parse(user_firmware_version):
                        messages.info(request, f"Same version found for {device_model}: {scraped_version}")
                    elif version.parse(scraped_version) > version.parse(user_firmware_version):
                        download_link = scraped_data['download_link']
                        if download_link:
                           messages.warning(request, f"A newer version ({scraped_version}) is available for {device_model}.")
                           messages.info(request, f"Download it <a href='{download_link}'>....here</a>.")
                        else:
                           messages.warning(request, f"A newer version ({scraped_version}) is available for {device_model}, but no download link was found on website.")
                    else:
                        messages.warning(request, f"Older version found for {device_model}: {scraped_version}")
                else:
                    messages.warning(request, f"No scraped data found for {device_model}")
            
            # Trigger the crawling process and pass the callback function
            search_website(url=device_model, callback=handle_scraped_data)


            # Save form data
            form.save()
            messages.success(request, 'Firmware Registered Successfully')
            return redirect('add_Firmware')  # Redirect to a success page after successful form submission
    else:
        form = FirmwareForm()
    
    firmware_records = Firmware.objects.all()
    return render(request, 'dashboard/add_record.html', {'form': form, 'firmware_records': firmware_records})




class UserView(ListView):
    model = User
    template_name = 'dashboard/list_user.html'
    context_object_name = 'users'
    paginate_by = 5

    def get_queryset(self):
        return User.objects.order_by('-id')




   


class UserUpdateView(BSModalUpdateView):
    model = User
    template_name = 'dashboard/u_update.html'
    form_class = UserForm
    success_message = 'Success: Data was updated.'
    success_url = reverse_lazy('users')

    

class UserReadView(BSModalReadView):
    model = User
    template_name = 'dashboard/view_user.html'




class DeleteUser(BSModalDeleteView):
    model = User
    template_name = 'dashboard/delete_user.html'
    success_message = 'Success: Data was deleted.'
    success_url = reverse_lazy('users')



def create(request):
    choice = ['1', '0', 5000, 10000, 15000, 'Register', 'Admin', 'Vendor','Regular_User']
    choice = {'choice': choice}
    if request.method == 'POST':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            username=request.POST['username']
            userType=request.POST['userType']
            email=request.POST['email']
            password=request.POST['password']
            password = make_password(password)
            print("Hashed Password:", password)
            print("User Type")
            print(userType)
            
            if userType == "Vendor":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_vendor=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users')
            
            elif userType == "Admin":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_admin=True,is_superuser=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users') 
              
            elif userType == "Regular_User":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_regularuser=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users')  
            else:
                messages.success(request, 'Member was not created')
                return redirect('users')
    else:
        choice = ['1', '0', 5000, 10000, 15000, 'Register', 'Admin', 'Vendor','Regular_User']
        choice = {'choice': choice}
        return render(request, 'dashboard/add.html', choice)


    
    

