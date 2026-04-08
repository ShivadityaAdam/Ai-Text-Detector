package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"github.com/jung-kurt/gofpdf"
)


type AnalysisData struct {
	Username   string  `json:"username"`
	Score      float64 `json:"ai_score"`
	Perplexity float64 `json:"perplexity"`
	Burstiness float64 `json:"burstiness"`
	Verdict    string  `json:"verdict"`
}

func generateReport(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, "Only POST allowed", http.StatusMethodNotAllowed)
		return
	}

	var data AnalysisData
	err := json.NewDecoder(r.Body).Decode(&data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	
	pdf := gofpdf.New("P", "mm", "A4", "")
	pdf.AddPage()
	

	pdf.SetFont("Arial", "B", 24)
	pdf.Cell(40, 10, "AI Shield Integrity Report")
	pdf.Ln(20)

	
	pdf.SetFont("Arial", "", 14)
	pdf.Cell(40, 10, fmt.Sprintf("User: %s", data.Username))
	pdf.Ln(10)
	pdf.Cell(40, 10, fmt.Sprintf("AI Probability Score: %.2f%%", data.Score*100))
	pdf.Ln(10)
	pdf.Cell(40, 10, fmt.Sprintf("Verdict: %s", data.Verdict))
	pdf.Ln(15)

	
	pdf.SetFont("Arial", "I", 12)
	pdf.Cell(40, 10, "Technical Metrics:")
	pdf.Ln(8)
	pdf.Cell(40, 10, fmt.Sprintf("- Perplexity: %.2f", data.Perplexity))
	pdf.Ln(8)
	pdf.Cell(40, 10, fmt.Sprintf("- Burstiness: %.2f", data.Burstiness))

	
	w.Header().Set("Content-Type", "application/pdf")
	pdf.Output(w)
}

func main() {
	http.HandleFunc("/generate", generateReport)
	fmt.Println("Go Report Service running on port 8080...")
	http.ListenAndServe(":8080", nil)
}
