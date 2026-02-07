from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    
     path("", views.landing_page, name="landing"),
    
    path('organizer_register', views.organizer_register, name='organizer_register'),
    path('login/', views.organizer_login, name='organizer_login'),
    path('dashboard/', views.organizer_dashboard, name='organizer_dashboard'),
    path('logout/', views.organizer_logout, name='organizer_logout'),
    
     path('add-event/', views.add_event, name='add_event'),
    path('events/', views.view_events, name='view_events'),
    path('add-image/<int:event_id>/', views.add_event_image, name='add_event_image'),
    
    path('edit-image/<int:image_id>/', views.edit_event_image, name='edit_event_image'),
path('delete-image/<int:image_id>/', views.delete_event_image, name='delete_event_image'),
path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),

path('cancel-requests/', views.cancel_requests, name='cancel_requests'),
path('approve-cancel/<int:reg_id>/', views.approve_cancel, name='approve_cancel'),
path('reject-cancel/<int:reg_id>/', views.reject_cancel, name='reject_cancel'),
path('add-result/<int:event_id>/', views.add_result, name='add_result'),

path('media/add/', views.add_media, name='add_media'),
path('media/view/', views.view_media, name='view_media'),
path('media/image/edit/<int:image_id>/', views.edit_image, name='edit_image'),
path('media/video/edit/<int:video_id>/', views.edit_video, name='edit_video'),
path('media/image/delete/<int:image_id>/', views.delete_image, name='delete_image'),
path('media/video/delete/<int:video_id>/', views.delete_video, name='delete_video'),
    path('gallery/add/', views.add_gallery_image, name='add_gallery_image'),
path('gallery/edit/<int:id>/', views.edit_gallery_image, name='edit_gallery_image'),
    path('gallery/delete/<int:id>/', views.delete_gallery_image, name='delete_gallery_image'),


path("forgot-password/", views.forgot_password, name="forgot_password"),
path("verify-otp/", views.verify_otp, name="verify_otp"),
path("reset-password/", views.reset_password, name="reset_password"),

# -----------------------------
#  USER 
# -----------------------------


    path('user_register/', views.user_register, name='user_register'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),

    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user_programs/', views.view_programs, name='view_programs'),
    
    path('register-program/<int:event_id>/', views.register_program_form, name='register_program_form'),
    path('register-program-submit/<int:event_id>/', views.register_program_submit, name='register_program_submit'),
    path('my-programs/', views.my_programs, name='my_programs'),
    path('cancel-request/<int:reg_id>/',views.request_cancel_registration,name='request_cancel_registration'),
    path('results/', views.view_results, name='view_results'),
    path("user/forgot-password/", views.user_forgot_password, name="user_forgot_password"),
    path("user/verify-otp/", views.user_verify_otp, name="user_verify_otp"),
    path("user/reset-password/", views.user_reset_password, name="user_reset_password"),



# -----------------------------
#  ADMIN 
# -----------------------------



path('admin/login/', views.admin_login, name='admin_login'),
path('admin/register/', views.admin_register, name='admin_register'),
path('admin/logout/', views.admin_logout, name='admin_logout'),

path('admin/users/', views.manage_users, name='manage_users'),
path('admin/users/add/', views.add_user, name='add_user'),
path('admin/users/edit/<int:id>/', views.edit_user, name='edit_user'),
path('admin/users/delete/<int:id>/', views.delete_user, name='delete_user'),


path('admin/organizers/', views.manage_organizers, name='manage_organizers'),
path('admin/organizers/add/', views.add_organizer, name='add_organizer'),
path('admin/organizers/edit/<int:id>/', views.edit_organizer, name='edit_organizer'),
path('admin/organizers/delete/<int:id>/', views.delete_organizer, name='delete_organizer'),

path('admin/events/', views.manage_events, name='manage_events'),
path('admin/events/edit/<int:id>/', views.admin_edit_event, name='admin_edit_event'),
path('admin/events/delete/<int:id>/', views.admin_delete_event, name='admin_delete_event'),


path('admin/media/', views.manage_media, name='manage_media'),
path('admin/media/add/', views.admin_add_media, name='admin_add_media'),
path('admin/media/edit/image/<int:id>/', views.admin_edit_image, name='admin_edit_image'),
path('admin/media/edit/video/<int:id>/', views.admin_edit_video, name='admin_edit_video'),
path('admin/media/delete/image/<int:id>/', views.admin_delete_image, name='admin_delete_image'),
path('admin/media/delete/video/<int:id>/', views.admin_delete_video, name='admin_delete_video'),

path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),


]


