from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField


LICENSE = (
    ('CIFS', 'CIFS'),
    ('NFS', 'NFS'),
    ('FCP', 'FCP'),
    ('iSCSI', 'iSCSI'),
    ('FlexClone', 'FlexClone'),
    ('SnapMirror', 'SnapMirror'),
    ('SnapRestore', 'SnapRestore'),
)

class installbase(models.Model):
    licensed = MultiSelectField(choices=LICENSE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    customer = models.CharField(max_length=100)
    production = models.BooleanField(default=True)
    installedat = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    osversion = models.CharField(max_length=100)
    serialnumber = models.TextField(max_length=100)
    hostname = models.TextField(max_length=100)
    ipslist = models.TextField()
    shelfmodel = models.TextField()
    disk = models.TextField()
    diskmodel = models.TextField()
    shelfemptyslot = models.TextField()
    slotinfo = models.TextField()
    installedate = models.DateField()
    warrantydate = models.DateField()
    engineername = models.CharField(max_length=100)
    controllereoa = models.DateField(null=True, blank=True)
    controllereos = models.DateField(null=True, blank=True)
    addlist = models.TextField()
    deleted = models.BooleanField(default=False)
    delete_date = models.DateTimeField(auto_now=True)
    sanswitch = models.BooleanField()
    sanswitchserial = models.CharField(max_length=100, null=True, blank=True)
    sanswitchmodel = models.CharField(max_length=30, null=True, blank=True)
    sanswitchhostname = models.TextField(null=True, blank=True)
    sanswitchport = models.IntegerField(null=True, blank=True)
    sanswitchportlicense = models.IntegerField(null=True, blank=True)
    sanswitchipaddress = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-installedate']

    def __str__(self):
        return self.hostname

    def get_absolute_url(self):
        return reverse('installbase:installbase_detail', args=[self.id])