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

## Usage

Run the application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Requirements

- Python 3.8 or higher
- Streamlit 1.39.0
- Pandas 2.2.3

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

## Data Storage

Campsite data is stored locally in `campsites_data.csv`. This file is created automatically when you first run the application and is excluded from version control.

## Contributing

Feel free to submit issues or pull requests to improve the application!