import { useState } from 'react'
import './Checkout.css'
import { submitCheckout } from './services/api'

const US_STATES = [
  'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
  'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
  'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
  'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
  'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
  'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
  'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
  'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
  'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
  'West Virginia', 'Wisconsin', 'Wyoming'
]

function Checkout({ purchaseDetails = null }) {
  const [formData, setFormData] = useState({
    full_name: '',
    card_number: '',
    card_expiry: '',
    card_cvv: '',
    billing_address: '',
    city: '',
    state: '',
    country: 'U.S.A.',
    zip_code: ''
  })

  const [errors, setErrors] = useState({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitMessage, setSubmitMessage] = useState({ type: null, text: '' })

  // Format card number with spaces every 4 digits
  const formatCardNumber = (value) => {
    const cleaned = value.replace(/\s/g, '')
    const formatted = cleaned.match(/.{1,4}/g)?.join(' ') || cleaned
    return formatted.slice(0, 19) // Max 16 digits + 3 spaces
  }

  // Format expiry date as MM/YY
  const formatExpiry = (value) => {
    const cleaned = value.replace(/\D/g, '')
    if (cleaned.length >= 2) {
      return cleaned.slice(0, 2) + '/' + cleaned.slice(2, 4)
    }
    return cleaned
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    let formattedValue = value

    if (name === 'card_number') {
      formattedValue = formatCardNumber(value)
    } else if (name === 'card_expiry') {
      formattedValue = formatExpiry(value)
    } else if (name === 'card_cvv') {
      formattedValue = value.replace(/\D/g, '').slice(0, 4)
    } else if (name === 'zip_code') {
      formattedValue = value.replace(/\D/g, '').slice(0, 5)
    }

    setFormData(prev => ({
      ...prev,
      [name]: formattedValue
    }))

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const validateForm = () => {
    const newErrors = {}

    // Full Name validation
    if (!formData.full_name.trim()) {
      newErrors.full_name = 'Full name is required'
    } else if (formData.full_name.trim().length < 2) {
      newErrors.full_name = 'Full name must be at least 2 characters'
    }

    // Card Number validation
    const cardNumberCleaned = formData.card_number.replace(/\s/g, '')
    if (!cardNumberCleaned) {
      newErrors.card_number = 'Card number is required'
    } else if (cardNumberCleaned.length < 13 || cardNumberCleaned.length > 19) {
      newErrors.card_number = 'Card number must be 13-19 digits'
    } else if (!/^\d+$/.test(cardNumberCleaned)) {
      newErrors.card_number = 'Card number must contain only digits'
    }

    // Expiry validation
    if (!formData.card_expiry) {
      newErrors.card_expiry = 'Expiry date is required'
    } else {
      const expiryMatch = formData.card_expiry.match(/^(\d{2})\/(\d{2})$/)
      if (!expiryMatch) {
        newErrors.card_expiry = 'Invalid format. Use MM/YY'
      } else {
        const month = parseInt(expiryMatch[1])
        const year = parseInt('20' + expiryMatch[2])
        const currentDate = new Date()
        const currentYear = currentDate.getFullYear()
        const currentMonth = currentDate.getMonth() + 1

        if (month < 1 || month > 12) {
          newErrors.card_expiry = 'Invalid month'
        } else if (year < currentYear || (year === currentYear && month < currentMonth)) {
          newErrors.card_expiry = 'Card has expired'
        }
      }
    }

    // CVV validation
    if (!formData.card_cvv) {
      newErrors.card_cvv = 'CVV is required'
    } else if (formData.card_cvv.length < 3 || formData.card_cvv.length > 4) {
      newErrors.card_cvv = 'CVV must be 3-4 digits'
    }

    // Billing Address validation
    if (!formData.billing_address.trim()) {
      newErrors.billing_address = 'Billing address is required'
    } else if (formData.billing_address.trim().length < 5) {
      newErrors.billing_address = 'Address must be at least 5 characters'
    }

    // City validation
    if (!formData.city.trim()) {
      newErrors.city = 'City is required'
    } else if (formData.city.trim().length < 2) {
      newErrors.city = 'City must be at least 2 characters'
    }

    // State validation
    if (!formData.state) {
      newErrors.state = 'State is required'
    }

    // Zip Code validation
    if (!formData.zip_code) {
      newErrors.zip_code = 'Zip code is required'
    } else if (formData.zip_code.length !== 5) {
      newErrors.zip_code = 'Zip code must be 5 digits'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!validateForm()) {
      return
    }

    setIsSubmitting(true)
    setSubmitMessage({ type: null, text: '' })

    try {
      const result = await submitCheckout(formData)

      if (result.success) {
        // Show success message
        setSubmitMessage({ 
          type: 'success', 
          text: result.message || 'Checkout successful! Your order has been processed.' 
        })
        
        // Reset form
        setFormData({
          full_name: '',
          card_number: '',
          card_expiry: '',
          card_cvv: '',
          billing_address: '',
          city: '',
          state: '',
          country: 'U.S.A.',
          zip_code: ''
        })
        setErrors({})
        
        // Clear success message after 5 seconds
        setTimeout(() => {
          setSubmitMessage({ type: null, text: '' })
        }, 5000)
      } else {
        // Handle validation errors from backend
        if (result.errors && Array.isArray(result.errors)) {
          const backendErrors = {}
          result.errors.forEach(error => {
            // Extract field name from error message
            const fieldMatch = error.match(/^(\w+)/)
            if (fieldMatch) {
              backendErrors[fieldMatch[1]] = error
            }
          })
          setErrors(prev => ({ ...prev, ...backendErrors }))
          setSubmitMessage({ 
            type: 'error', 
            text: result.message || 'Please correct the errors in the form' 
          })
        } else {
          setSubmitMessage({ 
            type: 'error', 
            text: result.message || result.error || 'Checkout failed. Please try again.' 
          })
        }
        
        // Clear error message after 5 seconds
        setTimeout(() => {
          setSubmitMessage({ type: null, text: '' })
        }, 5000)
      }
    } catch (error) {
      console.error('Error submitting checkout:', error)
      setSubmitMessage({ 
        type: 'error', 
        text: 'An unexpected error occurred. Please try again.' 
      })
      
      // Clear error message after 5 seconds
      setTimeout(() => {
        setSubmitMessage({ type: null, text: '' })
      }, 5000)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="checkout-container">
      <header className="checkout-header">
        <div className="checkout-header-content">
          <div className="logo">
            <span className="logo-icon">🦋</span>
            <span className="logo-text">Ticket Monarch</span>
          </div>
          <div className="header-icons">
            <span className="icon">🛒</span>
            <span className="icon">☰</span>
          </div>
        </div>
      </header>
      <div className="checkout-content">
        {/* Success/Error Message */}
        {submitMessage.type && (
          <div className={`submit-message ${submitMessage.type}`}>
            {submitMessage.type === 'success' ? '✓' : '✗'} {submitMessage.text}
          </div>
        )}
        
        <div className="checkout-content-wrapper">
          {/* Left Panel - Forms */}
          <div className="checkout-forms">
          <form onSubmit={handleSubmit}>
            {/* Payment Details Section */}
            <div className="form-section">
              <h2 className="section-title">Payment Details</h2>
              
              <div className="form-group">
                <label htmlFor="card_number">Card Number</label>
                <input
                  type="text"
                  id="card_number"
                  name="card_number"
                  value={formData.card_number}
                  onChange={handleChange}
                  placeholder="1234 5678 9012 3456"
                  maxLength="19"
                  className={errors.card_number ? 'error' : ''}
                />
                {errors.card_number && <span className="error-message">{errors.card_number}</span>}
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="card_expiry">MM/YY</label>
                  <input
                    type="text"
                    id="card_expiry"
                    name="card_expiry"
                    value={formData.card_expiry}
                    onChange={handleChange}
                    placeholder="MM/YY"
                    maxLength="5"
                    className={errors.card_expiry ? 'error' : ''}
                  />
                  {errors.card_expiry && <span className="error-message">{errors.card_expiry}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="card_cvv">CVC</label>
                  <input
                    type="text"
                    id="card_cvv"
                    name="card_cvv"
                    value={formData.card_cvv}
                    onChange={handleChange}
                    placeholder="123"
                    maxLength="4"
                    className={errors.card_cvv ? 'error' : ''}
                  />
                  {errors.card_cvv && <span className="error-message">{errors.card_cvv}</span>}
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="full_name">Name on Card</label>
                <input
                  type="text"
                  id="full_name"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  placeholder="John Doe"
                  className={errors.full_name ? 'error' : ''}
                />
                {errors.full_name && <span className="error-message">{errors.full_name}</span>}
              </div>
            </div>

            {/* Billing Address Section */}
            <div className="form-section">
              <h2 className="section-title">Billing Address</h2>
              
              <div className="form-group">
                <label htmlFor="billing_address">Address</label>
                <input
                  type="text"
                  id="billing_address"
                  name="billing_address"
                  value={formData.billing_address}
                  onChange={handleChange}
                  placeholder="123 Main Street"
                  className={errors.billing_address ? 'error' : ''}
                />
                {errors.billing_address && <span className="error-message">{errors.billing_address}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="apartment">Apartment, Suite, etc (optional)</label>
                <input
                  type="text"
                  id="apartment"
                  name="apartment"
                  placeholder="Apt 4B"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="city">City</label>
                  <input
                    type="text"
                    id="city"
                    name="city"
                    value={formData.city}
                    onChange={handleChange}
                    placeholder="New York"
                    className={errors.city ? 'error' : ''}
                  />
                  {errors.city && <span className="error-message">{errors.city}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="zip_code">Zip Code</label>
                  <input
                    type="text"
                    id="zip_code"
                    name="zip_code"
                    value={formData.zip_code}
                    onChange={handleChange}
                    placeholder="10001"
                    maxLength="5"
                    className={errors.zip_code ? 'error' : ''}
                  />
                  {errors.zip_code && <span className="error-message">{errors.zip_code}</span>}
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="country">Country</label>
                  <select
                    id="country"
                    name="country"
                    value={formData.country}
                    onChange={handleChange}
                  >
                    <option value="U.S.A.">U.S.A.</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="state">State</label>
                  <select
                    id="state"
                    name="state"
                    value={formData.state}
                    onChange={handleChange}
                    className={errors.state ? 'error' : ''}
                  >
                    <option value="">Select State</option>
                    {US_STATES.map(state => (
                      <option key={state} value={state}>{state}</option>
                    ))}
                  </select>
                  {errors.state && <span className="error-message">{errors.state}</span>}
                </div>
              </div>
            </div>
          </form>
          </div>

          {/* Right Panel - Purchase Details */}
          <div className="checkout-summary">
          <div className="summary-section">
            <h2 className="section-title">Purchase Details</h2>
            
            <table className="purchase-table">
              <thead>
                <tr>
                  <th>Tickets</th>
                  <th>Price</th>
                  <th>Count</th>
                </tr>
              </thead>
              <tbody>
                {purchaseDetails ? (
                  purchaseDetails.map((item, index) => (
                    <tr key={index}>
                      <td>{item.name}</td>
                      <td>${parseFloat(item.price).toFixed(2)}</td>
                      <td>{item.count}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td>Chappel Roan - Nov 16 Section 219</td>
                    <td>$100.00</td>
                    <td>1</td>
                  </tr>
                )}
                <tr className="total-row">
                  <td><strong>Total</strong></td>
                  <td><strong>
                    ${purchaseDetails 
                      ? purchaseDetails.reduce((sum, item) => sum + (parseFloat(item.price) * item.count), 0).toFixed(2)
                      : '100.00'}
                  </strong></td>
                  <td><strong>
                    {purchaseDetails 
                      ? purchaseDetails.reduce((sum, item) => sum + item.count, 0)
                      : 1}
                  </strong></td>
                </tr>
              </tbody>
            </table>

            <button 
              type="submit" 
              className="purchase-button"
              onClick={handleSubmit}
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Processing...' : 'Purchase'}
            </button>
          </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Checkout

