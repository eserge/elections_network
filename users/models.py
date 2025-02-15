# -*- coding:utf-8 -*-
from django.db import models

from grakon.models import Profile
from locations.models import Location

ROLE_CHOICES = (
    ('observer', u'Наблюдатель'),
    ('voter', u'Избиратель'),
)
ROLE_TYPES = dict(ROLE_CHOICES)

class Role(models.Model):
    user = models.ForeignKey(Profile, related_name='roles')
    location = models.ForeignKey(Location)
    type = models.CharField(max_length=10, choices=ROLE_CHOICES)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'location', 'type')

    def type_name(self):
        return ROLE_TYPES[self.type]

class Contact(models.Model):
    user = models.ForeignKey(Profile, related_name='contacts')
    contact = models.ForeignKey(Profile, related_name='have_in_contacts')
    time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'contact')
