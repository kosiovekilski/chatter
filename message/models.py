from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

class Message(models.Model):
    from_user = models.ForeignKey(User, related_name="sender")
    to_user = models.ForeignKey(User, related_name="resiver")
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message

    def get_date(self):
        return self.date

    def get_to_user(self):
        return self.to_user.username

    def get_user(self):
        return self.from_user.username
