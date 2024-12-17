import pandas as pd
import matplotlib.pyplot as plt
import os

# Define input and output paths
input_path = './data/combined_bedroom_category_long.csv'
output_folder = './descriptive statistics'
os.makedirs(output_folder, exist_ok=True)

# Load the data
df = pd.read_csv(input_path)

# Ensure Count_of_Rents is numeric
df['Count_of_Rents'] = pd.to_numeric(df['Count_of_Rents'], errors='coerce')
df = df.dropna(subset=['Count_of_Rents'])  # Remove rows with invalid values
df['Count_of_Rents'] = df['Count_of_Rents'].astype(int)

# --- Data Analysis ---

# 1. Total number of Airbnb listings over years
total_listings = df.groupby('Year')['Count_of_Rents'].sum().reset_index()
total_listings.columns = ['Year', 'Total_Rents']

# 2. Adjust room type: keep 'Room', aggregate others as 'Entire home'
df['Bedroom_Category_Adjusted'] = df['Bedroom_Category'].apply(
    lambda x: 'Room' if 'Room' in x else 'Entire home'
)

# Group data for adjusted room types
room_type_summary = df.groupby(['Year', 'Bedroom_Category_Adjusted'])['Count_of_Rents'].sum().reset_index()
room_type_summary.columns = ['Year', 'Bedroom_Category', 'Total_Rents']

# 3. Top boroughs with the most listings and their room type distribution
top_boroughs = df.groupby('Borough')['Count_of_Rents'].sum().nlargest(3).index  # Top 3 boroughs
top_regions_summary = df[df['Borough'].isin(top_boroughs)].groupby(
    ['Year', 'Borough', 'Bedroom_Category_Adjusted']
)['Count_of_Rents'].sum().reset_index()
top_regions_summary.columns = ['Year', 'Borough', 'Bedroom_Category', 'Total_Rents']

# Get a sorted list of years
years = sorted(df['Year'].unique())

# --- Data Visualization ---

# Visualization 1: Total Airbnb listings over years
plt.figure(figsize=(10, 6))
plt.plot(total_listings['Year'], total_listings['Total_Rents'], marker='o', linestyle='-', color='b')
plt.title("Total Airbnb Listings Change Over Years")
plt.xlabel("Year")
plt.ylabel("Total Listings")
plt.xticks(years, rotation=45)  # Ensure x-axis has integer years
plt.grid(True)
plt.savefig(os.path.join(output_folder, "total_listings_trend.png"))
plt.show()

# Visualization 2: Change in adjusted room types over years
plt.figure(figsize=(12, 8))
for room_type in room_type_summary['Bedroom_Category'].unique():
    subset = room_type_summary[room_type_summary['Bedroom_Category'] == room_type]
    plt.plot(subset['Year'], subset['Total_Rents'], marker='o', linestyle='-', label=room_type)

plt.title("Change in Room Types Over Years")
plt.xlabel("Year")
plt.ylabel("Number of Listings")
plt.xticks(years, rotation=45)
plt.legend(title="Room Type")
plt.grid(True)
plt.savefig(os.path.join(output_folder, "adjusted_room_type_trend.png"))
plt.show()

# Visualization 3: Top boroughs and room type distribution
plt.figure(figsize=(12, 8))
for borough in top_boroughs:
    subset = top_regions_summary[top_regions_summary['Borough'] == borough]
    for category in subset['Bedroom_Category'].unique():
        subdata = subset[subset['Bedroom_Category'] == category]
        plt.bar(subdata['Year'] + (0.1 * top_boroughs.tolist().index(borough)),
                subdata['Total_Rents'], label=f"{borough} - {category}")

plt.title("Top Boroughs and Their Room Type Distribution")
plt.xlabel("Year")
plt.ylabel("Total Listings")
plt.xticks(years, rotation=45)
plt.legend(title="Borough and Room Type", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "top_boroughs_room_type.png"))
plt.show()

# --- Save Results ---
total_listings.to_csv(os.path.join(output_folder, "total_listings_summary.csv"), index=False)
room_type_summary.to_csv(os.path.join(output_folder, "adjusted_room_type_summary.csv"), index=False)
top_regions_summary.to_csv(os.path.join(output_folder, "top_regions_summary.csv"), index=False)

print("Analysis completed. Results and visualizations have been saved successfully.")
