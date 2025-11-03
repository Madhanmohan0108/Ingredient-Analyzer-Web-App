from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import time
import os

from ocr.models import UploadedImage, OCRResult
from ocr.services import OCRService
from ingredient_analysis.models import AnalysisResult
from ingredient_analysis.classifier import SafetyChecker
from ingredient_analysis.brand_matcher import BrandMatcher
from ingredient_analysis.category_detector import CategoryDetector

def home(request):
    """Render home page"""
    return render(request, 'index.html')

@csrf_exempt
@require_http_methods(["POST"])
def analyze(request):
    """Main analysis endpoint"""
    try:
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image provided'}, status=400)
        
        image_file = request.FILES['image']
        
        if image_file.size > 10 * 1024 * 1024:
            return JsonResponse({'error': 'File too large. Maximum 10MB.'}, status=400)
        
        # Create image record
        uploaded_image = UploadedImage.objects.create(image=image_file)
        
        # OCR Extraction
        ocr_service = OCRService()
        raw_text = ocr_service.extract_text(uploaded_image.image.path, preprocess=True)
        extracted_ingredients = ocr_service.extract_ingredients(raw_text)
        ocr_confidence = ocr_service.get_confidence_score(uploaded_image.image.path)
        
        # Create OCR result
        ocr_result = OCRResult.objects.create(
            image=uploaded_image,
            raw_text=raw_text,
            extracted_ingredients=extracted_ingredients,
            confidence=ocr_confidence,
            processing_time=1.0
        )
        
        # Safety Checking
        safety_checker = SafetyChecker()
        user_conditions = request.POST.getlist('conditions[]', [])
        unsafe_raw = safety_checker.check_safety(raw_text, user_conditions)
        
        # Enrich with ingredient info
        unsafe_ingredients = []
        for ingredient, effect in unsafe_raw:
            unsafe_ingredients.append({
                'ingredient': ingredient,
                'effect': effect,
                'definition': safety_checker.fetch_wikipedia_definition(ingredient),
                'safety': safety_checker._get_safety_rating(ingredient),
            })
        
        # Brand Identification
        brand_matcher = BrandMatcher()
        brand_result = brand_matcher.identify_brand(extracted_ingredients)
        
        # Category Detection
        category_detector = CategoryDetector()
        category_result = category_detector.detect_category(extracted_ingredients)
        
        # Create analysis result
        analysis = AnalysisResult.objects.create(
            ocr_result=ocr_result,
            unsafe_ingredients=unsafe_ingredients,
            health_conditions=user_conditions,
            identified_brand=brand_result['brand'],
            product_category=category_result['category'],
            confidence_score=brand_result['confidence'],
            recommendations="Product analysis complete."
        )
        
        return JsonResponse({
            'status': 'success',
            'analysis_id': str(analysis.id),
            'extracted_text': raw_text,
            'ingredients': extracted_ingredients,
            'unsafe_ingredients': unsafe_ingredients,
            'identified_brand': {
                'name': brand_result['brand'],
                'product_name': brand_result['product_name'],
                'confidence': brand_result['confidence']
            },
            'product_category': category_result['category'],
            'overall_confidence': (brand_result['confidence'] + (category_result['confidence'] * 100)) / 2,
            'ocr_confidence': ocr_confidence
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
