# Tesla Campsite Finder ⚡

A web application for discovering and sharing campsites that offer Tesla charging facilities.

## Features

- **Submit Campsites**: Share information about Tesla-friendly campsites including:
  - Location name
  - Address
  - Charging capacity (kW)
  - Available amenities (RV hookups, WiFi, restrooms, etc.)

- **View Campsites**: Browse all submitted campsites with:
  - Search functionality
  - Detailed campsite information
  - CSV download option

## Installation

1. Clone this repository:
```bash
git clone https://github.com/muthukumaran-s02/tesla-camp-sites.git
cd tesla-camp-sites
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:

**Option 1: Using Docker (Recommended)**
```bash
# Start PostgreSQL using docker-compose
docker-compose up -d

# The database will be created automatically
```

**Option 2: Manual PostgreSQL Setup**
```bash
# Create a new PostgreSQL database
createdb tesla_campsites

# Or using psql
psql -U postgres
CREATE DATABASE tesla_campsites;
\q
```

4. Configure database connection:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your database credentials
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=tesla_campsites
# DB_USER=postgres
# DB_PASSWORD=your_password
```

## Requirements

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Streamlit 1.39.0
- Pandas 2.2.3
- SQLAlchemy 2.0.36
- psycopg2-binary 2.9.10

## Usage

Run the application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Database Schema

The application uses a PostgreSQL database with the following table structure:

```sql
CREATE TABLE campsites (
    id SERIAL PRIMARY KEY,
    location_name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    charging_capacity FLOAT NOT NULL,
    amenities TEXT,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## How to Use

### Submit a Campsite
1. Navigate to the "Submit a Campsite" tab
2. Fill in the required fields:
   - Location Name
   - Address
   - Charging Capacity
3. Select applicable amenities from the list
4. Add any additional amenities not listed
5. Click "Submit Campsite"

### View Campsites
1. Navigate to the "View Campsites" tab
2. Browse all submitted campsites
3. Use the search box to filter by location or address
4. Download the data as CSV if needed

## Environment Variables

The following environment variables can be configured:

- `DB_HOST`: PostgreSQL server host (default: localhost)
- `DB_PORT`: PostgreSQL server port (default: 5432)
- `DB_NAME`: Database name (default: tesla_campsites)
- `DB_USER`: Database user (default: postgres)
- `DB_PASSWORD`: Database password (default: postgres)

## Contributing

Feel free to submit issues or pull requests to improve the application!