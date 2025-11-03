from django.contrib import admin
from .models import UploadedImage, OCRResult

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'uploaded_at', 'processed']
    list_filter = ['uploaded_at', 'processed']

@admin.register(OCRResult)
class OCRResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'confidence', 'created_at']
    list_filter = ['confidence', 'created_at']
