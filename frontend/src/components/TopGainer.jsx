import React, { useEffect, useState } from "react";
import axios from "axios";

const TopGainer = () => {
  const [allRows, setAllRows] = useState([]); // store historical rows
  const [selectedStock, setSelectedStock] = useState(null); // stock for modal

  // Fetch top gainers from Django API
  const fetchTopGainers = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/top-gainers/");

      // Validate array
      if (!Array.isArray(res.data)) {
        console.error("API did not return an array:", res.data);
        return;
      }

      // Ensure numeric fields
      const newRow = res.data.map((stock) => ({
        symbol: stock.symbol,
        LTP: Number(stock.LTP),
        open: Number(stock.open),
        previous_close: Number(stock.previous_close),
        "%change": Number(stock["%change"]),
        high: Number(stock.high),
        low: Number(stock.low),
        volume: Number(stock.volume),
      }));

      setAllRows((prev) => [...prev, newRow]);
    } catch (err) {
      console.error("Error fetching top gainers:", err);
    }
  };

  // Auto-refresh every 60 seconds
  useEffect(() => {
    fetchTopGainers();
    const interval = setInterval(fetchTopGainers, 60000);
    return () => clearInterval(interval);
  }, []);

  // Get background color based on previous row's LTP
  const getBgColor = (symbol, ltp, rowIndex) => {
    if (rowIndex === 0) return "white";
    const prevRow = allRows[rowIndex - 1];
    const prevStock = prevRow.find((s) => s.symbol === symbol);
    if (!prevStock) return "white";
    if (ltp > prevStock.LTP) return "#c6f6c6"; // green
    if (ltp < prevStock.LTP) return "#f6c6c6"; // red
    return "#c6d9f6"; // blue
  };

  // Get full history of a stock
  const getStockHistory = (symbol) => {
    return allRows
      .map((row) => row.find((s) => s.symbol === symbol))
      .filter(Boolean);
  };

  // Calculate averages
  const getAverages = (history) => {
    const avgLTP = history.reduce((sum, s) => sum + s.LTP, 0) / history.length;
    const avgVol = history.reduce((sum, s) => sum + s.volume, 0) / history.length;
    return { avgLTP, avgVol };
  };

  return (
    <div style={{ padding: "20px", background: "#eef2f7" }}>
      <button
        onClick={fetchTopGainers}
        style={{ padding: "10px 20px", marginBottom: "20px", cursor: "pointer" }}
      >
        🔄 Refresh (Add New Row)
      </button>

      {/* Display all rows */}
      <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
        {allRows.map((row, rowIndex) => (
          <div
            key={rowIndex}
            style={{
              display: "flex",
              gap: "10px",
              overflowX: "auto",
              paddingBottom: "5px",
            }}
          >
            {row.map((stock) => (
              <div
                key={`${stock.symbol}-${rowIndex}`}
                onClick={() => setSelectedStock(stock.symbol)}
                style={{
                  minWidth: "150px",
                  border: "1px solid #ccc",
                  padding: "10px",
                  background: getBgColor(stock.symbol, stock.LTP, rowIndex),
                  cursor: "pointer",
                  flexShrink: 0,
                }}
              >
                <div><b>{stock.symbol}</b></div>
                <div>LTP: {stock.LTP}</div>
                <div>Open: {stock.open}</div>
                <div>Prev: {stock.previous_close}</div>
                <div>%Chg: {stock["%change"]}</div>
                <div>High: {stock.high}</div>
                <div>Low: {stock.low}</div>
                <div>Vol: {stock.volume}</div>
              </div>
            ))}
          </div>
        ))}
      </div>

      {/* Modal for stock history */}
      {selectedStock && (
        <div
          onClick={() => setSelectedStock(null)}
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            background: "rgba(0,0,0,0.3)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 1000,
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              background: "#f7faff",
              padding: "20px",
              borderRadius: "8px",
              width: "350px",
              maxHeight: "400px",
              overflowY: "auto",
            }}
          >
            <h3>Stock History - {selectedStock}</h3>
            <p>Appeared in {getStockHistory(selectedStock).length} previous rows</p>
            <div>
              {getStockHistory(selectedStock).map((stock, idx, arr) => {
                let color = "#c6d9f6";
                if (idx > 0) {
                  const prev = arr[idx - 1];
                  if (stock.LTP > prev.LTP) color = "#c6f6c6";
                  else if (stock.LTP < prev.LTP) color = "#f6c6c6";
                }
                return (
                  <div
                    key={idx}
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      padding: "5px",
                      background: color,
                      marginBottom: "2px",
                    }}
                  >
                    <span>LTP: {stock.LTP}</span>
                    <span>Vol: {stock.volume}</span>
                  </div>
                );
              })}
            </div>
            <div style={{ marginTop: "10px", fontWeight: "bold" }}>
              {(() => {
                const history = getStockHistory(selectedStock);
                if (history.length === 0) return "";
                const { avgLTP, avgVol } = getAverages(history);
                return `Average LTP: ${avgLTP.toFixed(2)}, Average Vol: ${avgVol.toFixed(0)}`;
              })()}
            </div>
            <button
              onClick={() => setSelectedStock(null)}
              style={{ marginTop: "10px", padding: "5px 10px", cursor: "pointer" }}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TopGainer;
