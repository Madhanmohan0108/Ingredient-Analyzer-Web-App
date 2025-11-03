from django.db import models
import uuid

class AnalysisResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ocr_result = models.OneToOneField('ocr.OCRResult', on_delete=models.CASCADE)
    unsafe_ingredients = models.JSONField(default=list)
    health_conditions = models.JSONField(default=list)
    identified_brand = models.CharField(max_length=255, blank=True, null=True)
    product_category = models.CharField(max_length=100, blank=True, null=True)
    confidence_score = models.FloatField(default=0.0)
    recommendations = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analysis {self.id}"
