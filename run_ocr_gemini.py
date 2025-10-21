import os
from google import genai
from PIL import Image

# --- Configuration ---
# The client automatically looks for the GEMINI_API_KEY environment variable.
try:
    client = genai.Client(api_key="YOUR_GEMINI_API_KEY")  ## here you have to give your api key
    ## when uploading just change your api kry to YOUR_GEMINI_API_KEY
except Exception as e:
    print("Error initializing Gemini client. Make sure your GEMINI_API_KEY environment variable is set correctly.")
    print(f"Details: {e}")
    exit()

# Set the path to your image file
IMAGE_PATH = "images/cap-3.png"
## Here you have to give your image path 

# The prompt is the instruction you give to the model about the image.
# You can ask it to describe the image, extract specific information, etc.
# For legitimate text extraction:
PROMPT = "What is the text clearly visible in this image? Only return the transcribed text."

# Use a multimodal model
MODEL_NAME = "gemini-2.5-flash" 

# --- Function to send image and get text ---
def generate_text_from_image(image_path: str, prompt: str):
    """
    Sends an image and a text prompt to the Gemini API and prints the response.
    """
    try:
        # 1. Load the image using Pillow
        img = Image.open(image_path)
        
        # 2. Call the API with the prompt and the image
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt, img]  # Pass both the text prompt and the image object
        )
        
        # 3. Print the model's text response
       
        
        cleaned_text = "".join(response.text.split())  # Remove all whitespace
       #  print(response.text) ## we dont need this 
        print(cleaned_text) ## we need this the actual text withut space 


    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except Exception as e:
        print(f"An error occurred during API call: {e}")

# --- Execute the function ---
if __name__ == "__main__":
    generate_text_from_image(IMAGE_PATH, PROMPT)
