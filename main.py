import os
import io
import math
import torch
import numpy as np
import easyocr
from PIL import Image, ImageOps, ImageFilter
from fastapi import FastAPI, UploadFile, File, HTTPException
from supabase import create_client, Client
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from fpdf import FPDF

app = FastAPI()

# --- CONFIGURATION ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- MODEL LOADING (AI DETECTION & OCR) ---
# GPT-2 is the industry standard for calculating Perplexity in AI detection
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2").to(device)
reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())

# --- HELPER FUNCTIONS ---

def calculate_perplexity(text):
    """Calculates how 'predictable' the text is. Lower = More likely AI."""
    encodings = tokenizer(text, return_tensors="pt")
    max_length = model.config.n_positions
    stride = 512
    
    seq_len = encodings.input_ids.size(1)
    nlls = []
    for begin_loc in range(0, seq_len, stride):
        end_loc = min(begin_loc + max_length, seq_len)
        trg_len = end_loc - begin_loc
        input_ids = encodings.input_ids[:, begin_loc:end_loc].to(device)
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            neg_log_likelihood = outputs.loss * trg_len

        nlls.append(neg_log_likelihood)

    perplexity = torch.exp(torch.stack(nlls).sum() / seq_len)
    return float(perplexity)

def calculate_burstiness(text):
    """Calculates variance in sentence length. Lower = More likely AI."""
    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 5]
    if len(sentences) < 2: return 0
    lengths = [len(s.split()) for s in sentences]
    variance = np.var(lengths)
    return float(variance)

def preprocess_image(image_bytes):
    """Enhances image quality for better OCR accuracy."""
    img = Image.open(io.BytesIO(image_bytes))
    img = ImageOps.grayscale(img)
    img = img.filter(ImageFilter.SHARPEN)
    return np.array(img)

# --- API ENDPOINTS ---

@app.post("/scan")
async def scan_content(file: UploadFile = File(...)):
    # 1. Image OCR or Text Read
    contents = await file.read()
    if file.content_type.startswith("image/"):
        processed_img = preprocess_image(contents)
        ocr_result = reader.readtext(processed_img, detail=0)
        text = " ".join(ocr_result)
    else:
        text = contents.decode("utf-8")

    if len(text.split()) < 10:
        raise HTTPException(status_code=400, detail="Text too short for reliable detection.")

    # 2. Advanced Analysis
    ppl = calculate_perplexity(text)
    burst = calculate_burstiness(text)

    # 3. Hybrid Scoring (Tuned thresholds)
    # AI usually has PPL < 60 and Burstiness < 20
    ai_prob = 0
    if ppl < 60: ai_prob += 0.6
    if burst < 20: ai_prob += 0.3
    ai_prob = min(ai_prob + (max(0, 40 - ppl) * 0.01), 0.99) # Extra weight for very low PPL

    # 4. Save to Supabase
    data = {"text": text, "ai_score": ai_prob, "perplexity": ppl, "burstiness": burst}
    db_res = supabase.table("scans").insert(data).execute()

    return {
        "score": ai_prob,
        "perplexity": round(ppl, 2),
        "burstiness": round(burst, 2),
        "id": db_res.data[0]['id']
    }

@app.get("/report/{scan_id}")
async def get_report(scan_id: int):
    res = supabase.table("scans").select("*").eq("id", scan_id).execute()
    if not res.data: raise HTTPException(status_code=404)
    
    scan = res.data[0]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "AI Content Forensic Analysis", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"AI Probability: {round(scan['ai_score']*100, 2)}%", ln=True)
    pdf.cell(200, 10, f"Perplexity (Randomness): {scan['perplexity']}", ln=True)
    pdf.cell(200, 10, f"Burstiness (Rhythm): {scan['burstiness']}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Source Text:\n{scan['text'][:500]}...")
    
    return io.BytesIO(pdf.output(dest='S'))
