import React from 'react';
import Products from './components/Products';
import Payments from './components/Payments';
import './App.css';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>Sklep</h1>
            </header>
            <main>
                <Products />
                <hr />
                <Payments />
            </main>
        </div>
    );
}

export default App;