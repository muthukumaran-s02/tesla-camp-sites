import streamlit as st
import pandas as pd
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

# Database configuration
Base = declarative_base()

class Campsite(Base):
    __tablename__ = 'campsites'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    charging_capacity = Column(Float, nullable=False)
    amenities = Column(Text)
    submission_date = Column(DateTime, default=datetime.now)

# Database connection
def get_database_url():
    """Get database URL from environment variables or use default for local testing"""
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'tesla_campsites')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgres')
    
    return f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

@st.cache_resource
def get_engine():
    """Create and cache database engine"""
    database_url = get_database_url()
    return create_engine(database_url, poolclass=NullPool)

def init_database():
    """Initialize database tables"""
    try:
        engine = get_engine()
        Base.metadata.create_all(engine)
        return True
    except Exception as e:
        st.error(f"Database connection error: {e}")
        st.info("Please ensure PostgreSQL is running and the database credentials are correct.")
        return False

def get_session():
    """Get database session"""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

# Load existing data
def load_data():
    """Load campsite data from PostgreSQL database"""
    try:
        session = get_session()
        campsites = session.query(Campsite).all()
        session.close()
        
        data = [{
            'Location Name': c.location_name,
            'Address': c.address,
            'Charging Capacity (kW)': c.charging_capacity,
            'Amenities': c.amenities,
            'Submission Date': c.submission_date.strftime('%Y-%m-%d %H:%M:%S')
        } for c in campsites]
        
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=[
            'Location Name', 
            'Address', 
            'Charging Capacity (kW)', 
            'Amenities',
            'Submission Date'
        ])

# Save new submission
def save_submission(location_name, address, charging_capacity, amenities):
    """Save new campsite submission to PostgreSQL database"""
    try:
        session = get_session()
        new_campsite = Campsite(
            location_name=location_name,
            address=address,
            charging_capacity=charging_capacity,
            amenities=amenities,
            submission_date=datetime.now()
        )
        session.add(new_campsite)
        session.commit()
        session.close()
        return True
    except Exception as e:
        st.error(f"Error saving submission: {e}")
        return False

# Main application
def main():
    # Initialize database
    if not init_database():
        st.warning("⚠️ Running in demo mode. Database connection failed.")
        st.stop()
    
    # Set page configuration
    st.set_page_config(
        page_title="Tesla Campsite Finder",
        page_icon="⚡",
        layout="wide"
    )
    
    # Title and description
    st.title("⚡ Tesla Campsite Finder")
    st.markdown("Welcome to the Tesla Campsite Finder! Discover and share campsites that offer Tesla charging facilities.")
    
    # Create tabs for different features
    tab1, tab2 = st.tabs(["📝 Submit a Campsite", "🗺️ View Campsites"])
    
    # Tab 1: Submit a campsite
    with tab1:
        st.header("Submit a New Campsite")
        st.markdown("Help fellow Tesla owners by sharing campsite information!")
        
        with st.form("submission_form"):
            # Location Name
            location_name = st.text_input(
                "Location Name *",
                placeholder="e.g., Yosemite Valley Campground"
            )
            
            # Address
            address = st.text_area(
                "Address *",
                placeholder="Enter the full address of the campsite",
                height=100
            )
            
            # Charging Capacity
            charging_capacity = st.number_input(
                "Charging Capacity (kW) *",
                min_value=0.0,
                max_value=350.0,
                value=50.0,
                step=5.0,
                help="Maximum charging power available"
            )
            
            # Amenities (multiple select)
            amenities_options = [
                "RV Hookups",
                "Tent Camping",
                "Restrooms",
                "Showers",
                "WiFi",
                "Picnic Area",
                "Fire Pits",
                "Hiking Trails",
                "Pet Friendly",
                "Restaurant/Food",
                "Laundry",
                "Playground"
            ]
            
            selected_amenities = st.multiselect(
                "Amenities",
                amenities_options,
                help="Select all amenities available at this campsite"
            )
            
            # Additional amenities text input
            additional_amenities = st.text_input(
                "Other Amenities",
                placeholder="Any other amenities not listed above"
            )
            
            # Submit button
            submitted = st.form_submit_button("Submit Campsite", type="primary")
            
            if submitted:
                # Validate required fields
                if not location_name or not address:
                    st.error("Please fill in all required fields (marked with *)")
                else:
                    # Combine amenities
                    all_amenities = ", ".join(selected_amenities)
                    if additional_amenities:
                        all_amenities += f", {additional_amenities}" if all_amenities else additional_amenities
                    
                    # Save submission
                    if save_submission(
                        location_name,
                        address,
                        charging_capacity,
                        all_amenities if all_amenities else "None specified"
                    ):
                        st.success("✅ Campsite submitted successfully! Thank you for contributing!")
                        st.balloons()
    
    # Tab 2: View campsites
    with tab2:
        st.header("Discover Tesla-Friendly Campsites")
        
        # Load and display data
        df = load_data()
        
        if len(df) == 0:
            st.info("No campsites have been submitted yet. Be the first to add one!")
        else:
            # Display total count
            st.metric("Total Campsites", len(df))
            
            # Search functionality
            search_term = st.text_input(
                "🔍 Search Campsites",
                placeholder="Search by location name or address..."
            )
            
            # Filter data based on search
            if search_term:
                mask = df['Location Name'].str.contains(search_term, case=False, na=False) | \
                       df['Address'].str.contains(search_term, case=False, na=False)
                filtered_df = df[mask]
            else:
                filtered_df = df
            
            # Display results
            if len(filtered_df) == 0:
                st.warning("No campsites match your search.")
            else:
                st.subheader(f"Showing {len(filtered_df)} campsite(s)")
                
                # Display each campsite as a card
                for idx, row in filtered_df.iterrows():
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### 📍 {row['Location Name']}")
                            st.markdown(f"**Address:** {row['Address']}")
                            st.markdown(f"**Amenities:** {row['Amenities']}")
                        
                        with col2:
                            st.metric("Charging Capacity", f"{row['Charging Capacity (kW)']} kW")
                            st.caption(f"Added: {row['Submission Date']}")
                        
                        st.divider()
                
                # Option to download data
                st.subheader("Download Data")
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name="tesla_campsites.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
