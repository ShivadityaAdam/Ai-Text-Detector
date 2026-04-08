from fastapi import FastAPI, UploadFile, File
import easyocr
import io
from PIL import Image

app = FastAPI()
reader = easyocr.Reader(['en']) # Initialize OCR for English

# This would be your existing AI Detection Logic
def detect_ai_generated_text(text):
    # Placeholder for your specific detection script logic
    # e.g., probability = model.predict(text)
    length = len(text.split())
    probability = 0.85 if "automated" in text.lower() else 0.15 
    return {"score": probability, "verdict": "AI" if probability > 0.5 else "Human"}

@app.post("/analyze")
async def analyze_text(text: str):
    return detect_ai_generated_text(text)

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    # 1. Read the image file
    request_object_content = await file.read()
    img = Image.open(io.BytesIO(request_object_content))
    
    # 2. Run OCR
    # detail=0 returns just the text strings
    results = reader.readtext(request_object_content, detail=0)
    extracted_text = " ".join(results)
    
    # 3. Run AI Detection on the extracted text
    analysis = detect_ai_generated_text(extracted_text)
    
    return {
        "extracted_text": extracted_text,
        "analysis": analysis
    }
