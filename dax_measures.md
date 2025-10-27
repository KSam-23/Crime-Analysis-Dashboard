# DAX Measures Documentation
## Crime Analysis Dashboard

This document contains all DAX formulas used in the Power BI Crime Analysis Dashboard, organized by category with detailed explanations.

---

## Table of Contents
1. [Basic Aggregations](#basic-aggregations)
2. [Time Intelligence](#time-intelligence)
3. [Percentages & Ratios](#percentages--ratios)
4. [Comparisons & Changes](#comparisons--changes)
5. [Moving Averages & Trends](#moving-averages--trends)
6. [Geographic Metrics](#geographic-metrics)
7. [Crime Type Analytics](#crime-type-analytics)
8. [Operational KPIs](#operational-kpis)
9. [Advanced Analytics](#advanced-analytics)

---

## Basic Aggregations

### Total Crimes
**Purpose**: Count total number of crime incidents
```dax
Total Crimes = COUNTROWS(fact_crimes)
```

### Total Arrests
**Purpose**: Count crimes where an arrest was made
```dax
Total Arrests = 
CALCULATE(
    COUNTROWS(fact_crimes),
    fact_crimes[arrest_made] = TRUE()
)
```

### Domestic Crimes
**Purpose**: Count domestic-related crimes
```dax
Domestic Crimes = 
CALCULATE(
    COUNTROWS(fact_crimes),
    fact_crimes[domestic] = TRUE()
)
```

### Unique Crime Types
**Purpose**: Count distinct types of crimes
```dax
Unique Crime Types = DISTINCTCOUNT(dim_crime_type[primary_type])
```

### Unique Locations
**Purpose**: Count distinct locations (beats)
```dax
Unique Locations = DISTINCTCOUNT(fact_crimes[beat])
```

---

## Time Intelligence

### Crimes MTD (Month-to-Date)
**Purpose**: Total crimes from start of current month to today
```dax
Crimes MTD = 
TOTALMTD(
    [Total Crimes],
    dim_date[date]
)
```

### Crimes QTD (Quarter-to-Date)
**Purpose**: Total crimes from start of current quarter to today
```dax
Crimes QTD = 
TOTALQTD(
    [Total Crimes],
    dim_date[date]
)
```

### Crimes YTD (Year-to-Date)
**Purpose**: Total crimes from start of current year to today
```dax
Crimes YTD = 
TOTALYTD(
    [Total Crimes],
    dim_date[date]
)
```

### Same Period Last Year
**Purpose**: Crimes in the same period one year ago
```dax
Same Period Last Year = 
CALCULATE(
    [Total Crimes],
    SAMEPERIODLASTYEAR(dim_date[date])
)
```

### Last Month Crimes
**Purpose**: Total crimes in the previous month
```dax
Last Month Crimes = 
CALCULATE(
    [Total Crimes],
    PREVIOUSMONTH(dim_date[date])
)
```

---

## Percentages & Ratios

### Arrest Rate
**Purpose**: Percentage of crimes resulting in arrest
```dax
Arrest Rate = 
VAR TotalCrimes = [Total Crimes]
VAR TotalArrests = [Total Arrests]
RETURN
DIVIDE(TotalArrests, TotalCrimes, 0) * 100
```

### Arrest Rate (Formatted)
**Purpose**: Arrest rate with % symbol for display
```dax
Arrest Rate % = 
FORMAT([Arrest Rate], "0.0%")
```

### Domestic Crime %
**Purpose**: Percentage of crimes that are domestic
```dax
Domestic Crime % = 
DIVIDE(
    [Domestic Crimes],
    [Total Crimes],
    0
) * 100
```

### Crime Type Distribution %
**Purpose**: Percentage of each crime type
```dax
Crime Type % = 
VAR CurrentCrimeType = [Total Crimes]
VAR AllCrimes = 
    CALCULATE(
        [Total Crimes],
        ALL(dim_crime_type[primary_type])
    )
RETURN
DIVIDE(CurrentCrimeType, AllCrimes, 0) * 100
```

### District Crime Share
**Purpose**: Percentage of crimes in each district
```dax
District Crime Share = 
VAR DistrictCrimes = [Total Crimes]
VAR TotalAllDistricts = 
    CALCULATE(
        [Total Crimes],
        ALL(dim_location[district])
    )
RETURN
DIVIDE(DistrictCrimes, TotalAllDistricts, 0) * 100
```

---

## Comparisons & Changes

### YoY Change (Year-over-Year)
**Purpose**: Percentage change from previous year
```dax
YoY Change = 
VAR CurrentYear = [Total Crimes]
VAR PreviousYear = [Same Period Last Year]
RETURN
DIVIDE(
    CurrentYear - PreviousYear,
    PreviousYear,
    0
) * 100
```

### YoY Change (Formatted)
**Purpose**: YoY change with +/- and %
```dax
YoY Change (Formatted) = 
VAR Change = [YoY Change]
VAR FormattedValue = FORMAT(Change, "+0.0%;-0.0%;0.0%")
RETURN
FormattedValue
```

### MoM Change (Month-over-Month)
**Purpose**: Percentage change from previous month
```dax
MoM Change = 
VAR CurrentMonth = [Total Crimes]
VAR PreviousMonth = [Last Month Crimes]
RETURN
DIVIDE(
    CurrentMonth - PreviousMonth,
    PreviousMonth,
    0
) * 100
```

### QoQ Change (Quarter-over-Quarter)
**Purpose**: Percentage change from previous quarter
```dax
QoQ Change = 
VAR CurrentQuarter = [Crimes QTD]
VAR PreviousQuarter = 
    CALCULATE(
        [Crimes QTD],
        PREVIOUSQUARTER(dim_date[date])
    )
RETURN
DIVIDE(
    CurrentQuarter - PreviousQuarter,
    PreviousQuarter,
    0
) * 100
```

### Absolute Change YoY
**Purpose**: Absolute number difference from previous year
```dax
Absolute Change YoY = 
[Total Crimes] - [Same Period Last Year]
```

---

## Moving Averages & Trends

### 7-Day Moving Average
**Purpose**: Average crimes over last 7 days
```dax
7-Day MA = 
AVERAGEX(
    DATESINPERIOD(
        dim_date[date],
        LASTDATE(dim_date[date]),
        -7,
        DAY
    ),
    [Total Crimes]
)
```

### 30-Day Moving Average
**Purpose**: Average crimes over last 30 days
```dax
30-Day MA = 
AVERAGEX(
    DATESINPERIOD(
        dim_date[date],
        LASTDATE(dim_date[date]),
        -30,
        DAY
    ),
    [Total Crimes]
)
```

### 12-Month Rolling Average
**Purpose**: Average monthly crimes over last 12 months
```dax
12-Month Rolling Avg = 
AVERAGEX(
    DATESINPERIOD(
        dim_date[date],
        LASTDATE(dim_date[date]),
        -12,
        MONTH
    ),
    [Total Crimes]
)
```

### Trend Indicator
**Purpose**: Shows if crime is increasing or decreasing
```dax
Trend Indicator = 
VAR CurrentMonth = [Total Crimes]
VAR PreviousMonth = [Last Month Crimes]
VAR Change = CurrentMonth - PreviousMonth
RETURN
SWITCH(
    TRUE(),
    Change > 0, "📈 Increasing",
    Change < 0, "📉 Decreasing",
    "➡️ Stable"
)
```

---

## Geographic Metrics

### Crime Density (per 1000 population)
**Purpose**: Crimes per 1,000 residents
```dax
Crime Density = 
VAR TotalCrimes = [Total Crimes]
VAR Population = SUM(dim_location[population])
RETURN
DIVIDE(TotalCrimes, Population / 1000, 0)
```

### Crimes per Square Mile
**Purpose**: Crime concentration by area
```dax
Crimes per Sq Mile = 
VAR TotalCrimes = [Total Crimes]
VAR AreaSqMiles = SUM(dim_location[area_sq_miles])
RETURN
DIVIDE(TotalCrimes, AreaSqMiles, 0)
```

### High Crime District Flag
**Purpose**: Identify districts above average
```dax
High Crime District = 
VAR DistrictCrimes = [Total Crimes]
VAR AvgCrimes = 
    AVERAGEX(
        ALL(dim_location[district]),
        [Total Crimes]
    )
RETURN
IF(DistrictCrimes > AvgCrimes, "High", "Normal")
```

### Top N Districts (Dynamic)
**Purpose**: Rank districts by crime count
```dax
District Rank = 
RANKX(
    ALL(dim_location[district]),
    [Total Crimes],
    ,
    DESC,
    DENSE
)
```

---

## Crime Type Analytics

### Violent Crimes
**Purpose**: Count of violent crimes only
```dax
Violent Crimes = 
CALCULATE(
    [Total Crimes],
    dim_crime_type[is_violent] = TRUE()
)
```

### Property Crimes
**Purpose**: Count of property crimes only
```dax
Property Crimes = 
CALCULATE(
    [Total Crimes],
    dim_crime_type[is_property] = TRUE()
)
```

### Violent Crime Rate
**Purpose**: Percentage of violent crimes
```dax
Violent Crime Rate = 
DIVIDE(
    [Violent Crimes],
    [Total Crimes],
    0
) * 100
```

### Average Severity
**Purpose**: Average severity level of crimes
```dax
Average Severity = 
AVERAGE(dim_crime_type[severity_level])
```

### High Severity Crimes
**Purpose**: Count of severity level 4 or 5
```dax
High Severity Crimes = 
CALCULATE(
    [Total Crimes],
    dim_crime_type[severity_level] >= 4
)
```

---

## Operational KPIs

### Clearance Rate
**Purpose**: Percentage of crimes solved/cleared
```dax
Clearance Rate = 
VAR Cleared = 
    CALCULATE(
        COUNTROWS(fact_crimes),
        dim_arrest[arrest_status] = "Yes"
    )
VAR Total = [Total Crimes]
RETURN
DIVIDE(Cleared, Total, 0) * 100
```

### Average Days to Arrest
**Purpose**: Average time from crime to arrest
```dax
Avg Days to Arrest = 
CALCULATE(
    AVERAGE(dim_arrest[days_to_arrest]),
    dim_arrest[arrest_status] = "Yes"
)
```

### Response Time (simulated)
**Purpose**: Average response time in minutes
```dax
Avg Response Time = 
AVERAGE(fact_crimes[response_time_minutes])
```

### Cases Pending
**Purpose**: Count of unresolved cases
```dax
Cases Pending = 
CALCULATE(
    COUNTROWS(fact_crimes),
    dim_arrest[arrest_status] = "Pending"
)
```

### Case Resolution %
**Purpose**: Percentage of cases resolved
```dax
Case Resolution % = 
VAR Resolved = 
    CALCULATE(
        COUNTROWS(fact_crimes),
        dim_arrest[disposition] <> BLANK()
    )
VAR Total = [Total Crimes]
RETURN
DIVIDE(Resolved, Total, 0) * 100
```

---

## Advanced Analytics

### Crime Prediction (Simple Linear)
**Purpose**: Basic forecast based on trend
```dax
Crime Forecast = 
VAR HistoricalAvg = [12-Month Rolling Avg]
VAR Trend = [YoY Change] / 100
RETURN
HistoricalAvg * (1 + Trend)
```

### Risk Score
**Purpose**: Composite risk indicator (0-100)
```dax
Risk Score = 
VAR CrimeDensity = [Crime Density]
VAR MaxDensity = 
    MAXX(
        ALL(dim_location),
        [Crime Density]
    )
VAR ViolentRate = [Violent Crime Rate]
VAR TrendFactor = IF([YoY Change] > 0, 1.2, 0.8)
RETURN
MINX(
    {100},
    (CrimeDensity / MaxDensity * 50 + ViolentRate * 0.5) * TrendFactor
)
```

### Seasonal Index
**Purpose**: Compare current period to seasonal average
```dax
Seasonal Index = 
VAR CurrentMonthCrimes = [Total Crimes]
VAR HistoricalSameMonth = 
    CALCULATE(
        AVERAGE(fact_crimes[crime_count]),
        FILTER(
            ALL(dim_date),
            dim_date[month] = MAX(dim_date[month])
        )
    )
RETURN
DIVIDE(CurrentMonthCrimes, HistoricalSameMonth, 0) * 100
```

### Contribution to Total
**Purpose**: Percentage contribution of filtered context
```dax
% of Total = 
DIVIDE(
    [Total Crimes],
    CALCULATE(
        [Total Crimes],
        ALL()
    ),
    0
) * 100
```

### Cumulative Crimes
**Purpose**: Running total of crimes
```dax
Cumulative Crimes = 
CALCULATE(
    [Total Crimes],
    FILTER(
        ALL(dim_date[date]),
        dim_date[date] <= MAX(dim_date[date])
    )
)
```

### Crimes vs Target
**Purpose**: Compare actual to target
```dax
Crimes vs Target = 
VAR ActualCrimes = [Total Crimes]
VAR Target = 10000  // Set your target
RETURN
ActualCrimes - Target
```

---

## Conditional Formatting Measures

### Arrest Rate Color
**Purpose**: Color coding for arrest rate KPI
```dax
Arrest Rate Color = 
VAR Rate = [Arrest Rate]
RETURN
SWITCH(
    TRUE(),
    Rate >= 30, "#2ECC71",  // Green - Good
    Rate >= 20, "#F39C12",  // Orange - Average
    "#E74C3C"               // Red - Needs Improvement
)
```

### YoY Change Color
**Purpose**: Color for increase/decrease
```dax
YoY Change Color = 
IF(
    [YoY Change] < 0,
    "#2ECC71",  // Green - Crime decreased
    IF(
        [YoY Change] > 5,
        "#E74C3C",  // Red - Significant increase
        "#F39C12"   // Orange - Slight increase
    )
)
```

---

## Filter Context Helpers

### Selected District
**Purpose**: Show currently selected district name
```dax
Selected District = 
IF(
    HASONEVALUE(dim_location[district_name]),
    SELECTEDVALUE(dim_location[district_name]),
    "All Districts"
)
```

### Selected Time Period
**Purpose**: Display selected date range
```dax
Selected Period = 
VAR MinDate = MIN(dim_date[date])
VAR MaxDate = MAX(dim_date[date])
RETURN
FORMAT(MinDate, "MMM DD, YYYY") & " - " & FORMAT(MaxDate, "MMM DD, YYYY")
```

### Filter Count
**Purpose**: Show number of active filters
```dax
Active Filters = 
VAR Filters = 
    COUNTROWS(FILTERS(dim_crime_type[primary_type])) +
    COUNTROWS(FILTERS(dim_location[district])) +
    COUNTROWS(FILTERS(dim_date[year]))
RETURN
IF(Filters > 0, "Filters: " & Filters, "No Filters")
```

---

## Performance Optimization Tips

### Use Variables
```dax
// Good - Uses variable
Optimized Measure = 
VAR TotalCrimes = [Total Crimes]
RETURN
DIVIDE(TotalCrimes, [Total Arrests], 0)

// Avoid - Calculates Total Crimes twice
Unoptimized Measure = 
DIVIDE([Total Crimes], [Total Arrests], 0)
```

### Filter Context
```dax
// Good - Efficient filter
Efficient Filter = 
CALCULATE(
    [Total Crimes],
    dim_crime_type[is_violent] = TRUE()
)

// Avoid - Expensive filter
Inefficient Filter = 
FILTER(
    ALL(fact_crimes),
    RELATED(dim_crime_type[is_violent]) = TRUE()
)
```

---

## Notes & Best Practices

1. **Naming Convention**: Use clear, descriptive names
2. **Comments**: Add comments for complex formulas
3. **Variables**: Use VAR for readability and performance
4. **Error Handling**: Use DIVIDE with default value instead of division operator
5. **Format Strings**: Set appropriate format strings in measure properties
6. **Testing**: Test measures with different filter contexts
7. **Documentation**: Keep this document updated with new measures

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 2.0 | Dec 2024 | Added advanced analytics section | Data Team |
| 1.5 | Sep 2024 | Added geographic metrics | Data Team |
| 1.0 | Jun 2024 | Initial DAX measures | Data Team |

---

## Contact

For questions about these DAX measures:
- **Email**: your.email@example.com
- **Documentation**: See main README.md
- **Last Updated**: December 2024
