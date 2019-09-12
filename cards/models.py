from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='vibes/',
                              max_length=255, null=True, blank=True, default='/static/img/default.png')
    phone = models.CharField(max_length=20, blank=True, default='')
    email_confirmed = models.BooleanField(default=False)
    bio = models.TextField()


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


class Subject(models.Model):
    name = models.CharField(max_length=20)

    @classmethod
    def all_subjects(cls):
        return cls.objects.all()


class Card(models.Model):
    title = models.CharField(max_length=30)
    notes = models.TextField(max_length=300)
    # subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    # updated_on = models.DateField(auto_now_add=True null=True, blank=True)

    class Meta:
        ordering = ["-created_on"]

    @classmethod
    def all_cards(cls):
        return cls.objects.all()

    @classmethod
    def display_subject(cls, subject):
        return cls.objects.filter(subject=subject)

    @classmethod
    def fetch_cards_of_subject(cls, subject_id):
        return cls.objects.filter(subject__id=subject_id)

    @classmethod
    def search_by_subject(cls, search_term):
        return cls.objects.filter(subject__name__icontains=search_term)
