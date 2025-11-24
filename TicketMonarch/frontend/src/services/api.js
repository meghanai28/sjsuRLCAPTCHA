// Backend API base URL
// In development with Vite proxy, you can also use relative URLs like '/api'
// For production, update this to your backend server URL
const API_BASE_URL = 'http://localhost:5000'

export const submitCheckout = async (checkoutData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/checkout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(checkoutData),
    })

    const data = await response.json()

    if (response.ok && data.success) {
      return { success: true }
    }

    return { success: false }

  } catch (error) {
    return { success: false }
  }
}

/**
 * Get all orders from the backend
 * @returns {Promise<Object>} Response object with orders data
 */
export const getOrders = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/orders`)
    const data = await response.json()

    if (response.ok && data.success) {
      return {
        success: true,
        data: data.orders || [],
        count: data.count || 0
      }
    }

    return {
      success: false,
      error: data.error || 'Failed to fetch orders',
      data: []
    }
  } catch (error) {
    console.error('Get orders API error:', error)
    return {
      success: false,
      error: 'Network error',
      message: 'Unable to fetch orders. Please check your connection.',
      data: []
    }
  }
}

/**
 * Export checkout data to CSV
 * @returns {Promise<Object>} Response object with export status
 */
export const exportCheckouts = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/export`)
    const data = await response.json()

    if (response.ok && data.success) {
      return {
        success: true,
        message: data.message || 'Data exported successfully',
        filePath: data.file_path
      }
    }

    return {
      success: false,
      error: data.error || 'Failed to export data'
    }
  } catch (error) {
    console.error('Export API error:', error)
    return {
      success: false,
      error: 'Network error',
      message: 'Unable to export data. Please check your connection.'
    }
  }
}

/**
 * Health check endpoint
 * @returns {Promise<Object>} Response object with health status
 */
export const healthCheck = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`)
    const data = await response.json()

    return {
      success: response.ok,
      data: data
    }
  } catch (error) {
    console.error('Health check API error:', error)
    return {
      success: false,
      error: 'Unable to connect to the server'
    }
  }
}

