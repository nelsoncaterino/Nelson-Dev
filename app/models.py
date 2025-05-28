from django.db import models

class IPVisit(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    user_agent = models.TextField(blank=True, null=True)
    is_bot = models.BooleanField(default=False)
    
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    isp = models.CharField(max_length=100, blank=True, null=True)
    
    os_type = models.CharField(max_length=50, blank=True, null=True)
    browser = models.CharField(max_length=50, blank=True, null=True)
    device_type = models.CharField(max_length=50, blank=True, null=True)
    
    session_id = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    
    duration_seconds = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.timestamp}"
