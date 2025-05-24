// src/context/CartContext.js
import React, { createContext, useState, useContext } from 'react';

// Tworzymy kontekst dla koszyka
export const CartContext = createContext();

// Tworzymy Providera, który będzie dostarczał stan koszyka do komponentów
export const CartProvider = ({ children }) => {
    const [cartItems, setCartItems] = useState([]); // Stan koszyka, lista produktów

    // Funkcja do dodawania produktu do koszyka
    const addToCart = (product) => {
        setCartItems((prevItems) => {
            const existingItem = prevItems.find((item) => item.id === product.id);
            if (existingItem) {
                // Jeśli produkt już istnieje, zwiększ jego ilość
                return prevItems.map((item) =>
                    item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
                );
            } else {
                // W przeciwnym razie dodaj nowy produkt z ilością 1
                return [...prevItems, { ...product, quantity: 1 }];
            }
        });
    };

    // Funkcja do usuwania produktu z koszyka (lub zmniejszania ilości)
    const removeFromCart = (productId) => {
        setCartItems((prevItems) => {
            const existingItem = prevItems.find((item) => item.id === productId);
            if (existingItem && existingItem.quantity > 1) {
                // Jeśli ilość > 1, zmniejsz ilość
                return prevItems.map((item) =>
                    item.id === productId ? { ...item, quantity: item.quantity - 1 } : item
                );
            } else {
                // W przeciwnym razie usuń produkt
                return prevItems.filter((item) => item.id !== productId);
            }
        });
    };

    // Funkcja do całkowitego usunięcia produktu z koszyka
    const clearProductFromCart = (productId) => {
        setCartItems((prevItems) => prevItems.filter((item) => item.id !== productId));
    };


    // Obliczanie całkowitej liczby przedmiotów i sumy koszyka
    const getTotalItems = () => {
        return cartItems.reduce((total, item) => total + item.quantity, 0);
    };

    const getTotalAmount = () => {
        return cartItems.reduce((total, item) => total + item.price * item.quantity, 0);
    };


    return (
        <CartContext.Provider value={{
            cartItems,
            addToCart,
            removeFromCart,
            clearProductFromCart,
            getTotalItems,
            getTotalAmount
        }}>
            {children}
        </CartContext.Provider>
    );
};

// Niestandardowy hook do łatwego używania kontekstu koszyka
export const useCart = () => {
    return useContext(CartContext);
};