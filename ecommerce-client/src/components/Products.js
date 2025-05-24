import React from 'react';
import { useProducts } from '../hooks/useProducts';
import './Products.css';

const Products = () => {
    const { products, loading, error } = useProducts();

    if (loading) {
        return <div className="products-container">Ładowanie produktów...</div>;
    }

    if (error) {
        return <div className="products-container error">Błąd: {error.message}</div>;
    }

    return (
        <div className="products-container">
            <h2>Dostępne Produkty</h2>
            <div className="product-list">
                {products.map(product => (
                    <div key={product.id} className="product-card">
                        <h3>{product.name}</h3>
                        <p>{product.description}</p>
                        <p className="price">{product.price.toFixed(2)} PLN</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Products;