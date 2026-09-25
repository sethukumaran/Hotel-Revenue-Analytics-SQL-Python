# Hotel-Revenue-Analytics-SQL-Python

## Executive Summary

This project analyzes a hotel booking dataset across **25 properties, 4 cities, 2 hotel categories and 4 room classes**, using a star-schema style model:
- `dim_date`
- `dim_hotels`
- `dim_rooms`
- `fact_bookings`
- `fact_aggregated_bookings`
The analysis combines booking behavior, revenue realization, cancellation patterns, room economics, booking-channel mix, and occupancy.

### Key portfolio metrics

| KPI | Result |
|---|---:|
| Total bookings | 134,590 |
| Total guests | 274,134 |
| Revenue generated | ₹2.01B |
| Revenue realized | ₹1.71B |
| Revenue gap | ₹298.8M |
| Revenue realization rate | 85.12% |
| Cancellation rate | 24.83% |
| No-show rate | 5.02% |
| Overall occupancy | 57.87% |
| Average rating (rated bookings) | 3.62 |
| Bookings with a rating | 42.12% |

## Business Insights

### 1. Revenue is concentrated in Mumbai
Mumbai generated approximately **₹668.6M** in realized revenue, the largest contribution among the four cities. Hyderabad generated approximately ₹325.2M, Bangalore ₹420.4M and Delhi ₹294.5M.

**Business implication:** Mumbai should be treated as a major revenue engine, while lower-revenue markets should be investigated for demand, pricing, inventory, and property-level differences rather than judged only at city level.

### 2. Occupancy is highly uneven across properties
Portfolio occupancy is about **57.9%**, but property occupancy ranges from roughly **44.4% to 66.4%**.

The lower-occupancy properties include:
- Atliq Grands — Bangalore
- Atliq Seasons — Mumbai
- Atliq Exotica — Hyderabad
- Atliq Bay — Mumbai

**Business implication:** These properties represent clear diagnostic opportunities. Management should compare their local demand, pricing, channel mix, room availability, and cancellation behavior against stronger properties.

### 3. Cancellation is a major revenue-leakage area
There were **33,420 cancellations**, about **24.8% of bookings**. The generated-vs-realized revenue gap is approximately **₹298.8M**.

Cancelled bookings realize 40% of generated revenue in this dataset, while checked-out and no-show records show 100% realization.

**Business implication:** Cancellation policy, deposit requirements, flexible-rate design, reminder journeys and channel-specific cancellation terms should be investigated. The 40% realization for cancelled bookings should also be validated with finance because it appears to represent a cancellation fee/refund rule.

### 4. Mumbai has the highest realized revenue per booking
Average realized revenue per booking is approximately:
- Mumbai: ₹15.4K
- Bangalore: ₹13.1K
- Delhi: ₹12.2K
- Hyderabad: ₹9.3K

**Business implication:** The difference is large enough to investigate room mix, rate structure, length of stay, property mix and customer segment composition.

### 5. Premium and Presidential rooms generate substantially more value per booking
Average realized revenue per booking is approximately:
- Presidential: ₹23.4K
- Premium: ₹15.1K
- Elite: ₹11.3K
- Standard: ₹8.1K

**Business implication:** Upselling and packaging strategies can be valuable, but should be paired with occupancy and room-level demand analysis to avoid unnecessary discounting of high-value inventory.

### 6. Booking-channel volume is concentrated
The `others` channel contributes about **40.9% of bookings**, followed by MakeYourTrip at about 20.0%. Direct online contributes about 9.9%, while direct offline contributes about 5.0%.

Cancellation rates are relatively similar across platforms (roughly 24–25%).

**Business implication:** Because channel volume is concentrated, channel economics should be monitored beyond booking count: commission cost, cancellation behavior, customer quality, realized ADR and repeat rate should be added if available.

### 7. Demand is strongest around the middle of the analysis period
Realized revenue by booking month:
- May 2022: ₹573.2M
- June 2022: ₹564.8M
- July 2022: ₹499.2M

**Business implication:** The July decline should be decomposed into demand, pricing, property availability, cancellation and channel effects before changing commercial strategy.

## Senior Analyst Recommendations

1. **Build a property opportunity matrix** using occupancy, realized revenue, cancellation rate and rating.
2. **Investigate the ₹298.8M revenue gap**, separating cancellation fees, refunds and other revenue adjustments.
3. **Review low-occupancy properties individually** rather than applying one portfolio-wide pricing action.
4. **Analyze channel profitability**, not only channel volume. Add commission/marketing cost if available.
5. **Promote room upgrades** where higher room classes have healthy demand and sufficient inventory.
6. **Strengthen cancellation prevention** through deposit rules, reminders and differentiated flexible/non-refundable rates.
7. **Add customer segmentation** in the next iteration: new vs repeat guest, business vs leisure, domestic vs international, booking lead time and stay length.

## Data Quality Notes

- `ratings_given` is missing for **77,907 of 134,590 bookings** (~57.9%). Treat average rating as an observed-rating metric, not a full-population customer satisfaction metric.
- `dim_date` contains 92 dates, while `fact_bookings` contains booking dates beginning in April and check-in dates from May through July. Confirm whether April booking dates are intentionally outside the check-in reporting window.
- `fact_aggregated_bookings` contains 9,200 records, consistent with 25 properties × 92 dates × 4 room categories.
- The `day_type` field contains the value `weekeday`; standardize it to `weekday` in a production model.
- The dataset contains both generated and realized revenue. Always define which metric is used for financial reporting.
- No-show records have 100% realized revenue in this extract. Validate whether this is an intentional no-show charge policy.

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- SQL

## Conclusion

- This Hotel Revenue Analytics project provided a comprehensive view of booking performance, revenue generation, occupancy, cancellations, room-category economics, property performance, and booking-channel behavior across the hotel portfolio.

- The analysis shows that the business generated strong overall revenue, but there is significant opportunity to improve revenue realization and operational efficiency. The approximately ₹298.8M gap between revenue generated and revenue realized, combined with a 24.8% cancellation rate, highlights cancellation management as an important area for commercial improvement.

- Performance also varies considerably across cities and individual properties. Mumbai emerged as the largest revenue contributor, while property-level occupancy varied significantly, indicating that a single strategy may not be appropriate across the entire portfolio. Lower-occupancy properties should be investigated individually to understand differences in demand, pricing, inventory utilization, and booking-channel performance.

- Room-category analysis indicates that premium room categories generate substantially higher revenue per booking, creating opportunities for targeted upselling, room upgrades, and premium packages where demand supports them. At the same time, the concentration of bookings across specific channels demonstrates the importance of evaluating channels not only by booking volume but also by cancellation rate, commission cost, customer quality, and realized revenue.

- From a data perspective, the analysis also identified several areas requiring attention, including missing customer ratings, inconsistent date coverage, and the need to standardize certain categorical values. Addressing these data-quality issues would improve the reliability of future reporting and predictive analytics.

## Overall Business Takeaway

- The hotel business has a solid revenue base, but the analysis suggests that improving revenue realization, reducing cancellations, optimizing underperforming properties, and increasing the value generated from premium rooms and booking channels could create meaningful commercial opportunities.
- The next stage of analytics should move beyond descriptive reporting toward profitability analysis, customer segmentation, demand forecasting, dynamic pricing, cancellation prediction, and property-level performance forecasting.
