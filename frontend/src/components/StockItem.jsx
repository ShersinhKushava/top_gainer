import { useState } from 'react';

function StockItem({ stock, onUpdate, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState(stock.name);
  const [price, setPrice] = useState(stock.price);
  const [quantity, setQuantity] = useState(stock.quantity);

  const handleSave = () => {
    onUpdate(stock.id, { name, price: parseFloat(price), quantity: parseInt(quantity, 10) });
    setIsEditing(false);
  };

  return (
    <li>
      {isEditing ? (
        <>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
          <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} step="0.01" min="0" />
          <input type="number" value={quantity} onChange={(e) => setQuantity(e.target.value)} min="0" />
          <button onClick={handleSave}>Save</button>
          <button onClick={() => setIsEditing(false)}>Cancel</button>
        </>
      ) : (
        <>
          <span>{name} - Rs.{price.toFixed(2)} - Qty: {quantity}</span>
          <button onClick={() => setIsEditing(true)}>Edit</button>
          <button onClick={() => onDelete(stock.id)}>Delete</button>
        </>
      )}
    </li>
  );
}

export default StockItem;
