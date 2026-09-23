from datetime import datetime
from bridges.data_src_dependent.data_source import get_earthquake_usgs_data
import matplotlib.pyplot as plt


#Get 100 earthquakes
quakes = get_earthquake_usgs_data(100)
print(f"Fetched {len(quakes)} earthquakes\n")

#=========================================
#Sort Earthquake Data
#=========================================

#Sort by magnitude, strongest to weakest
by_magnitude = sorted(quakes, key=lambda eq: eq.magnitude, reverse=True)

#Sort by date, most recent to latest
# eq.time is a formatted as "%Y-%m-%d %H:%M:%S", so you have to convert it to a real date time object to sort correctly
by_date = sorted(quakes, key=lambda eq: eq.time, reverse=True)

#=========================================
# Display Earthquake Data
#=========================================

#Print top 10 strongest earthquakes
print("Top 10 Strongest Earthquakes")
print("-" * 50)
for eq in by_magnitude[:10]:
    print(f"Magnitude: {eq.magnitude:<5} {eq.location:<30} {eq.time}")

#Print top 10 most recent earthquakes
print("\nTop 10 Most Recent Earthquakes")
print("-" * 50)
for eq in by_date[:10]:
    print(f"{eq.time}  {eq.location:<30} Magnitude: {eq.magnitude}")

