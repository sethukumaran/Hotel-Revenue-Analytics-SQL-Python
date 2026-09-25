-- Hotel Revenue Analytics: SQL Analysis
-- Assumption: PostgreSQL-style SQL. Adjust DATE_TRUNC / EXTRACT syntax for your database.

-- 1. Overall KPI
SELECT
    COUNT(*) AS total_bookings,
    SUM(no_guests) AS total_guests,
    SUM(revenue_generated) AS revenue_generated,
    SUM(revenue_realized) AS revenue_realized,
    SUM(revenue_generated - revenue_realized) AS revenue_gap,
    ROUND(100.0 * SUM(revenue_realized) / NULLIF(SUM(revenue_generated),0), 2) AS realization_rate_pct
FROM fact_bookings;

-- 2. Booking status / cancellation analysis
SELECT
    booking_status,
    COUNT(*) AS bookings,
    SUM(revenue_generated) AS revenue_generated,
    SUM(revenue_realized) AS revenue_realized,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS booking_share_pct
FROM fact_bookings
GROUP BY booking_status
ORDER BY bookings DESC;

-- 3. Property performance
SELECT
    h.property_id,
    h.property_name,
    h.city,
    h.category,
    COUNT(b.booking_id) AS bookings,
    SUM(b.revenue_realized) AS realized_revenue,
    ROUND(AVG(b.ratings_given), 2) AS avg_rating,
    ROUND(100.0 * SUM(CASE WHEN b.booking_status='Cancelled' THEN 1 ELSE 0 END)
          / COUNT(*), 2) AS cancellation_rate_pct
FROM fact_bookings b
JOIN dim_hotels h ON b.property_id = h.property_id
GROUP BY h.property_id, h.property_name, h.city, h.category
ORDER BY realized_revenue DESC;

-- 4. Occupancy by property
SELECT
    h.property_name,
    h.city,
    SUM(a.successful_bookings) AS successful_bookings,
    SUM(a.capacity) AS capacity,
    ROUND(100.0 * SUM(a.successful_bookings) / NULLIF(SUM(a.capacity),0), 2) AS occupancy_pct
FROM fact_aggregated_bookings a
JOIN dim_hotels h ON a.property_id = h.property_id
GROUP BY h.property_name, h.city
ORDER BY occupancy_pct DESC;

-- 5. City-level performance
SELECT
    h.city,
    COUNT(*) AS bookings,
    SUM(b.revenue_realized) AS realized_revenue,
    ROUND(100.0 * SUM(CASE WHEN b.booking_status='Cancelled' THEN 1 ELSE 0 END)
          / COUNT(*), 2) AS cancellation_rate_pct
FROM fact_bookings b
JOIN dim_hotels h ON b.property_id = h.property_id
GROUP BY h.city
ORDER BY realized_revenue DESC;

-- 6. Room-class economics
SELECT
    r.room_class,
    COUNT(*) AS bookings,
    SUM(b.revenue_realized) AS realized_revenue,
    ROUND(AVG(b.revenue_realized),2) AS avg_realized_per_booking
FROM fact_bookings b
JOIN dim_rooms r ON b.room_category = r.room_id
GROUP BY r.room_class
ORDER BY avg_realized_per_booking DESC;

-- 7. Booking platform mix
SELECT
    booking_platform,
    COUNT(*) AS bookings,
    SUM(revenue_realized) AS realized_revenue,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS booking_share_pct
FROM fact_bookings
GROUP BY booking_platform
ORDER BY bookings DESC;

-- 8. Monthly trend
SELECT
    DATE_TRUNC('month', booking_date)::date AS booking_month,
    COUNT(*) AS bookings,
    SUM(revenue_realized) AS realized_revenue,
    SUM(revenue_generated) AS generated_revenue
FROM fact_bookings
GROUP BY 1
ORDER BY 1;

-- 9. Lead-time analysis
SELECT
    CASE
        WHEN (check_in_date - booking_date) = 0 THEN 'Same day'
        WHEN (check_in_date - booking_date) BETWEEN 1 AND 2 THEN '1-2 days'
        WHEN (check_in_date - booking_date) BETWEEN 3 AND 7 THEN '3-7 days'
        WHEN (check_in_date - booking_date) BETWEEN 8 AND 14 THEN '8-14 days'
        ELSE '15+ days'
    END AS lead_time_bucket,
    COUNT(*) AS bookings,
    SUM(revenue_realized) AS realized_revenue,
    ROUND(100.0 * SUM(CASE WHEN booking_status='Cancelled' THEN 1 ELSE 0 END)
          / COUNT(*),2) AS cancellation_rate_pct
FROM fact_bookings
GROUP BY 1
ORDER BY MIN(check_in_date - booking_date);

-- 10. High-priority property opportunity screen
WITH occupancy AS (
    SELECT property_id,
           SUM(successful_bookings) AS successful_bookings,
           SUM(capacity) AS capacity
    FROM fact_aggregated_bookings
    GROUP BY property_id
),
revenue AS (
    SELECT property_id,
           SUM(revenue_realized) AS realized_revenue,
           COUNT(*) AS bookings,
           SUM(CASE WHEN booking_status='Cancelled' THEN 1 ELSE 0 END) AS cancellations
    FROM fact_bookings
    GROUP BY property_id
)
SELECT
    h.property_name,
    h.city,
    ROUND(100.0 * o.successful_bookings / NULLIF(o.capacity,0),2) AS occupancy_pct,
    r.realized_revenue,
    ROUND(100.0 * r.cancellations / NULLIF(r.bookings,0),2) AS cancellation_rate_pct
FROM occupancy o
JOIN revenue r ON o.property_id = r.property_id
JOIN dim_hotels h ON o.property_id = h.property_id
ORDER BY occupancy_pct ASC, realized_revenue DESC;
