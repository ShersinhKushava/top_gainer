import StockItem from './StockItem';

function StockList({ stocks, onUpdate, onDelete }) {
  return (
    <ul>
      {stocks.map(stock => (
        <StockItem key={stock.id} stock={stock} onUpdate={onUpdate} onDelete={onDelete} />
      ))}
    </ul>
  );
}

export default StockList;
