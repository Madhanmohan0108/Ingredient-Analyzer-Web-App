from django.db import models
import uuid

class UploadedImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Image {self.id}"

class OCRResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.OneToOneField(UploadedImage, on_delete=models.CASCADE)
    raw_text = models.TextField()
    extracted_ingredients = models.JSONField(default=list)
    confidence = models.FloatField(default=0.0)
    processing_time = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"OCR Result for {self.image.id}"
