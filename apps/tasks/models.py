from django.db import models
from apps.accounts.models import Account, Team

PRIORITY = (
    (1, 'Low'),
    (2, 'Medium'),
    (3, 'High'),
    (4, 'Urgent')
)

STATUS = (
    (1, 'New'),
    (2, 'Process'),
    (3, 'Completed'),
    (4, 'Deleted')
)


class Task(models.Model):
    title = models.CharField(max_length=222)
    description = models.TextField()
    priority = models.IntegerField(choices=PRIORITY)
    status = models.IntegerField(choices=STATUS)
    supervisor = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    deadline = models.DateField()
    type = models.CharField(max_length=221, null=True)
    is_deleted = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SendTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver_task', null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='receiver_team', null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

