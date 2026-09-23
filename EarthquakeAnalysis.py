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

#=========================================
#Visualize Earthquake Data
#=========================================

#Scatter plot: x-latitude, y-magnitude
magnitudes = [eq.magnitude for eq in quakes]
latitudes = [eq.latit for eq in quakes]

#Create and label the scatter plot using the data from the two lists of mags. & lats. above
#Uses a red color map, and the magnitudes, to display higher magnitude earthquakes as darker shades of red
plt.figure()
scatter = plt.scatter(latitudes, magnitudes, c=magnitudes, cmap="Reds")
plt.colorbar(scatter, label="Magnitude")
plt.xlabel("Latitude")
plt.ylabel("Magnitude")
plt.title("Earthquake Magnitude vs. Latitude")
plt.savefig("earthquake_scatter.png")
print("\nSaved earthquake_scatter.png")


#Bar chart
#Create data ranges
ranges = ["0-1", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7+"]
counts = [0] * len(ranges)

#Creates a list of 8 zeros (one for each magnitude range), and increments each index when a corresponding magnitude range is found
for m in magnitudes:
    if m >= 7:
        counts[7] += 1
    else:
        counts[int(m)] += 1

#Create and plot data using the lists counts and ranges
plt.figure()
plt.bar(ranges, counts)
plt.xlabel("Magnitude Range")
plt.ylabel("Number of Earthquakes")
plt.title("Earthquake Magnitude Distribution")
plt.savefig("earthquake_bar_chart.png")
print("Saved earthquake_bar_chart.png")

plt.show()

#=======================================================================================
#Display the strongest earthquake, and the most recent earthquake based on sorted data
#=======================================================================================
largest = by_magnitude[0]
print(f"\nLargest earthquake: Magnitude: {largest.magnitude} - {largest.location} ({largest.time})")

most_recent = by_date[0]
print(f"Most recent earthquake: {most_recent.time} - {most_recent.location} (Magnitude: {most_recent.magnitude})")