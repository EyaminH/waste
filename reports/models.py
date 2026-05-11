from django.db import models
from django.conf import settings

class WasteReport(models.fields.Field):
    pass # To be replaced

class WasteReport(models.Model):
    WASTE_TYPES = (
        ('ORGANIC', 'Organic'),
        ('PLASTIC', 'Plastic'),
        ('METAL', 'Metal'),
        ('E_WASTE', 'E-Waste'),
        ('HAZARDOUS', 'Hazardous'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COLLECTED', 'Collected'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    )

    location = models.CharField(max_length=500)
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPES)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    rejection_reason = models.TextField(blank=True, null=True)
    
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported_waste')
    collector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='collected_waste')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_waste_type_display()} at {self.location}"

class Feedback(models.Model):
    report = models.OneToOneField(WasteReport, on_delete=models.CASCADE, related_name='feedback')
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.report}"
