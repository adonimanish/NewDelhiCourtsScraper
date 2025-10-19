import cv2
import numpy as np
import os
import time
from PIL import Image

class CaptchaSolver:
    """Handles CAPTCHA solving using Gemini OCR with preprocessing"""
    
    def __init__(self):
        # Try to import Gemini modules
        try:
            from google import genai
            self.genai = genai
            # Initialize Gemini client with API key
            self.client = genai.Client(api_key="AIzaSyBvokbedL9AahypW7uesYP6G7eNwAfyvNU")
            self.use_gemini = True
            print("✅ Gemini OCR initialized")
        except Exception as e:
            print(f"⚠️ Gemini OCR not available: {e}")
            self.use_gemini = False
    
    def solve_with_gemini(self, image_path):
        """Use Gemini to solve the captcha"""
        try:
            # Load the image
            img = Image.open(image_path)
            
            # Model name
            model_name = "gemini-2.5-flash"
            
            # Prepare the prompt
            prompt = "What is the text clearly visible in this image? Only return the transcribed text."
            
            # Add wait time and retry logic
            max_attempts = 3
            wait_time = 15  # seconds
            
            for attempt in range(max_attempts):
                try:
                    print(f"📝 Attempt {attempt + 1}/{max_attempts}: Sending image to Gemini...")
                    time.sleep(wait_time)  # Wait before API call
                    
                    # Generate response using the client
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=[prompt, img]  # Pass both the text prompt and the image object
                    )
                    
                    # Add post-processing wait
                    time.sleep(5)  # Give extra time for response processing
                    
                    # Clean the text - remove all whitespace
                    cleaned_text = "".join(response.text.split())
                    
                    print(f"🔍 Raw response: {response.text}")
                    print(f"✨ Cleaned text: {cleaned_text}")
                    
                    if self.validate_captcha(cleaned_text):
                        print(f"✅ Got valid response after {attempt + 1} attempts")
                        return True, cleaned_text
                        
                    print(f"⚠️ Invalid response: {cleaned_text}, retrying...")
                    
                except Exception as e:
                    print(f"⚠️ Attempt {attempt + 1} failed: {e}")
                    if attempt < max_attempts - 1:
                        print(f"Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                    
            return False, None
            
        except FileNotFoundError:
            print(f"❌ Error: Image file not found at {image_path}")
            return False, None
        except Exception as e:
            print(f"❌ Gemini OCR error: {e}")
            return False, None
    
    def validate_captcha(self, text):
        """Validate if the extracted text looks like a valid captcha"""
        if text and len(text) >= 4 and len(text) <= 8 and text.isalnum():
            return True
        return False
    
    def solve_with_fallback(self, image_path):
        """Try Gemini first, then fallback to manual input if needed"""
        if self.use_gemini:
            success, captcha_text = self.solve_with_gemini(image_path)
            if success:
                print(f"✅ Gemini OCR detected: {captcha_text}")
                return captcha_text
        
        # Fallback to manual input
        print("❌ Gemini OCR failed or incorrect. Please enter captcha manually:")
        print(f"Check the captcha image at: {image_path}")
        captcha_text = input("Enter captcha: ").strip()
        
        return captcha_text

# Test function
if __name__ == "__main__":
    solver = CaptchaSolver()
    
    # Test with a sample image
    test_image = "captcha_sample.png"
    if os.path.exists(test_image):
        result = solver.solve_with_fallback(test_image)
        print(f"\n{'='*50}")
        print(f"Final captcha result: {result}")
        print(f"{'='*50}")
    else:
        print("Place a test captcha image named 'captcha_sample.png' to test")
