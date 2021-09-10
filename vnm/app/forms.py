#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from django import forms
from app.models import Actor

class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        exclude = []

    zip = forms.FileField(required=False)