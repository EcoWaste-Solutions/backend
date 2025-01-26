import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from fastapi import File, UploadFile
import shutil

from datetime import datetime

from fastapi import Form

from typing import List

from config import settings



import base64
import requests

# Replace with your OpenAI API key
# api_key = "YOUR_OPENAI_API_KEY"
api_key = settings.api_key
# Replace with the image path you want to extract text from
prompt = """You are an expert in waste management and recycling. Analyze this image and provide:
        1. The type of waste (e.g., plastic, paper, glass, metal, organic)
        2. An estimate of the quantity or amount (in kg or liters)
        3. Your confidence level in this assessment (as a percentage)
        4. Any other relevant information or observations
        
        Respond in JSON format like this:
        {
          "wasteType": "type of waste. e.g., plastic, paper, glass, metal, organic(only type seperated by comma)",
          "quantity": "estimated quantity. e.g., 5 , 10 (only digits)",
          "unit": "unit of quantity. e.g., kg, liters",
          "confidence": confidence level as a number between 0 and 1
          "categuryPercentage": "percentage of waste type in the image. e.g., 50, 30 (only digits)",
          "other": "any other relevant information"
        }"""
def encode_image(image_path):
    """
    Encodes an image file to base64 string
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_text(image_data):
    """
    Extracts text from an image using OpenAI Vision
    """
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_data}"},
                    },
                ],
            }
        ],
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    response_data = response.json()
    if "choices" in response_data and len(response_data["choices"]) > 0:
        return response_data["choices"][0]["message"]["content"].strip()
    else:
        return "Could not extract text from image."


# Encode the image to base64

# Print the extracted text
def parse_image_details(extracted_text: str) -> dict:
    # Example parsing logic; this could be more advanced depending on the format of the extracted text
    lines = extracted_text.split("\n")

    wasteType = ""
    quantity = ""
    unit = ""
    confidence = ""
    other = ""
    categoryPercentage = ""
    for line in lines:
        if "wasteType" in line:
            wasteType = line.split(":")[1].strip().strip('",')
        if "quantity" in line:
            quantity = line.split(":")[1].strip().strip('",')
        if "unit" in line:
            unit = line.split(":")[1].strip().strip('",')
        if "confidence" in line:
            confidence = line.split(":")[1].strip().strip('",')
        if "other" in line:
            other = line.split(":")[1].strip().strip('",')
        if "categuryPercentage" in line:
            categoryPercentage = line.split(":")[1].strip().strip('",')

        
    
    return {
        "wasteType": [x.strip() for x in wasteType.split(",")],
        "quantity": int(quantity),
        "unit": unit,
        "confidence": confidence,
        "other": other,
        "categoryPercentage": [int(x) for x in categoryPercentage.split(",")]
    }


def process_image(image_data):
   
    extracted_text = extract_text(image_data)
    return parse_image_details(extracted_text)



