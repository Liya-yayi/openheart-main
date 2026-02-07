import os
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.contrib import messages
import random
from django.core.mail import send_mail



def landing_page(request):
    return render(request, "landing.html")
# =========================
# ORGANIZER REGISTER
# =========================
def organizer_register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']

        # check if email already exists
        if Organizer.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('organizer_register')

        Organizer.objects.create(
            name=name,
            email=email,
            password=password,
            phone=phone
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect('organizer_login')

    return render(request, 'organizers/register.html')


# =========================
# ORGANIZER LOGIN
# =========================
def organizer_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            organizer = Organizer.objects.get(email=email, password=password)
            request.session['organizer_id'] = organizer.id
            request.session['organizer_name'] = organizer.name
            return redirect('organizer_dashboard')
        except Organizer.DoesNotExist:
            messages.error(request, "Invalid email or password")

    return render(request, 'organizers/login.html')


# =========================
# ORGANIZER DASHBOARD (TEST)
# =========================
def organizer_dashboard(request):
    if 'organizer_id' not in request.session:
        return redirect('organizer_login')

    return render(request, 'organizers/dashboard.html')


# =========================
# LOGOUT
# =========================
def organizer_logout(request):
    request.session.flush()
    return redirect('organizer_login')



# =========================
# ADD EVENT
# =========================
def add_event(request):
    if 'organizer_id' not in request.session:
        return redirect('organizer_login')

    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        event_type = request.POST['event_type']
        event_date = request.POST['event_date']
        venue = request.POST['venue']

        organizer = Organizer.objects.get(id=request.session['organizer_id'])
        max_participants = request.POST.get('max_participants')

        Event.objects.create(
            organizer=organizer,
            title=title,
            description=description,
            event_type=event_type,
            max_participants=max_participants if event_type == 'group' else None,
            event_date=event_date,
            venue=venue
        )

        messages.success(request, "Event added successfully")
        return redirect('view_events')

    return render(request, 'organizers/add_event.html')


# =========================
# VIEW EVENTS
# =========================
def view_events(request):
    if 'organizer_id' not in request.session:
        return redirect('organizer_login')

    organizer = Organizer.objects.get(id=request.session['organizer_id'])
    events = Event.objects.filter(organizer=organizer)

    return render(request, 'organizers/view_events.html', {'events': events})



# =========================
# ADD EVENT IMAGE
# =========================
def add_event_image(request, event_id):
    if 'organizer_id' not in request.session:
        return redirect('organizer_login')

    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        image = request.FILES['image']
        EventImage.objects.create(event=event, image=image)
        messages.success(request, "Image uploaded successfully")
        return redirect('view_events')

    return render(request, 'organizers/add_event_image.html', {'event': event})


def edit_event(request, event_id):
    if 'organizer_id' not in request.session:
        return redirect('organizer_login')

    event = get_object_or_404(
        Event,
        id=event_id,
        organizer_id=request.session['organizer_id']
    )

    if request.method == "POST":
        event.title = request.POST['title']
        event.description = request.POST['description']
        event.event_type = request.POST['event_type']
        event.event_date = request.POST['event_date']
        event.venue = request.POST['venue']
        event.save()

        messages.success(request, "Event updated successfully")
        return redirect('view_events')

    return render(request, 'organizers/edit_event.html', {'event': event})

def delete_event(request, event_id):
    if 'organizer_id' not in request.session:
        return redirect('organizer_login')

    event = get_object_or_404(
        Event,
        id=event_id,
        organizer_id=request.session['organizer_id']
    )

    if request.method == "POST":
        # 🔥 delete all image files
        for img in event.images.all():
            if img.image and os.path.isfile(img.image.path):
                os.remove(img.image.path)

        event.delete()
        messages.success(request, "Event deleted successfully")
        return redirect('view_events')

    return render(request, 'organizers/confirm_delete.html', {'event': event})


def edit_event_image(request, image_id):
    if 'organizer_id' not in request.session:
        return redirect('organizer_login')

    image = get_object_or_404(
        EventImage,
        id=image_id,
        event__organizer_id=request.session['organizer_id']
    )

    if request.method == "POST":
        if 'image' in request.FILES:
            # 🔥 delete old file
            if image.image and os.path.isfile(image.image.path):
                os.remove(image.image.path)

            image.image = request.FILES['image']
            image.save()

            messages.success(request, "Image updated successfully")
            return redirect('view_events')

    return render(request, 'organizers/edit_event_image.html', {'image': image})

def delete_event_image(request, image_id):
    if 'organizer_id' not in request.session:
        return redirect('organizer_login')

    image = get_object_or_404(
        EventImage,
        id=image_id,
        event__organizer_id=request.session['organizer_id']
    )

    if request.method == "POST":
        # 🔥 delete file from media folder
        if image.image and os.path.isfile(image.image.path):
            os.remove(image.image.path)

        # delete db record
        image.delete()

        messages.success(request, "Image deleted successfully")
        return redirect('view_events')

    return render(request, 'organizers/confirm_delete_image.html', {'image': image})

def add_gallery_image(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        title = request.POST.get('title')

        if image:
            GalleryImage.objects.create(
                image=image,
                title=title
            )
            return redirect('add_gallery_image')

    images = GalleryImage.objects.all().order_by('-uploaded_at')
    return render(request, 'organizers/add_gallary_image.html', {'images': images})

def edit_gallery_image(request, id):
    image_obj = get_object_or_404(GalleryImage, id=id)

    if request.method == "POST":
        image_obj.title = request.POST.get('title')

        if request.FILES.get('image'):
            image_obj.image = request.FILES.get('image')

        image_obj.save()
        return redirect('add_gallery_image')

    return render(request, 'organizers/edit_gallery_image.html', {'image': image_obj})

def delete_gallery_image(request, id):
    image_obj = get_object_or_404(GalleryImage, id=id)
    image_obj.delete()
    return redirect('add_gallery_image')


# -----------------------
# USER Module
# -----------------------


def user_register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('user_register')

        User.objects.create(
            name=name,
            email=email,
            password=password,
            phone=phone
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect('user_login')

    return render(request, 'users/register.html')

def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return redirect('user_dashboard')
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials")

    return render(request, 'users/login.html')

def user_logout(request):
    request.session.flush()
    return redirect('user_login')
def user_dashboard(request):
    if 'user_id' not in request.session:
        return redirect('user_login')

    # Fetch latest gallery images (for About section)
    gallery_images = GalleryImage.objects.order_by('-uploaded_at')[:4]

    # Fetch videos (if you plan to use them later)
    gallery_videos = GalleryVideo.objects.order_by('-uploaded_at')

    context = {
        'gallery_images': gallery_images,
        'gallery_videos': gallery_videos,
    }

    return render(request, 'users/dashboard.html', context)
def view_programs(request):
    if 'user_id' not in request.session:
        return redirect('user_login')

    events = Event.objects.all()
    return render(request, 'users/view_programs.html', {'events': events})

def register_program_form(request, event_id):
    if 'user_id' not in request.session:
        return redirect('user_login')

    event = get_object_or_404(Event, id=event_id)

    member_range = []
    if event.event_type == 'group' and event.max_participants:
        member_range = range(event.max_participants)

    return render(
        request,
        'users/register_program.html',
        {
            'event': event,
            'member_range': member_range
        }
    )


def register_program_submit(request, event_id):
    if 'user_id' not in request.session:
        return redirect('user_login')

    user = User.objects.get(id=request.session['user_id'])
    event = get_object_or_404(Event, id=event_id)

    # Prevent duplicate registration
    if ProgramRegistration.objects.filter(user=user, event=event).exists():
        messages.error(request, "Already registered")
        return redirect('view_programs')

    registration = ProgramRegistration.objects.create(
        user=user,
        event=event
    )

    if event.event_type == 'group':
        names = request.POST.getlist('member_name[]')
        emails = request.POST.getlist('member_email[]')
        phones = request.POST.getlist('member_phone[]')
        college_ids = request.POST.getlist('member_college_id[]')
        departments = request.POST.getlist('member_department[]')
        years = request.POST.getlist('member_year[]')

        for name, email, phone, college_id, department, year in zip(
            names, emails, phones, college_ids, departments, years
        ):
            GroupMember.objects.create(
                registration=registration,
                name=name,
                email=email,
                phone=phone,
                college_id=college_id,
                department=department,
                year=year
            )

    messages.success(request, "Registered successfully")
    return redirect('my_programs')

def my_programs(request):
    if 'user_id' not in request.session:
        return redirect('user_login')

    registrations = ProgramRegistration.objects.filter(
        user_id=request.session['user_id']
    )

    return render(
        request,
        'users/my_programs.html',
        {'registrations': registrations}
    )


def request_cancel_registration(request, reg_id):
    if 'user_id' not in request.session:
        return redirect('user_login')

    registration = get_object_or_404(
        ProgramRegistration,
        id=reg_id,
        user_id=request.session['user_id'],
        status='active'
    )

    registration.status = 'cancel_requested'
    registration.save()

    messages.success(request, "Cancellation request sent to organizer")
    return redirect('my_programs')


# ORGANIZER → VIEW REQUESTS
def cancel_requests(request):
    if 'organizer_id' not in request.session:
        return redirect('organizer_login')

    requests = ProgramRegistration.objects.filter(
        event__organizer_id=request.session['organizer_id'],
        status='cancel_requested'
    )

    return render(
        request,
        'organizers/cancel_requests.html',
        {'requests': requests}
    )


# ORGANIZER → APPROVE
def approve_cancel(request, reg_id):
    if 'organizer_id' not in request.session:
        return redirect('organizer_login')

    registration = get_object_or_404(
        ProgramRegistration,
        id=reg_id,
        event__organizer_id=request.session['organizer_id']
    )

    registration.status = 'cancelled'
    registration.save()

    messages.success(request, "Cancellation approved")
    return redirect('cancel_requests')


# ORGANIZER → REJECT
def reject_cancel(request, reg_id):
    if 'organizer_id' not in request.session:
        return redirect('organizer_login')

    registration = get_object_or_404(
        ProgramRegistration,
        id=reg_id,
        event__organizer_id=request.session['organizer_id']
    )

    registration.status = 'active'
    registration.save()

    messages.info(request, "Cancellation rejected")
    return redirect('cancel_requests')


def view_results(request):
    if 'user_id' not in request.session:
        return redirect('user_login')

    events = Event.objects.filter(result_published=True)
    return render(request, 'users/view_results.html', {'events': events})



def add_result(request, event_id):
    if 'organizer_id' not in request.session:
        return redirect('organizer_login')

    event = get_object_or_404(
        Event,
        id=event_id,
        organizer_id=request.session['organizer_id']
    )

    if request.method == 'POST':
        event.first_place = request.POST.get('first_place')
        event.second_place = request.POST.get('second_place')
        event.third_place = request.POST.get('third_place')
        event.result_published = True
        event.save()

        messages.success(request, "Result published successfully")
        return redirect('view_events')

    return render(request, 'organizers/add_result.html', {'event': event})

def add_media(request):
    if request.method == "POST":
        if 'image' in request.FILES:
            GalleryImage.objects.create(
                image=request.FILES['image']
            )

        if 'video' in request.FILES:
            GalleryVideo.objects.create(
                video=request.FILES['video']
            )

        return redirect('view_media')

    return render(request, 'organizers/add_media.html')

def view_media(request):
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    videos = GalleryVideo.objects.all().order_by('-uploaded_at')

    return render(request, 'organizers/view_media.html', {
        'images': images,
        'videos': videos
    })
    
def edit_image(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)

    if request.method == "POST":
        if 'image' in request.FILES:
            image.image = request.FILES['image']
            image.save()
        return redirect('view_media')

    return render(request, 'organizers/edit_image.html', {'image': image})

def edit_video(request, video_id):
    video = get_object_or_404(GalleryVideo, id=video_id)

    if request.method == "POST":
        if 'video' in request.FILES:
            video.video = request.FILES['video']
            video.save()
        return redirect('view_media')

    return render(request, 'organizers/edit_video.html', {'video': video})
def delete_image(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)
    image.delete()
    return redirect('view_media')

def delete_video(request, video_id):
    video = get_object_or_404(GalleryVideo, id=video_id)
    video.delete()
    return redirect('view_media')


# -----------------------------
#  ADMIN 
# -----------------------------


def admin_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            admin = Admin.objects.get(email=email, password=password)
            request.session['admin_id'] = admin.id
            request.session['admin_name'] = admin.name
            return redirect('admin_dashboard')
        except Admin.DoesNotExist:
            return render(request, 'admin/admin_login.html', {'error': 'Invalid credentials'})

    return render(request, 'admin/admin_login.html')

def admin_register(request):
    if request.method == "POST":
        Admin.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            password=request.POST['password'],
            phone=request.POST['phone']
        )
        return redirect('admin_login')

    return render(request, 'admin/admin_register.html')

def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_id'):
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def admin_dashboard(request):

    users_count = User.objects.count()
    organizers_count = Organizer.objects.count()
    events_count = Event.objects.count()
    media_count = GalleryImage.objects.count() + GalleryVideo.objects.count()

    context = {
        'users_count': users_count,
        'organizers_count': organizers_count,
        'events_count': events_count,
        'media_count': media_count,
    }

    return render(request, "admin/dashboard.html", context)


@admin_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin/manage_users.html', {'users': users})


@admin_required
def add_user(request):
    if request.method == "POST":
        User.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            password=request.POST['password'],
            phone=request.POST['phone']
        )
        return redirect('manage_users')

    return render(request, 'admin/add_user.html')


@admin_required
def edit_user(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.save()
        return redirect('manage_users')

    return render(request, 'admin/edit_user.html', {'user': user})


@admin_required
def delete_user(request, id):
    User.objects.filter(id=id).delete()
    return redirect('manage_users')


@admin_required
def manage_organizers(request):
    organizers = Organizer.objects.all()
    return render(request, 'admin/manage_organizers.html', {'organizers': organizers})
@admin_required
def add_organizer(request):
    if request.method == "POST":
        Organizer.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            password=request.POST['password'],
            phone=request.POST['phone']
        )
        return redirect('manage_organizers')

    return render(request, 'admin/add_organizer.html')

@admin_required
def edit_organizer(request, id):
    organizer = get_object_or_404(Organizer, id=id)

    if request.method == "POST":
        organizer.name = request.POST['name']
        organizer.email = request.POST['email']
        organizer.phone = request.POST['phone']

        # update password only if entered
        if request.POST.get('password'):
            organizer.password = request.POST['password']

        organizer.save()
        return redirect('manage_organizers')

    return render(request, 'admin/edit_organizer.html', {
        'organizer': organizer
    })


@admin_required
def delete_organizer(request, id):
    Organizer.objects.filter(id=id).delete()
    return redirect('manage_organizers')


@admin_required
def manage_events(request):
    events = Event.objects.all()
    return render(request, 'admin/manage_events.html', {'events': events})

@admin_required
def admin_edit_event(request, id):
    event = get_object_or_404(Event, id=id)
    organizers = Organizer.objects.all()

    if request.method == "POST":
        event.organizer_id = request.POST['organizer']
        event.title = request.POST['title']
        event.description = request.POST['description']
        event.category = request.POST['category']
        event.event_type = request.POST['event_type']
        event.max_participants = request.POST.get('max_participants') or None
        event.event_date = request.POST['event_date']
        event.venue = request.POST['venue']
        event.result_published = 'result_published' in request.POST

        event.save()
        return redirect('manage_events')

    return render(request, 'admin/edit_event.html', {
        'event': event,
        'organizers': organizers
    })


@admin_required
def admin_delete_event(request, id):
    Event.objects.filter(id=id).delete()
    return redirect('manage_events')


@admin_required
def manage_media(request):
    images = GalleryImage.objects.all()
    videos = GalleryVideo.objects.all()
    return render(request, 'admin/manage_media.html', {
        'images': images,
        'videos': videos
    })


@admin_required
def admin_add_media(request):
    if request.method == "POST":
        if 'image' in request.FILES:
            GalleryImage.objects.create(image=request.FILES['image'])

        if 'video' in request.FILES:
            GalleryVideo.objects.create(video=request.FILES['video'])

        return redirect('manage_media')

    return render(request, 'admin/add_media.html')


@admin_required
def admin_delete_image(request, id):
    GalleryImage.objects.filter(id=id).delete()
    return redirect('manage_media')

@admin_required
def admin_delete_video(request, id):
    GalleryVideo.objects.filter(id=id).delete()
    return redirect('manage_media')
@admin_required
def admin_edit_image(request, id):
    image = get_object_or_404(GalleryImage, id=id)

    if request.method == "POST":
        if 'image' in request.FILES:
            image.image = request.FILES['image']
            image.save()
        return redirect('manage_media')

    return render(request, 'admin/edit_image.html', {
        'image': image
    })
@admin_required
def admin_edit_video(request, id):
    video = get_object_or_404(GalleryVideo, id=id)

    if request.method == "POST":
        if 'video' in request.FILES:
            video.video = request.FILES['video']
            video.save()
        return redirect('manage_media')

    return render(request, 'admin/edit_video.html', {
        'video': video
    })


@admin_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')




def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = Organizer.objects.get(email=email)
        except Organizer.DoesNotExist:
            messages.error(request, "Email not registered")
            return redirect("forgot_password")

        otp = random.randint(100000, 999999)
        request.session['reset_email'] = email
        request.session['reset_otp'] = str(otp)

        send_mail(
            "Open Heart Password Reset OTP",
            f"Your OTP for password reset is: {otp}",
            "yourgmail@gmail.com",
            [email],
            fail_silently=False,
        )

        return redirect("verify_otp")

    return render(request, "organizers/forgot_password.html")


def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST.get("otp")
        session_otp = request.session.get("reset_otp")

        if user_otp == session_otp:
            return redirect("reset_password")
        else:
            messages.error(request, "Invalid OTP")
            return redirect("verify_otp")

    return render(request, "organizers/verify_otp.html")


def reset_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        email = request.session.get("reset_email")

        user = Organizer.objects.get(email=email)
        user.password = password   # (plain – later you can hash)
        user.save()

        messages.success(request, "Password reset successful")
        return redirect("organizer_login")

    return render(request, "organizers/reset_password.html")



def user_forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not registered")
            return redirect("user_forgot_password")

        otp = random.randint(100000, 999999)

        request.session['user_reset_email'] = email
        request.session['user_reset_otp'] = str(otp)

        send_mail(
            "Open Heart - Password Reset OTP",
            f"Your OTP for resetting password is: {otp}",
            "yourgmail@gmail.com",
            [email],
            fail_silently=False,
        )

        messages.success(request, "OTP sent to your email")
        return redirect("user_verify_otp")

    return render(request, "users/user_forgot_password.html")


def user_verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        session_otp = request.session.get("user_reset_otp")

        if otp == session_otp:
            return redirect("user_reset_password")
        else:
            messages.error(request, "Invalid OTP")
            return redirect("user_verify_otp")

    return render(request, "users/user_verify_otp.html")


def user_reset_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        email = request.session.get("user_reset_email")

        user = User.objects.get(email=email)
        user.password = password   # later you can hash it
        user.save()

        del request.session['user_reset_email']
        del request.session['user_reset_otp']

        messages.success(request, "Password reset successful")
        return redirect("user_login")

    return render(request, "users/user_reset_password.html")