import streamlit as st
import pandas as pd
import os
from datetime import datetime

# File to store submissions
DATA_FILE = 'campsites_data.csv'

# Initialize data file if it doesn't exist
def init_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            'Location Name', 
            'Address', 
            'Charging Capacity (kW)', 
            'Amenities',
            'Submission Date'
        ])
        df.to_csv(DATA_FILE, index=False)

# Load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=[
        'Location Name', 
        'Address', 
        'Charging Capacity (kW)', 
        'Amenities',
        'Submission Date'
    ])

# Save new submission
def save_submission(location_name, address, charging_capacity, amenities):
    df = load_data()
    new_row = pd.DataFrame([{
        'Location Name': location_name,
        'Address': address,
        'Charging Capacity (kW)': charging_capacity,
        'Amenities': amenities,
        'Submission Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Main application
def main():
    # Initialize data file
    init_data_file()
    
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
                    save_submission(
                        location_name,
                        address,
                        charging_capacity,
                        all_amenities if all_amenities else "None specified"
                    )
                    
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
