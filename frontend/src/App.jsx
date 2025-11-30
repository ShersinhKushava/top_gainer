import { useState, useEffect } from 'react';
import axios from 'axios';
import StockList from './components/StockList';
import AddStock from './components/AddStock';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './components/Header';
import { Routes, Route } from 'react-router-dom';
import TopGainer from './components/TopGainer';

const API_BASE = 'http://localhost:8000/api';

function Stock({ stocks, addStock, updateStock, deleteStock }) {
  return (
    <>
      <h1 className="mb-4 text-center">Stock Management</h1>
      <AddStock onAdd={addStock} />
      <StockList stocks={stocks} onUpdate={updateStock} onDelete={deleteStock} />
    </>
  )
}

function Todos() {
  return (
    <div className="p-4 text-center">
      <h2>Todos Page</h2>
      <p>This page is under construction.</p>
    </div>
  )
}

function App() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetchStocks();
  }, []);

  const fetchStocks = async () => {
    const response = await axios.get(`${API_BASE}/stocks/`);
    setStocks(response.data);
  };

  const addStock = async (stock) => {
    const response = await axios.post(`${API_BASE}/stocks/`, stock);
    setStocks([...stocks, response.data]);
  };

  const updateStock = async (id, updatedStock) => {
    await axios.put(`${API_BASE}/stocks/${id}/`, updatedStock);
    fetchStocks();
  };

  const deleteStock = async (id) => {
    await axios.delete(`${API_BASE}/stocks/${id}/`);
    setStocks(stocks.filter(stock => stock.id !== id));
  };

  return (
    <div className="App container mt-4">
      <Header />
      <Routes>
        <Route path="/" element={<Stock stocks={stocks} addStock={addStock} updateStock={updateStock} deleteStock={deleteStock} />} />
        <Route path="/todos" element={<Todos />} />
        <Route path="Top-Gainer" element={<TopGainer />} />
      </Routes>
    </div>
  );
}

export default App;
