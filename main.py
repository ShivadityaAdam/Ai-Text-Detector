from fastapi import FastAPI, File, UploadFile, HTTPException
import easyocr
import torch
import numpy as np
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import re
import io

app = FastAPI()


reader = easyocr.Reader(['en'])


device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_id)
model = GPT2LMHeadModel.from_pretrained(model_id).to(device)
model.eval()

def calculate_perplexity(text):
    """Calculates how 'predictable' the text is to an AI model."""
    encodings = tokenizer(text, return_tensors="pt")
    input_ids = encodings.input_ids.to(device)
    
    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
        loss = outputs.loss
        perplexity = torch.exp(loss)
    
    return perplexity.item()

def calculate_burstiness(text):
    """Calculates the variance in sentence length (Humans have high burstiness)."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 2]
    
    if len(sentences) < 2:
        return 0.0
    
    lengths = [len(s.split()) for s in sentences]
    variance = np.var(lengths)
    return float(variance)

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
   
    image_data = await file.read()
    results = reader.readtext(image_data, detail=0)
    full_text = " ".join(results)

    if len(full_text.split()) < 10:
        raise HTTPException(status_code=400, detail="Text too short for accurate detection (min 10 words)")


    ppl = calculate_perplexity(full_text)
    burst = calculate_burstiness(full_text)

    
    ai_probability = 0.0
    
    
    if ppl < 40: 
        ai_probability += 0.6
    elif ppl < 80: 
        ai_probability += 0.3
        
    if burst < 5:
        ai_probability += 0.3
    elif burst > 20: 
        ai_probability -= 0.2

    final_score = max(0.0, min(0.99, ai_probability))

    return {
        "text_preview": full_text[:200] + "...",
        "metrics": {
            "perplexity": round(ppl, 2),
            "burstiness": round(burst, 2)
        },
        "ai_score": round(final_score, 4),
        "verdict": "Likely AI" if final_score > 0.6 else "Likely Human"
    }
