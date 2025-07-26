// marketplace_dashboard.jsx
import React, { useState, useEffect } from 'react';

function MarketplaceDashboard() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    // Note: Replace with your actual WebSocket server URL
    const ws = new WebSocket("wss://your-marketplace-server.example.com/ws");

    ws.onmessage = (e) => {
      const event = JSON.parse(e.data);
      setEvents(ev => [event, ...ev].slice(0, 50));
    };

    ws.onclose = () => console.log("Marketplace WebSocket closed");
    ws.onerror = (err) => console.error("WS error:", err);

    return () => ws.close();
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h2>Live Marketplace Event Feed</h2>
      <div style={{ 
        maxHeight: '400px', 
        overflowY: 'auto', 
        border: '1px solid #ccc', 
        padding: '10px',
        backgroundColor: '#f9f9f9'
      }}>
        {events.map((ev, i) => (
          <div key={i} style={{ 
            padding: '8px', 
            marginBottom: '5px', 
            backgroundColor: 'white',
            borderRadius: '4px',
            fontSize: '14px'
          }}>
            [{ev.timestamp || new Date().toISOString()}] {ev.organism} {ev.action} {ev.bounty?.id}
          </div>
        ))}
      </div>
    </div>
  );
}

export default MarketplaceDashboard;