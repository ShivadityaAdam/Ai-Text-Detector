package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"strconv"

	"github.com/gofiber/fiber/v2"
	"github.com/jackc/pgx/v5"
	"github.com/jung-kurt/gofpdf"
)

func main() {
	app := fiber.New()

	
	dbURL := os.Getenv("DATABASE_URL")
	conn, err := pgx.Connect(context.Background(), dbURL)
	if err != nil {
		log.Fatalf("Unable to connect to Supabase: %v\n", err)
	}
	defer conn.Close(context.Background())

	
	app.Get("/generate/:id", func(c *fiber.Ctx) error {
		scanID := c.Params("id")
		
		
		var text string
		var score float64
		var ppl float64
		
		query := "SELECT text, ai_score, perplexity FROM scans WHERE id=$1"
		err := conn.QueryRow(context.Background(), query, scanID).Scan(&text, &score, &ppl)
		if err != nil {
			return c.Status(404).JSON(fiber.Map{"error": "Scan record not found"})
		}

		
		pdf := gofpdf.New("P", "mm", "A4", "")
		pdf.AddPage()
		
		
		pdf.SetFont("Arial", "B", 16)
		pdf.Cell(40, 10, "Official AI Detection Audit")
		pdf.Ln(12)

		
		pdf.SetFont("Arial", "", 12)
		pdf.Cell(40, 10, fmt.Sprintf("Report ID: %s", scanID))
		pdf.Ln(8)
		pdf.Cell(40, 10, fmt.Sprintf("AI Probability: %.2f%%", score*100))
		pdf.Ln(8)
		pdf.Cell(40, 10, fmt.Sprintf("Linguistic Perplexity: %.2f", ppl))
		pdf.Ln(15)

		
		pdf.SetFont("Arial", "I", 10)
		pdf.MultiCell(0, 5, fmt.Sprintf("Analyzed Text Sample:\n%s", text), "1", "L", false)

		
		c.Set("Content-Type", "application/pdf")
		c.Set("Content-Disposition", fmt.Sprintf("attachment; filename=audit_%s.pdf", scanID))
		
		return pdf.Output(c.Response().BodyWriter())
	})

	log.Fatal(app.Listen(":3000"))
}
