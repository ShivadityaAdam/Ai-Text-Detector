# AI Text Detector

A high-fidelity forensic platform designed to identify machine-generated content in text and images. By analyzing linguistic patterns—specifically **Perplexity** and **Burstiness**—the system provides a mathematical probability of AI involvement.

## 🔬 Scientific Methodology
This project utilizes two primary statistical markers to verify authenticity:
* **Perplexity:** Measures the "randomness" of text. Since LLMs predict the next most likely token, AI text often exhibits lower perplexity (high predictability).
* **Burstiness:** Analyzes the variance in sentence structure. Human writing is naturally "bursty," while AI tends toward a uniform rhythmic flatness.

## 🛠️ Architecture
- **AI Engine (Python):** A FastAPI core utilizing GPT-2 for linguistic scoring and EasyOCR for image text extraction.
- **Audit Service (Go):** A high-performance Fiber service dedicated to generating cryptographically stable PDF reports.
- **Frontend (React):** A modern dashboard built with Vite and Tailwind CSS for real-time forensic visualization.
- **Persistence (Supabase):** Managed PostgreSQL and Auth to ensure data integrity.

## 📂 Project Structure
```text
/                  # Python AI Engine & API Logic
├── frontend/      # React (Vite) User Interface
└── reports/       # Go Reporting & Audit Service
