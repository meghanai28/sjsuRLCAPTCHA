import { useState, useEffect } from 'react'
import './App.css'
import Checkout from './Checkout'

function App() {
  const [view, setView] = useState('checkout') // 'checkout' or 'orders'
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [formData, setFormData] = useState({
    customer_name: '',
    email: '',
    product_name: '',
    quantity: 1,
    price: 0
  })

  useEffect(() => {
    fetchOrders()
  }, [])

  const fetchOrders = async () => {
    try {
      const response = await fetch('/api/orders')
      const data = await response.json()
      setOrders(data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching orders:', error)
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const total = formData.quantity * formData.price
    
    try {
      const response = await fetch('/api/orders', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          total: total
        })
      })
      
      if (response.ok) {
        const newOrder = await response.json()
        setOrders([...orders, newOrder])
        setFormData({
          customer_name: '',
          email: '',
          product_name: '',
          quantity: 1,
          price: 0
        })
        alert('Order created successfully!')
      } else {
        alert('Error creating order')
      }
    } catch (error) {
      console.error('Error creating order:', error)
      alert('Error creating order')
    }
  }

  const handleImport = async () => {
    try {
      const response = await fetch('/api/orders/import', {
        method: 'POST'
      })
      const data = await response.json()
      alert(data.message || 'Orders imported successfully!')
      fetchOrders()
    } catch (error) {
      console.error('Error importing orders:', error)
      alert('Error importing orders')
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  // Sample purchase details for checkout
  const purchaseDetails = [
    { name: 'Chappel Roan - Nov 16 Section 219', price: '100.00', count: 1 }
  ]

  return (
    <div className={`App ${view === 'checkout' ? 'checkout-view' : ''}`}>
      {view !== 'checkout' && (
      <header className="App-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%', maxWidth: '1200px', margin: '0 auto' }}>
          <h1>TicketMonarch</h1>
          <nav style={{ display: 'flex', gap: '20px' }}>
            <button 
              onClick={() => setView('checkout')}
              style={{ 
                padding: '8px 16px', 
                background: view === 'checkout' ? 'white' : 'transparent',
                color: view === 'checkout' ? '#667eea' : 'white',
                border: '1px solid white',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Checkout
            </button>
            <button 
              onClick={() => setView('orders')}
              style={{ 
                padding: '8px 16px', 
                background: view === 'orders' ? 'white' : 'transparent',
                color: view === 'orders' ? '#667eea' : 'white',
                border: '1px solid white',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Orders
            </button>
          </nav>
        </div>
      </header>
      )}

      {view === 'checkout' ? (
        <Checkout purchaseDetails={purchaseDetails} />
      ) : (
        <main className="App-main">
        <section className="order-form">
          <h2>Create New Order</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Customer Name:</label>
              <input
                type="text"
                name="customer_name"
                value={formData.customer_name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Product Name:</label>
              <input
                type="text"
                name="product_name"
                value={formData.product_name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Quantity:</label>
              <input
                type="number"
                name="quantity"
                value={formData.quantity}
                onChange={handleChange}
                min="1"
                required
              />
            </div>
            <div className="form-group">
              <label>Price:</label>
              <input
                type="number"
                name="price"
                value={formData.price}
                onChange={handleChange}
                min="0"
                step="0.01"
                required
              />
            </div>
            <div className="form-group">
              <label>Total: ${(formData.quantity * formData.price).toFixed(2)}</label>
            </div>
            <button type="submit">Create Order</button>
          </form>
        </section>

        <section className="orders-section">
          <div className="section-header">
            <h2>Orders</h2>
            <button onClick={handleImport} className="import-btn">
              Import from CSV
            </button>
          </div>
          
          {loading ? (
            <p>Loading orders...</p>
          ) : orders.length === 0 ? (
            <p>No orders found. Create one above or import from CSV.</p>
          ) : (
            <div className="orders-list">
              {orders.map(order => (
                <div key={order.id} className="order-card">
                  <h3>{order.product_name}</h3>
                  <p><strong>Customer:</strong> {order.customer_name}</p>
                  <p><strong>Email:</strong> {order.email}</p>
                  <p><strong>Quantity:</strong> {order.quantity}</p>
                  <p><strong>Price:</strong> ${parseFloat(order.price).toFixed(2)}</p>
                  <p><strong>Total:</strong> ${parseFloat(order.total).toFixed(2)}</p>
                  <p><strong>Date:</strong> {new Date(order.order_date).toLocaleString()}</p>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
      )}
    </div>
  )
}

export default App

