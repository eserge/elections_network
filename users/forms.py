# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from django import forms
from models import Profile


class EditProfileForm(ModelForm):
    phone = forms.CharField(required=False, 
                            help_text=u"Рекомендуемый формат: +74951234567")

    def __init__(self, *args, **kwargs):
        networks_profile = kwargs.get('instance').user.usermap_set.all()
        if not networks_profile:
            self.base_fields['show_networks_profile'].widget = self.base_fields['show_networks_profile'].hidden_widget()
        super(EditProfileForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = Profile
        exclude = ('user',)

    class Media:
        js = ('/static/libs/tiny_mce/tiny_mce.js',)
