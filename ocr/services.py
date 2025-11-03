import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import List
import re

class OCRService:
    """Extract text from images using Tesseract"""
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from image"""
        try:
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            text = pytesseract.image_to_string(thresh)
            return text.strip()
        except Exception as e:
            raise Exception(f"OCR Error: {str(e)}")
    
    def extract_ingredients(self, text: str) -> List[str]:
        """Parse text to extract ingredients"""
        ingredients_match = re.search(
            r'ingredients[:\s]+(.+?)(?:nutrition|allergen|warning|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if ingredients_match:
            ingredients_text = ingredients_match.group(1)
        else:
            ingredients_text = text
        
        ingredients = re.split(r'[,;|\n]+', ingredients_text)
        cleaned = []
        
        for ing in ingredients:
            ing = re.sub(r'\([^)]*\)', '', ing)
            ing = ' '.join(ing.split()).strip('.,;:- ')
            if ing and len(ing) > 2:
                cleaned.append(ing)
        
        return cleaned
