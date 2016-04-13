from django import forms
from models import Message

class send_message(forms.Form):
    message = forms.CharField(max_length=1000)
    date = forms.DateTimeField()
    class Meta:
        model = Message
