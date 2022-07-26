from django.db import models
from apps.accounts.models import Account

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


class Todo(models.Model):
    title = models.CharField(max_length=222)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.TextField()
    priority = models.IntegerField(choices=PRIORITY, default=1)
    status = models.IntegerField(choices=STATUS, default=1)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
