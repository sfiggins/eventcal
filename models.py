from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from django.contrib.localflavor.us.models import USStateField

class Contact(models.Model):
    """ An Event or Group Contact Person """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(blank=True, null=True)
    phone = models.PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    class Admin:
        pass

class Category(models.Model):
    """ Used to categorize events. """
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Admin:
        pass

class Location(models.Model):
    """ A city or place name. """
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=40, default="Lawrence")
    state = USStateField(default="KS")
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    directions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Admin:
        pass

class EventManager(models.Manager):
    def create_event(self, summary, user):
        new_event = self.model(summary=summary, created_by=user)
        new_event.save()
        return new_event

class Event(models.Model):
    """ An activity or happening """
    summary = models.CharField(max_length=200) 
    date_start = models.DateTimeField('start time')
    date_end = models.DateTimeField('end time', blank=True, null=True)
    description = models.TextField('event details', blank=True, null=True)
    publish = models.BooleanField(default=False)
    eventlink = models.URLField('event link', blank=True, null=True)

    # Information about the object
    created = models.DateField(editable=False)
    updated = models.DateTimeField(editable=False)
    created_by= models.ForeignKey(User)

    # Relational fields
    contacts = models.ManyToManyField(Contact)
    categories = models.ManyToManyField(Category)
    location = models.ForeignKey(Location)

    # Custom manager for automatically filling in the User
    # Curtesy of the B-List:
    # http://www.b-list.org/weblog/2006/11/02/django-tips-auto-populated-fields
    objects=EventManager()
    
    def __str__(self):
        return self.summary

    def save(self):
        if not self.id:
            self.created = date.today()
        self.updated = datetime.today()
        super(Event, self).save()
        
    class Admin:
        pass

