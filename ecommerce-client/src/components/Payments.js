import React, { useState } from 'react';
import { usePayments } from '../hooks/usePayments';
import './Payments.css';

const Payments = () => {
    const { submitPayment, paymentStatus, paymentError, loadingPayment } = usePayments();

    const [formData, setFormData] = useState({
        amount: 100.00,
        currency: 'PLN',
        cardNumber: '',
        expiryDate: '',
        cvv: '',
        customerName: '',
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const success = await submitPayment(formData);
        if (success) {
            setFormData({
                amount: 100.00,
                currency: 'PLN',
                cardNumber: '',
                expiryDate: '',
                cvv: '',
                customerName: '',
            });
        }
    };

    return (
        <div className="payments-container">
            <h2>Płatność</h2>
            <form onSubmit={handleSubmit} className="payment-form">
                <div className="form-group">
                    <label htmlFor="amount">Kwota:</label>
                    <input
                        type="number"
                        id="amount"
                        name="amount"
                        value={formData.amount}
                        onChange={handleChange}
                        step="0.01"
                        readOnly
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="currency">Waluta:</label>
                    <input
                        type="text"
                        id="currency"
                        name="currency"
                        value={formData.currency}
                        onChange={handleChange}
                        readOnly
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="cardNumber">Numer karty:</label>
                    <input
                        type="text"
                        id="cardNumber"
                        name="cardNumber"
                        value={formData.cardNumber}
                        onChange={handleChange}
                        placeholder="XXXX XXXX XXXX XXXX"
                        required
                        maxLength="19"
                    />
                </div>
                <div className="form-group half-width">
                    <div>
                        <label htmlFor="expiryDate">Data ważności (MM/RR):</label>
                        <input
                            type="text"
                            id="expiryDate"
                            name="expiryDate"
                            value={formData.expiryDate}
                            onChange={handleChange}
                            placeholder="MM/RR"
                            required
                            maxLength="5"
                        />
                    </div>
                    <div>
                        <label htmlFor="cvv">CVV:</label>
                        <input
                            type="text"
                            id="cvv"
                            name="cvv"
                            value={formData.cvv}
                            onChange={handleChange}
                            placeholder="XXX"
                            required
                            maxLength="4"
                        />
                    </div>
                </div>
                <div className="form-group">
                    <label htmlFor="customerName">Imię i Nazwisko:</label>
                    <input
                        type="text"
                        id="customerName"
                        name="customerName"
                        value={formData.customerName}
                        onChange={handleChange}
                        required
                    />
                </div>
                <button type="submit" disabled={loadingPayment}>
                    {loadingPayment ? 'Przetwarzanie...' : 'Zapłać'}
                </button>
            </form>

            {paymentStatus && <p className="payment-message success">{paymentStatus}</p>}
            {paymentError && <p className="payment-message error">Błąd płatności: {paymentError}</p>}
        </div>
    );
};

export default Payments;