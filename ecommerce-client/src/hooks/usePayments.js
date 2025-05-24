import { useState } from 'react';
import { processPayment } from '../api';

export const usePayments = () => {
    const [paymentStatus, setPaymentStatus] = useState(null); // Komunikat o sukcesie
    const [paymentError, setPaymentError] = useState(null);   // Komunikat o błędzie
    const [loadingPayment, setLoadingPayment] = useState(false); // Stan ładowania płatności

    const submitPayment = async (paymentData) => {
        setLoadingPayment(true);
        setPaymentStatus(null); // Resetuj statusy przed nowym żądaniem
        setPaymentError(null);
        try {
            const response = await processPayment(paymentData);
            setPaymentStatus(response);
            return true; // Wskazuje na sukces
        } catch (err) {
            setPaymentError(err.message);
            return false; // Wskazuje na błąd
        } finally {
            setLoadingPayment(false);
        }
    };

    return { submitPayment, paymentStatus, paymentError, loadingPayment };
};