from django.urls import include, path
from classroom import views
from django.contrib import admin
from classroom import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('vendor_login/', views.vendor_login, name='vendor_login'),
    path('user_login/', views.user_login, name='user_login'),
    path('signup/', views.signup, name='signup'),
    path('crawler/', views.crawler, name='crawler'),
    path('download-prompt/', views.download_prompt_view, name='download_prompt'),
    path('edit/<int:firmware_id>/', views.edit_firmware, name='edit_firmware'),
    path('delete/<int:firmware_id>/',views. delete_firmware, name='delete_firmware'),
    path('delete_all_scraped_data/', views.delete_all_scraped_data, name='delete_all_scraped_data'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_Firmware/', views.add_Firmware, name='add_Firmware'),
    path('save_record/', views.save_record, name='save_record'),
    path('logout/', views.logout_view, name='logout'),
    path('firmware_records/', views.firmware_records, name='firmware_records'),
    path('users/', views.UserView.as_view(), name='users'),
    path('view_user/<int:pk>', views.UserReadView.as_view(), name='view_user'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('user_update/<int:pk>', views.UserUpdateView.as_view(), name='user_update'),
    path('delete_user/<int:pk>', views.DeleteUser.as_view(), name='delete_user'),
    path('create/create', views.create, name='create'),






] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
