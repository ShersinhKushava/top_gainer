import { useState } from 'react';

function AddStock({ onAdd }) {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [quantity, setQuantity] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (name.trim() && price.trim() && quantity.trim()) {
      onAdd({ name, price: parseFloat(price), quantity: parseInt(quantity, 10) });
      setName('');
      setPrice('');
      setQuantity('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Price"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
        required
        step="0.01"
        min="0"
      />
      <input
        type="number"
        placeholder="Quantity"
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
        required
        min="0"
      />
      <button type="submit">Add Stock</button>
    </form>
  );
}

export default AddStock;
