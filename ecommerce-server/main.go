package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/google/uuid"
)

type Product struct {
	ID          string  `json:"id"`
	Name        string  `json:"name"`
	Description string  `json:"description"`
	Price       float64 `json:"price"`
}

type Payment struct {
	Amount       float64 `json:"amount"`
	Currency     string  `json:"currency"`
	CardNumber   string  `json:"cardNumber"`
	ExpiryDate   string  `json:"expiryDate"`
	Cvv          string  `json:"cvv"`
	CustomerName string  `json:"customerName"`
}

var products = []Product{
	{ID: uuid.New().String(), Name: "Zestaw klocków konstrukcyjnych", Description: "Duży zestaw klocków do budowania zamków i robotów.", Price: 129.99},
	{ID: uuid.New().String(), Name: "Pluszowy miś interaktywny", Description: "Miś, który mówi, śpiewa i reaguje na dotyk.", Price: 75.50},
	{ID: uuid.New().String(), Name: "Zdalnie sterowany dron", Description: "Mini dron dla początkujących z kamerą HD.", Price: 249.00},
	{ID: uuid.New().String(), Name: "Gra planszowa 'Poszukiwacze Skarbów'", Description: "Ekscytująca gra planszowa dla całej rodziny.", Price: 45.99},
	{ID: uuid.New().String(), Name: "Zestaw do malowania palcami", Description: "Bezpieczne farby i akcesoria dla małych artystów.", Price: 35.00},
}

func getProducts(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "http://localhost:3000")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(products)
}

func processPayment(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "http://localhost:3000")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	w.Header().Set("Content-Type", "application/json")

	var payment Payment
	err := json.NewDecoder(r.Body).Decode(&payment)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	log.Printf("Przetwarzanie płatności: kwota %.2f %s, Klient: %s, Karta: XXXX-XXXX-XXXX-%s\n",
		payment.Amount, payment.Currency, payment.CustomerName, payment.CardNumber[len(payment.CardNumber)-4:])

	time.Sleep(1 * time.Second)

	responseMsg := "Płatność pomyślna!"
	json.NewEncoder(w).Encode(map[string]string{"message": responseMsg})
}

func main() {
	http.HandleFunc("/api/products", getProducts)
	http.HandleFunc("/api/payments", processPayment)

	fmt.Println("Serwer Go uruchomiony na porcie :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
