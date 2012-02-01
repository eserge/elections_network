# coding=utf8
from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField

from locations.models import Location

class Profile(models.Model):
    user = models.OneToOneField(User)
    lastname = models.CharField(verbose_name=u"Фамилия", max_length=80, default='', blank=True)
    firstname = models.CharField(verbose_name=u"Имя", max_length=80, default='', blank=True)
    patronymic = models.CharField(verbose_name=u"Отчество", max_length=80, default='', blank=True)
    show_real_name = models.BooleanField(verbose_name=u"Показывать настоящее имя", default=False)
    phone = models.CharField(verbose_name=u"Телефон", max_length=20, default='', blank=True)
    show_networks_profile = models.BooleanField(verbose_name=u"Показывать профиль из соцсетей", default=False)
    about = HTMLField(verbose_name=u"О себе", default='', blank=True)

PARTICIPATION_CHOICES = (
    ('observer', u'Наблюдатель'),
    ('voter', u'Избиратель'),
)
PARTICIPATION_TYPES = dict(PARTICIPATION_CHOICES)

class Participation(models.Model):
    user = models.ForeignKey(User)
    location = models.ForeignKey(Location)
    type = models.CharField(max_length=10, choices=PARTICIPATION_CHOICES)

    class Meta:
        unique_together = ('user', 'location', 'type')

    def type_name(self):
        return PARTICIPATION_TYPES[self.type]

class Contact(models.Model):
    user = models.ForeignKey(User, related_name='users')
    contact = models.ForeignKey(User, related_name='contacts')

    class Meta:
        unique_together = ('user', 'contact')

def create_profile(sender, **kwargs):
    if kwargs.get('created', False):
        profile = Profile()
        profile.user = kwargs['instance']
        profile.save()

models.signals.post_save.connect(create_profile, sender=User)
