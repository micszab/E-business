// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Products from './components/Products';
import Cart from './components/Cart';
import Payments from './components/Payments'; // Nadal importujemy Payments
import { CartProvider, useCart } from './context/CartContext';
import './App.css';

// Komponent Navigation, aby wyświetlać liczbę przedmiotów w koszyku
const Navigation = () => {
    const { getTotalItems } = useCart();
    return (
        <nav className="App-nav">
            <Link to="/">Produkty</Link>
            <Link to="/cart">
                Koszyk ({getTotalItems()})
            </Link>
            {/* Opcjonalnie: link do płatności w nawigacji, jeśli chcesz, żeby użytkownik mógł tam przejść bezpośrednio */}
            {/* <Link to="/payments">Płatność</Link> */}
        </nav>
    );
};

function App() {
    return (
        <Router>
            <CartProvider>
                <div className="App">
                    <header className="App-header">
                        <h1>Sklep</h1>
                        <Navigation />
                    </header>
                    <main>
                        <Routes>
                            <Route path="/" element={<Products />} />
                            <Route path="/cart" element={<Cart />} />
                            <Route path="/payments" element={<Payments />} /> {/* Teraz Płatności mają własną trasę */}
                        </Routes>
                        {/* Usunięto:
                        <hr />
                        <Payments />
                        */}
                    </main>
                </div>
            </CartProvider>
        </Router>
    );
}

export default App;