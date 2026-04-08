# 🔍 AI Text Detector

A professional-grade system designed to identify machine-generated content through advanced linguistic analysis and Optical Character Recognition (OCR). This project features a distributed architecture utilizing **React, Node.js, Python, and Go** to provide a seamless end-to-end detection experience.

## 🛠️ System Architecture & Stack

This application is built using a specialized "best-tool-for-the-job" approach:

* **Frontend:** `React` + `TypeScript` + `Tailwind CSS`
    * *Role:* High-performance user dashboard with real-time scan interfaces and type-safe state management.
* **Authentication & Gateway:** `Node.js` + `Express` + `JWT`
    * *Role:* Secure user management, password hashing (Bcrypt), and API orchestration.
* **Database:** `PostgreSQL` + `Prisma ORM`
    * *Role:* Persistent relational data storage for user accounts and scan history.
* **Core AI Engine:** `Python` + `FastAPI` + `PyTorch`
    * *Role:* Image text extraction (EasyOCR) and NLP analysis using Perplexity and Burstiness metrics.
* **Reporting:** `Go (Golang)`
    * *Role:* High-speed, concurrent PDF generation for official integrity reports.

---

## 🧠 Detection Methodology

The **AI Text Detector** uses a dual-metric statistical approach to ensure high accuracy:

1.  **Perplexity:** Measures how "predictable" the text is. Lower perplexity scores indicate that the text follows the specific mathematical patterns typical of Large Language Models (LLMs).
2.  **Burstiness:** Analyzes the variation in sentence structure and length. Human writing naturally features "bursts" of varied sentence types, while AI output is often more uniform and robotic.

---

## 🏗️ Workflow

1.  **Input:** The user uploads a document image (JPG/PNG) via the dashboard.
2.  **OCR:** The **Python** engine extracts raw text from the image.
3.  **Analysis:** The text is processed through a **GPT-2** transformer model to calculate linguistic metrics.
4.  **Storage:** The **Node.js** gateway secures the result in a **PostgreSQL** database linked to the user's account.
5.  **Export:** The **Go** service generates a professional PDF report containing the final verdict and technical data.

---

## 🚀 Deployment & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-text-detector.git
```

### 2. Services Setup
* **Backend (Node.js):** `cd backend-auth && npm install`
* **AI Engine (Python):** `cd ai-python && pip install -r requirements.txt`
* **Reports (Go):** `cd report-service && go mod tidy`

### 3. Environment Variables
Ensure you have a `.env` file with the following:
* `DATABASE_URL`: Your PostgreSQL connection string.
* `JWT_SECRET`: A secure string for authentication.

---

## 🛡️ Security
* **Stateless Auth:** Secure session handling via JSON Web Tokens.
* **Data Integrity:** Relational mapping to ensure users can only access their own history.
* **Encryption:** Industry-standard password hashing with Bcrypt.


