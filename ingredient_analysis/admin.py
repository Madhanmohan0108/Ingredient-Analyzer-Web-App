from django.contrib import admin
from .models import AnalysisResult

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'identified_brand', 'product_category', 'confidence_score', 'created_at']
    list_filter = ['product_category', 'created_at']
    search_fields = ['identified_brand']
