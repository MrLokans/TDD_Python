from django.core.urlresolvers import reverse
from django.db import models


class List(models.Model):
    pass

    def get_absolute_url(self):
        # return URL for the vew with args
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    class Meta:
        ordering = ('id',)
        # text field unique in a single list
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text
