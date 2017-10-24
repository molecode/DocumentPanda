from django.db import models


class Customer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    customer_id = models.IntegerField(unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['customer_id']

    def __str__(self):
        return '{} - {}'.format(self.customer_id, self.name)
