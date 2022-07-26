from django.db import models
from apps.accounts.models import Account, Team


class Notification(models.Model):
    title = models.CharField(max_length=222)
    description = models.TextField()
    user = models.ManyToManyField(Account)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Chat(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='chat_sender')
    receiver = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='chat_reciever')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.sender.email
