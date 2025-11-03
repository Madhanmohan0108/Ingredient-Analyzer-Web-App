import openpyxl
import wikipediaapi
from typing import List, Tuple, Dict
import os

class SafetyChecker:
    """Check ingredients for harmful substances"""
    
    def __init__(self, excel_path: str = "static_data/harmful_ingredients.xlsx"):
        try:
            if os.path.exists(excel_path):
                self.wb = openpyxl.load_workbook(excel_path)
                self.sheet = self.wb.active
            else:
                self.sheet = None
        except:
            self.sheet = None
        
        self.health_risks = {
            "Diabetes": ["sugar", "high fructose corn syrup", "aspartame", "maltodextrin"],
            "High Blood Pressure": ["salt", "sodium", "msg", "sodium nitrate"],
            "Thyroid Issues": ["soy", "fluoride", "bromate"],
            "Heart Disease": ["trans fat", "palm oil", "cholesterol"],
            "Kidney Disease": ["phosphate", "potassium chloride"],
            "Cancer Risks": ["aspartame", "sodium nitrate", "bht", "bpa"]
        }
    
    def fetch_wikipedia_definition(self, ingredient: str) -> str:
        """Fetch Wikipedia summary"""
        try:
            wiki = wikipediaapi.Wikipedia(
                user_agent="IngredientAnalyzer/1.0",
                language="en"
            )
            page = wiki.page(ingredient)
            if page.exists():
                return page.summary[:300]
            else:
                return "Definition not found."
        except:
            return "Could not fetch definition."
    
    def check_safety(self, product_text: str, user_conditions: List[str] = None) -> List[Tuple[str, str]]:
        """Check for unsafe ingredients"""
        if user_conditions is None:
            user_conditions = []
        
        unsafe = []
        
        if self.sheet:
            try:
                for row in self.sheet.iter_rows(min_row=2, values_only=True):
                    if row[0] is None:
                        continue
                    ingredient = row[0]
                    effect = row[1] if len(row) > 1 else ""
                    if ingredient and ingredient.lower() in product_text.lower():
                        unsafe.append((ingredient.lower(), effect or "Found in database"))
            except:
                pass
        
        for condition in user_conditions:
            if condition in self.health_risks:
                for restricted in self.health_risks[condition]:
                    if restricted.lower() in product_text.lower():
                        unsafe.append((restricted.lower(), f"Avoid due to {condition}"))
        
        return list(set(unsafe))
    
    def _get_safety_rating(self, ingredient: str) -> str:
        """Get safety level"""
        harmful_list = ["aspartame", "trans fat", "sodium nitrate", "bht", "bpa"]
        if any(h in ingredient.lower() for h in harmful_list):
            return "HARMFUL"
        
        for ingredients_list in self.health_risks.values():
            if any(ing in ingredient.lower() for ing in ingredients_list):
                return "MODERATE"
        
        return "SAFE"
