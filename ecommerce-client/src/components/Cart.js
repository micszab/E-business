// src/components/Cart.js
import React from 'react';
import { useCart } from '../context/CartContext';
import { useNavigate } from 'react-router-dom'; // Importujemy useNavigate
import './Cart.css';

const Cart = () => {
    const { cartItems, addToCart, removeFromCart, clearProductFromCart, getTotalAmount, getTotalItems } = useCart();
    const navigate = useNavigate(); // Inicjujemy useNavigate

    const handleCheckout = () => {
        // Logika przejścia do płatności
        if (cartItems.length > 0) {
            // Tutaj możesz przekazać dane o koszyku do komponentu płatności,
            // jeśli Payments będzie miało bardziej zaawansowaną logikę.
            // Na razie po prostu nawigujemy.
            navigate('/payments'); // Przejdź do trasy /payments
        } else {
            alert('Twój koszyk jest pusty!');
        }
    };

    return (
        <div className="cart-container">
            <h2>Twój Koszyk ({getTotalItems()} przedmiotów)</h2>
            {cartItems.length === 0 ? (
                <p className="empty-cart-message">Twój koszyk jest pusty.</p>
            ) : (
                <>
                    <div className="cart-items-list">
                        {cartItems.map((item) => (
                            <div key={item.id} className="cart-item-card">
                                <div className="item-details">
                                    <h3>{item.name}</h3>
                                    <p>Cena jednostkowa: {item.price.toFixed(2)} PLN</p>
                                </div>
                                <div className="item-quantity-controls">
                                    <button onClick={() => removeFromCart(item.id)}>-</button>
                                    <span>{item.quantity}</span>
                                    <button onClick={() => addToCart(item)}>+</button>
                                </div>
                                <div className="item-total">
                                    Total: {(item.price * item.quantity).toFixed(2)} PLN
                                </div>
                                <button
                                    className="remove-item-button"
                                    onClick={() => clearProductFromCart(item.id)}
                                >
                                    Usuń
                                </button>
                            </div>
                        ))}
                    </div>
                    <div className="cart-summary">
                        <h3>Całkowita wartość koszyka: {getTotalAmount().toFixed(2)} PLN</h3>
                        <button className="checkout-button" onClick={handleCheckout}> {/* Dodajemy onClick */}
                            Przejdź do płatności
                        </button>
                    </div>
                </>
            )}
        </div>
    );
};

export default Cart;