"""
Hotel Revenue Analytics — End-to-End Python Analysis
Run from the project root after placing the five CSV files in data/.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA = "data"
FIG = "figures"
os.makedirs(FIG, exist_ok=True)

date = pd.read_csv(f"{DATA}/dim_date.csv")
hotels = pd.read_csv(f"{DATA}/dim_hotels.csv")
rooms = pd.read_csv(f"{DATA}/dim_rooms.csv")
agg = pd.read_csv(f"{DATA}/fact_aggregated_bookings.csv")
book = pd.read_csv(f"{DATA}/fact_bookings.csv")

date["date"] = pd.to_datetime(date["date"], errors="coerce")
for c in ["booking_date", "check_in_date", "checkout_date"]:
    book[c] = pd.to_datetime(book[c], errors="coerce")

# Data quality
print("=== SHAPES ===")
for name, df in {"date":date, "hotels":hotels, "rooms":rooms, "aggregated_bookings":agg, "bookings":book}.items():
    print(name, df.shape)

print("\n=== MISSING VALUES ===")
print(book.isna().sum())

# Enrich fact bookings
b = (book.merge(hotels, on="property_id", how="left")
          .merge(rooms, left_on="room_category", right_on="room_id", how="left"))

b["booking_month"] = b["booking_date"].dt.to_period("M").astype(str)
b["lead_days"] = (b["check_in_date"] - b["booking_date"]).dt.days

# Core KPIs
print("\n=== CORE KPIs ===")
print("Bookings:", len(b))
print("Guests:", b["no_guests"].sum())
print("Revenue generated:", b["revenue_generated"].sum())
print("Revenue realized:", b["revenue_realized"].sum())
print("Revenue gap:", b["revenue_generated"].sum() - b["revenue_realized"].sum())
print("Realization rate:",
      round(100*b["revenue_realized"].sum()/b["revenue_generated"].sum(), 2), "%")
print("Cancellation rate:",
      round(100*b["booking_status"].eq("Cancelled").mean(), 2), "%")
print("No-show rate:",
      round(100*b["booking_status"].eq("No Show").mean(), 2), "%")
print("Average rating among rated bookings:",
      round(b["ratings_given"].mean(), 2))

# Occupancy
a = (agg.merge(hotels, on="property_id", how="left")
         .merge(rooms, left_on="room_category", right_on="room_id", how="left"))
a["occupancy"] = a["successful_bookings"] / a["capacity"]
print("\nOverall occupancy:",
      round(100*a["successful_bookings"].sum()/a["capacity"].sum(), 2), "%")

# Business cuts
print("\n=== CITY PERFORMANCE ===")
city = b.groupby("city").agg(
    bookings=("booking_id","count"),
    realized_revenue=("revenue_realized","sum"),
    cancellations=("booking_status", lambda x: (x=="Cancelled").sum())
)
city["cancellation_rate"] = 100*city["cancellations"]/city["bookings"]
print(city.sort_values("realized_revenue", ascending=False))

print("\n=== PROPERTY PERFORMANCE ===")
prop = b.groupby(["property_id","property_name","city","category"]).agg(
    bookings=("booking_id","count"),
    realized_revenue=("revenue_realized","sum"),
    cancellations=("booking_status", lambda x: (x=="Cancelled").sum()),
    avg_rating=("ratings_given","mean")
).reset_index()
prop["cancellation_rate"] = 100*prop["cancellations"]/prop["bookings"]
print(prop.sort_values("realized_revenue", ascending=False).head(10))

print("\n=== ROOM CLASS ===")
room = b.groupby("room_class").agg(
    bookings=("booking_id","count"),
    realized_revenue=("revenue_realized","sum"),
    avg_realized_per_booking=("revenue_realized","mean")
).sort_values("avg_realized_per_booking", ascending=False)
print(room)

print("\n=== PLATFORM ===")
platform = b.groupby("booking_platform").agg(
    bookings=("booking_id","count"),
    realized_revenue=("revenue_realized","sum")
).sort_values("bookings", ascending=False)
print(platform)

# Visualizations
monthly = b.groupby("booking_month")["revenue_realized"].sum()
monthly.plot(marker="o", title="Monthly Realized Revenue", ylabel="₹", xlabel="Booking Month")
plt.tight_layout(); plt.savefig(f"{FIG}/monthly_revenue.png", dpi=180); plt.close()

city["realized_revenue"].sort_values().plot(kind="barh", title="Realized Revenue by City", xlabel="₹")
plt.tight_layout(); plt.savefig(f"{FIG}/revenue_by_city.png", dpi=180); plt.close()

prop.sort_values("realized_revenue").tail(10).set_index("property_name")["realized_revenue"].plot(
    kind="barh", title="Top 10 Properties by Realized Revenue", xlabel="₹")
plt.tight_layout(); plt.savefig(f"{FIG}/top_properties_revenue.png", dpi=180); plt.close()

a.groupby("city").apply(lambda x: x["successful_bookings"].sum()/x["capacity"].sum()).mul(100).plot(
    kind="bar", title="Occupancy by City", ylabel="Occupancy (%)")
plt.ylim(0,100); plt.tight_layout(); plt.savefig(f"{FIG}/occupancy_by_city.png", dpi=180); plt.close()

b["booking_status"].value_counts().plot(kind="bar", title="Booking Status Distribution", ylabel="Bookings")
plt.tight_layout(); plt.savefig(f"{FIG}/booking_status.png", dpi=180); plt.close()

platform["bookings"].sort_values().plot(kind="barh", title="Booking Volume by Platform", xlabel="Bookings")
plt.tight_layout(); plt.savefig(f"{FIG}/platform_volume.png", dpi=180); plt.close()

room["avg_realized_per_booking"].sort_values().plot(kind="bar", title="Average Realized Revenue by Room Class", ylabel="₹")
plt.tight_layout(); plt.savefig(f"{FIG}/room_class_value.png", dpi=180); plt.close()

property_occ = a.groupby(["property_id","property_name"]).agg(
    successful=("successful_bookings","sum"), capacity=("capacity","sum")).reset_index()
property_occ["occupancy_pct"] = 100*property_occ["successful"]/property_occ["capacity"]
property_rev = b.groupby("property_id")["revenue_realized"].sum()
property_occ["realized_revenue"] = property_occ["property_id"].map(property_rev)
plt.scatter(property_occ["occupancy_pct"], property_occ["realized_revenue"]/1e6)
plt.xlabel("Occupancy (%)"); plt.ylabel("Realized Revenue (₹ million)")
plt.title("Property Occupancy vs Realized Revenue")
plt.tight_layout(); plt.savefig(f"{FIG}/occupancy_vs_revenue.png", dpi=180); plt.close()

print("\nAnalysis complete. Charts saved to figures/.")
