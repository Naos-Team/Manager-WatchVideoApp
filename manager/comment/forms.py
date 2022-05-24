from audioop import add
from dataclasses import field
from hashlib import new
from django import forms
from main.models import TblComment, TblUsers, TblVideo

class CommentForm(forms.ModelForm):
    class Meta:
        model = TblComment
        fields = '__all__'