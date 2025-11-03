from typing import List, Dict
from difflib import SequenceMatcher

class BrandMatcher:
    """Match ingredients to brands"""
    
    def __init__(self):
        self.brands_database = {
            'TOOTHPASTE': [
                {
                    'name': 'Colgate Total 12',
                    'brand': 'Colgate',
                    'key_ingredients': ['Sodium Fluoride', 'Hydrated Silica'],
                    'confidence_weight': 0.95
                },
                {
                    'name': 'Sensodyne Repair',
                    'brand': 'Sensodyne',
                    'key_ingredients': ['Potassium Nitrate', 'Sodium Fluoride'],
                    'confidence_weight': 0.96
                },
            ],
            'SHAMPOO': [
                {
                    'name': 'Pantene Pro-V',
                    'brand': 'Pantene',
                    'key_ingredients': ['Sodium Laureth Sulfate', 'Panthenol'],
                    'confidence_weight': 0.93
                },
            ],
        }
    
    def identify_brand(self, ingredients: List[str]) -> Dict:
        """Match ingredients to brand"""
        best_match = None
        best_score = 0
        
        for category, products in self.brands_database.items():
            for product in products:
                score = self._calculate_match_score(
                    ingredients,
                    product['key_ingredients']
                )
                
                if score > best_score:
                    best_score = score
                    best_match = product
        
        if best_match:
            return {
                'brand': best_match['brand'],
                'product_name': best_match['name'],
                'confidence': best_score * 100,
            }
        
        return {
            'brand': 'Unknown',
            'product_name': 'Generic Product',
            'confidence': 0,
        }
    
    def _calculate_match_score(self, detected: List[str], required: List[str]) -> float:
        """Calculate match score"""
        if not required:
            return 0.0
        
        matches = sum(
            1 for req in required
            if any(self._fuzzy_match(req.lower(), d.lower()) > 0.8 for d in detected)
        )
        
        return matches / len(required)
    
    def _fuzzy_match(self, str1: str, str2: str) -> float:
        """Calculate string similarity"""
        return SequenceMatcher(None, str1, str2).ratio()
