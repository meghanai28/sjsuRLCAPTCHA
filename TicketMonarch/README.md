# TicketMonarch - Full-Stack Web Application

A full-stack web application built with Flask (Python) backend, React with Vite frontend, and SQLite database with CSV import capability.

## Project Structure

```
TicketMonarch/
├── backend/
│   ├── app.py              # Flask API server
│   ├── models.py           # SQLAlchemy database models
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── main.jsx        # Vite entry point
│   │   ├── App.css         # Application styles
│   │   └── index.css       # Global styles
│   ├── index.html          # HTML template
│   ├── vite.config.js      # Vite configuration
│   └── package.json        # Node.js dependencies
├── data/
│   ├── orders.csv          # CSV file for order data
│   └── ticketmonarch.db    # SQLite database (created automatically)
└── README.md               # This file
```

## Features

- **Backend API**: Flask REST API with SQLite database
- **Frontend**: React application with Vite for fast development
- **Database**: SQLite with SQLAlchemy ORM
- **CSV Import**: Import orders from CSV file
- **CORS Enabled**: Backend configured for frontend communication
- **Modern UI**: Beautiful, responsive design

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Quick Start

Follow these steps to get the application running:

### Step 1: Install Python Dependencies

Navigate to the backend directory and install the required Python packages:

```bash
cd backend
pip install -r requirements.txt
```

**Note:** It's recommended to use a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Node Dependencies

Navigate to the frontend directory and install the required Node.js packages:

```bash
cd frontend
npm install
```

### Step 3: Run the Flask Backend

From the backend directory, start the Flask server:

```bash
cd backend
python app.py
```

The backend API will be running on `http://localhost:5000`

### Step 4: Run the React Frontend

From the frontend directory, start the development server:

```bash
cd frontend
npm run dev
```

The frontend will be running on `http://localhost:5173` (Vite default port) (May run on other ports, check terminal)

### Step 5: Access the Application

Open your web browser and navigate to:

**http://localhost:5173**

The application should now be running with both frontend and backend connected.

### Database Setup

The SQLite database (`ticketmonarch.db`) will be automatically created in the `data/` directory when you first run the Flask server. The database schema is defined in `backend/models.py`.

## API Endpoints

- `GET /api/health` - Health check endpoint
- `GET /api/orders` - Get all orders
- `GET /api/orders/<id>` - Get a specific order by ID
- `POST /api/orders` - Create a new order
- `POST /api/orders/import` - Import orders from CSV file
- `POST /api/checkout` - Submit checkout form data
- `GET /api/export` - Export checkout data to CSV

## Usage

1. **Create an Order**: Fill out the form on the frontend and click "Create Order"
2. **View Orders**: All orders are displayed in the orders section
3. **Import from CSV**: Click the "Import from CSV" button to import orders from `data/orders.csv`

## CSV Format

The `orders.csv` file should have the following columns:
- `customer_name` - Customer's full name
- `email` - Customer's email address
- `product_name` - Name of the product/ticket
- `quantity` - Number of items
- `price` - Price per item
- `total` - Total price (quantity × price)
- `order_date` - Order date (ISO format)

Example:
```csv
customer_name,email,product_name,quantity,price,total,order_date
John Doe,john.doe@example.com,Concert Ticket VIP,2,150.00,300.00,2024-01-15T10:30:00
```

## Development

### Backend Development

- The Flask server runs in debug mode by default
- Database changes are automatically reflected
- CORS is enabled for frontend communication

### Frontend Development

- Vite provides hot module replacement (HMR) for instant updates
- The frontend proxies API requests to `http://localhost:5000`
- Changes to React components are reflected immediately

## Building for Production

### Frontend

Build the React app for production:
```bash
cd frontend
npm run build
```

The production build will be in the `frontend/dist` directory.

### Backend

For production deployment:
1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

## Troubleshooting

### Backend Issues

- **Port 5000 already in use**: Change the port in `app.py` or stop the process using port 5000
- **Database errors**: Delete `data/ticketmonarch.db` and restart the server to recreate the database
- **Import errors**: Ensure `data/orders.csv` exists and has the correct format

### Frontend Issues

- **Port 5173 already in use**: Vite will automatically use the next available port
- **API connection errors**: Ensure the Flask server is running on port 5000
- **Module not found**: Run `npm install` again to ensure all dependencies are installed
- **CORS errors**: Make sure the backend CORS is configured for `http://localhost:5173`

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-CORS, Pandas
- **Frontend**: React, Vite
- **Database**: SQLite
- **Styling**: CSS3 with modern design patterns

## License

This project is open source and available for use.

