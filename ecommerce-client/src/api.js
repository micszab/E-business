// src/api.js
const API_BASE_URL = 'http://localhost:8080/api'; // Upewnij się, że to odpowiada portowi serwera Go

export const fetchProducts = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/products`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Błąd podczas pobierania produktów:", error);
        throw error;
    }
};

export const processPayment = async (paymentData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/payments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(paymentData),
        });
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        // Serwer Go zwraca prosty tekst w odpowiedzi na sukces,
        // lub JSON z wiadomością o sukcesie.
        // Możemy go odczytać jako tekst, a potem ewentualnie parsować jako JSON jeśli jest.
        const responseText = await response.text();
        try {
            const jsonResponse = JSON.parse(responseText);
            return jsonResponse.message || "Płatność pomyślna (brak szczegółowej wiadomości)";
        } catch (e) {
            // Jeśli nie jest to JSON, zwróć po prostu tekst
            return responseText;
        }

    } catch (error) {
        console.error("Błąd podczas przetwarzania płatności:", error);
        throw error;
    }
};