# -=- encoding: utf-8 -=-
from django import forms
from django.db import models

import unicodedata

class SearchForm(forms.Form):
    value = forms.CharField(label='', max_length=20)
