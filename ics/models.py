from django.db import models
from django.urls import reverse
import os


class ics_part(models.Model):
    part_num = models.TextField()
    part_description = models.TextField()
    ea = models.IntegerField(default=0)

class ics_inout(models.Model):
    inout_id = models.ForeignKey(ics_part, on_delete=models.CASCADE)
    part_num = models.TextField(null=True)
    project_name = models.TextField(null=True)
    inout = models.BooleanField(null=True)
    ea = models.IntegerField(null=True)
    ics_update = models.DateField(null=True, blank=False)
    user = models.TextField(null=True)

    class Meta:
        ordering = ['-part_num']

    def __str__(self):
        return self.part_num

    def get_absolute_url(self):
        return reverse('ics:part_list')