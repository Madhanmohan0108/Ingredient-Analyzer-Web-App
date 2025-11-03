from typing import List, Dict

class CategoryDetector:
    """Detect product category from ingredients"""
    
    def __init__(self):
        self.category_signatures = {
            'TOOTHPASTE': {
                'indicators': ['sodium fluoride', 'hydrated silica'],
                'confidence': 0.9
            },
            'SHAMPOO': {
                'indicators': ['sodium laureth sulfate', 'cocamidopropyl'],
                'confidence': 0.85
            },
            'FACE_MOISTURIZER': {
                'indicators': ['hyaluronic acid', 'ceramides'],
                'confidence': 0.80
            },
            'SUNSCREEN': {
                'indicators': ['zinc oxide', 'titanium dioxide'],
                'confidence': 0.90
            },
        }
    
    def detect_category(self, ingredients: List[str]) -> Dict:
        """Detect product category"""
        ingredient_lower = [ing.lower() for ing in ingredients]
        
        best_category = None
        best_confidence = 0
        
        for category, data in self.category_signatures.items():
            matches = sum(
                1 for indicator in data['indicators']
                if any(indicator in ing for ing in ingredient_lower)
            )
            
            if matches > 0:
                confidence = (matches / len(data['indicators'])) * data['confidence']
                
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_category = category
        
        return {
            'category': best_category or 'UNKNOWN',
            'confidence': min(best_confidence, 1.0),
        }
