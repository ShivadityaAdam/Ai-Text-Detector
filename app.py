import streamlit as st
import torch
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
import numpy as np

st.set_page_config(page_title="AI Text Sentinel", page_icon="🔍")

st.title("🔍 AI Text Detector")
st.markdown("Enter text below to check if it was likely written by a **Human** or an **AI**.")


@st.cache_resource
def load_models():
    # 1. Classification Model (RoBERTa fine-tuned for detector)
    # Note: Using a popular community model for AI detection
    classifier = pipeline("text-classification", model="roberta-base-openai-detector")
    
    # 2. Perplexity Model (GPT-2 is standard for calculating randomness)
    ppl_model = GPT2LMHeadModel.from_pretrained("gpt2")
    ppl_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    
    return classifier, ppl_model, ppl_tokenizer

classifier, ppl_model, ppl_tokenizer = load_models()


def get_perplexity(text):
    inputs = ppl_tokenizer(text, return_tensors="pt")
    if inputs['input_ids'].size(1) <= 1:
        return 0
    with torch.no_grad():
        outputs = ppl_model(**inputs, labels=inputs["input_ids"])
    return torch.exp(outputs.loss).item()


text_input = st.text_area("Paste text here (at least 20 words for accuracy):", height=250)

if st.button("Analyze Text"):
    if len(text_input.split()) < 10:
        st.warning("Please enter at least 10 words for a reliable analysis.")
    else:
        with st.spinner("Analyzing linguistic patterns..."):
            # Get Classification
            results = classifier(text_input[:512]) # RoBERTa limit is 512 tokens
            label = results[0]['label']
            score = results[0]['score']
            
            # Get Perplexity
            ppl_score = get_perplexity(text_input)
            
            # --- Display Results ---
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Prediction")
                if label == "Real":
                    st.success(f"Likely **Human Written** ({score:.1%})")
                else:
                    st.error(f"Likely **AI Generated** ({score:.1%})")
            
            with col2:
                st.subheader("Complexity Score")
                st.metric("Perplexity", f"{ppl_score:.2f}")
                st.caption("Higher = More Human-like randomness")

            # Insights
            st.info("**Insight:** AI usually has low perplexity (predictable words). "
                    "Humans have high 'burstiness' and varied word choice.")

# --- Sidebar info ---
st.sidebar.title("About Project")
st.sidebar.info(
    "This detector uses a RoBERTa-base classifier and GPT-2 Perplexity scoring. "
    "GitHub Portfolio."
)
