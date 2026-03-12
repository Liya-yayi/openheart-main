from django.db import models

# Create your models here.


class Organizer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)   # simple password storage
    phone = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class Event(models.Model):

    
    EVENT_TYPE_CHOICES = [
        ('single', 'Single'),
        ('group', 'Group'),
    ]

    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES)

    max_participants = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    event_date = models.DateField()
    venue = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    result_published = models.BooleanField(default=False)
    first_place = models.CharField(max_length=200, null=True, blank=True)
    second_place = models.CharField(max_length=200, null=True, blank=True)
    third_place = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.title


class EventImage(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='event_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class ProgramRegistration(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancel_requested', 'Cancel Requested'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='active',null=True,blank=True)
    


    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.name} → {self.event.title}"
  

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/images/')
    title = models.CharField(max_length=200, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or "Gallery Image"
class GalleryVideo(models.Model):
    video = models.FileField(upload_to='gallery/videos/')
    title = models.CharField(max_length=200, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or "Gallery Video"

class mainadmin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)   # simple password storage
    phone = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name  
    
class GroupMember(models.Model):
    registration = models.ForeignKey(
        ProgramRegistration,
        on_delete=models.CASCADE,
        related_name='members'
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    college_id = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    year = models.PositiveIntegerField()   # e.g. 1,2,3,4

    def __str__(self):
        return f"{self.name} - {self.department} ({self.year} year)"


