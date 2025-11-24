from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_database, save_order

app = Flask(__name__)
# Enable CORS for Vite frontend (default port 5173)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])

# Initialize database when app starts
init_database()

@app.route('/api/checkout', methods=['POST'])
def checkout():
    """Process checkout form submission and save to database"""
    try:
        data = request.json or {}
        
        # Prepare data - use empty strings if fields are missing
        order_data = {
            'full_name': data.get('full_name', '') or '',
            'email': data.get('email', '') or '',
            'card_number': data.get('card_number', '') or '',
            'card_expiry': data.get('card_expiry', '') or '',
            'card_cvv': data.get('card_cvv', '') or '',
            'billing_address': data.get('billing_address', '') or '',
            'city': data.get('city', '') or '',
            'state': data.get('state', '') or '',
            'zip_code': data.get('zip_code', '') or ''
        }
        
        order_id = save_order(order_data)
        
        return jsonify({
            'success': True,
            'id': order_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

