from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Order, Checkout, init_db, get_db, engine, save_checkout_to_db, export_checkouts_to_csv
from sqlalchemy.orm import Session
import pandas as pd
import os
import re
from datetime import datetime

app = Flask(__name__)
# Enable CORS for Vite frontend (default port 5173)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])

# Get base directory and data directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CSV_PATH = os.path.join(DATA_DIR, 'orders.csv')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize database
init_db()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is running"""
    return jsonify({'status': 'healthy', 'message': 'Flask API is running'})

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Retrieve all orders from the database for admin view"""
    db = Session(bind=engine)
    try:
        orders = db.query(Order).all()
        return jsonify({
            'success': True,
            'count': len(orders),
            'orders': [order.to_dict() for order in orders]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order and save to database and CSV"""
    data = request.json
    
    try:
        db = Session(bind=engine)
        order = Order(
            customer_name=data['customer_name'],
            email=data['email'],
            product_name=data['product_name'],
            quantity=data['quantity'],
            price=data['price'],
            total=data['total']
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        
        # Also append to CSV file
        append_to_csv(order)
        
        return jsonify(order.to_dict()), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Retrieve a specific order by its ID"""
    db = Session(bind=engine)
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            return jsonify(order.to_dict())
        return jsonify({'error': 'Order not found'}), 404
    finally:
        db.close()

@app.route('/api/orders/import', methods=['POST'])
def import_csv():
    """Import orders from CSV file into the database, skipping duplicates"""
    if not os.path.exists(CSV_PATH):
        return jsonify({'error': 'CSV file not found'}), 404
    
    try:
        df = pd.read_csv(CSV_PATH)
        db = Session(bind=engine)
        
        imported_count = 0
        for _, row in df.iterrows():
            # Check if order already exists (by email and product_name)
            existing = db.query(Order).filter(
                Order.email == row['email'],
                Order.product_name == row['product_name']
            ).first()
            
            if not existing:
                order = Order(
                    customer_name=row['customer_name'],
                    email=row['email'],
                    product_name=row['product_name'],
                    quantity=int(row['quantity']),
                    price=float(row['price']),
                    total=float(row['total'])
                )
                db.add(order)
                imported_count += 1
        
        db.commit()
        return jsonify({'message': f'Imported {imported_count} orders from CSV'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/checkout', methods=['POST'])
def checkout():
    """Process checkout form submission with validation and save to database"""
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
    
    data = request.json
    
    # Validation functions
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_card_number(card_number):
        # Remove spaces and dashes
        cleaned = re.sub(r'[\s-]', '', str(card_number))
        # Check if it's 13-19 digits (standard card length)
        return cleaned.isdigit() and 13 <= len(cleaned) <= 19
    
    def validate_card_expiry(expiry):
        # Check MM/YY format
        pattern = r'^(0[1-9]|1[0-2])\/([0-9]{2})$'
        match = re.match(pattern, str(expiry))
        if not match:
            return False
        month, year = match.groups()
        # Check if expiry is not in the past
        current_year = datetime.now().year % 100
        current_month = datetime.now().month
        expiry_year = int(year)
        expiry_month = int(month)
        if expiry_year < current_year:
            return False
        if expiry_year == current_year and expiry_month < current_month:
            return False
        return True
    
    def validate_cvv(cvv):
        # CVV should be 3-4 digits
        return str(cvv).isdigit() and 3 <= len(str(cvv)) <= 4
    
    def validate_zip_code(zip_code):
        # US ZIP code: 5 digits or 5+4 format
        pattern = r'^\d{5}(-\d{4})?$'
        return re.match(pattern, str(zip_code)) is not None
    
    # Validate all required fields
    required_fields = {
        'full_name': str,
        'email': str,
        'card_number': str,
        'card_expiry': str,
        'card_cvv': str,
        'billing_address': str,
        'city': str,
        'state': str,
        'zip_code': str
    }
    
    errors = []
    
    # Check if all required fields are present
    for field, field_type in required_fields.items():
        if field not in data:
            errors.append(f'{field} is required')
        elif not isinstance(data[field], field_type):
            errors.append(f'{field} must be a {field_type.__name__}')
        elif not data[field] or (isinstance(data[field], str) and not data[field].strip()):
            errors.append(f'{field} cannot be empty')
    
    # Field-specific validations
    if 'full_name' in data and data['full_name']:
        if len(data['full_name'].strip()) < 2:
            errors.append('full_name must be at least 2 characters long')
        if len(data['full_name'].strip()) > 100:
            errors.append('full_name must be less than 100 characters')
    
    if 'email' in data and data['email']:
        if not validate_email(data['email']):
            errors.append('email must be a valid email address')
    
    if 'card_number' in data and data['card_number']:
        if not validate_card_number(data['card_number']):
            errors.append('card_number must be a valid card number (13-19 digits)')
    
    if 'card_expiry' in data and data['card_expiry']:
        if not validate_card_expiry(data['card_expiry']):
            errors.append('card_expiry must be in MM/YY format and not expired')
    
    if 'card_cvv' in data and data['card_cvv']:
        if not validate_cvv(data['card_cvv']):
            errors.append('card_cvv must be 3-4 digits')
    
    if 'billing_address' in data and data['billing_address']:
        if len(data['billing_address'].strip()) < 5:
            errors.append('billing_address must be at least 5 characters long')
        if len(data['billing_address'].strip()) > 200:
            errors.append('billing_address must be less than 200 characters')
    
    if 'city' in data and data['city']:
        if len(data['city'].strip()) < 2:
            errors.append('city must be at least 2 characters long')
        if len(data['city'].strip()) > 100:
            errors.append('city must be less than 100 characters')
    
    if 'state' in data and data['state']:
        if len(data['state'].strip()) < 2:
            errors.append('state must be at least 2 characters long')
        if len(data['state'].strip()) > 50:
            errors.append('state must be less than 50 characters')
    
    if 'zip_code' in data and data['zip_code']:
        if not validate_zip_code(data['zip_code']):
            errors.append('zip_code must be a valid US ZIP code (5 digits or 5+4 format)')
    
    if errors:
        return jsonify({
            'success': False,
            'error': 'Validation failed',
            'errors': errors
        }), 400
    
    # Save to database
    try:
        # Clean and prepare data
        checkout_data = {
            'full_name': data['full_name'].strip(),
            'email': data['email'].strip().lower(),
            'card_number': re.sub(r'[\s-]', '', str(data['card_number'])),  # Remove spaces/dashes
            'card_expiry': data['card_expiry'].strip(),
            'card_cvv': str(data['card_cvv']).strip(),
            'billing_address': data['billing_address'].strip(),
            'city': data['city'].strip(),
            'state': data['state'].strip(),
            'zip_code': data['zip_code'].strip()
        }
        
        checkout = save_checkout_to_db(checkout_data)
        
        return jsonify({
            'success': True,
            'message': 'Checkout data saved successfully',
            'checkout': checkout.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to save checkout data',
            'message': str(e)
        }), 500

@app.route('/api/export', methods=['GET'])
def export_data():
    """Export all checkout records from database to CSV file"""
    try:
        csv_path = export_checkouts_to_csv()
        
        # Check if file exists and has data
        if os.path.exists(csv_path):
            file_size = os.path.getsize(csv_path)
            if file_size > 0:
                return jsonify({
                    'success': True,
                    'message': 'Data exported successfully',
                    'file_path': csv_path,
                    'file_size': file_size
                })
            else:
                return jsonify({
                    'success': True,
                    'message': 'Export completed, but database is empty',
                    'file_path': csv_path
                })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create export file'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to export data',
            'message': str(e)
        }), 500

def append_to_csv(order):
    """Append a new order record to the orders CSV file"""
    # Create CSV with headers if it doesn't exist
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=['customer_name', 'email', 'product_name', 'quantity', 'price', 'total', 'order_date'])
        df.to_csv(CSV_PATH, index=False)
    
    # Append new order
    new_row = {
        'customer_name': order.customer_name,
        'email': order.email,
        'product_name': order.product_name,
        'quantity': order.quantity,
        'price': order.price,
        'total': order.total,
        'order_date': order.order_date.isoformat() if order.order_date else datetime.utcnow().isoformat()
    }
    
    df = pd.read_csv(CSV_PATH)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

