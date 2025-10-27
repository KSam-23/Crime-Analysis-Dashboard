# Data Dictionary - Crime Analysis Dataset

## Overview
This document provides detailed information about all data fields used in the Crime Analysis Dashboard project.

---

## Fact Table: `fact_crimes`

| Column Name | Data Type | Description | Example | Constraints |
|------------|-----------|-------------|---------|-------------|
| `crime_id` | VARCHAR(20) | Unique identifier for each crime incident | RD12345678 | Primary Key, NOT NULL |
| `date_key` | INT | Foreign key to date dimension | 20240115 | Foreign Key, NOT NULL |
| `location_key` | INT | Foreign key to location dimension | 1001 | Foreign Key, NOT NULL |
| `crime_type_key` | INT | Foreign key to crime type dimension | 501 | Foreign Key, NOT NULL |
| `case_number` | VARCHAR(15) | Police department case number | JA123456 | Unique, NOT NULL |
| `incident_datetime` | DATETIME | Date and time when crime occurred | 2024-01-15 14:30:00 | NOT NULL |
| `arrest_made` | BOOLEAN | Whether an arrest was made | TRUE/FALSE | Default: FALSE |
| `domestic` | BOOLEAN | Whether crime was domestic-related | TRUE/FALSE | Default: FALSE |
| `fbi_code` | VARCHAR(5) | FBI Uniform Crime Report code | 01A | - |
| `description` | VARCHAR(255) | Detailed description of the crime | THEFT - OVER $500 | - |
| `location_description` | VARCHAR(100) | Type of location where crime occurred | STREET, RESIDENCE, RETAIL | - |
| `beat` | VARCHAR(10) | Police beat number | 1234 | - |
| `district` | VARCHAR(5) | Police district number | 015 | - |
| `ward` | INT | City ward number | 42 | Range: 1-50 |
| `latitude` | DECIMAL(10,7) | Latitude coordinate | 41.8781136 | Range: -90 to 90 |
| `longitude` | DECIMAL(10,7) | Longitude coordinate | -87.6297982 | Range: -180 to 180 |
| `x_coordinate` | INT | X coordinate (State Plane) | 1176365 | - |
| `y_coordinate` | INT | Y coordinate (State Plane) | 1901428 | - |
| `updated_on` | DATETIME | Last update timestamp | 2024-01-15 15:00:00 | - |

---

## Dimension Table: `dim_date`

| Column Name | Data Type | Description | Example | Constraints |
|------------|-----------|-------------|---------|-------------|
| `date_key` | INT | Surrogate key (YYYYMMDD format) | 20240115 | Primary Key |
| `date` | DATE | Calendar date | 2024-01-15 | NOT NULL, Unique |
| `year` | INT | Year | 2024 | NOT NULL |
| `quarter` | INT | Quarter of year | 1 | Range: 1-4 |
| `quarter_name` | VARCHAR(10) | Quarter label | Q1 2024 | - |
| `month` | INT | Month number | 1 | Range: 1-12 |
| `month_name` | VARCHAR(20) | Month name | January | - |
| `month_short` | VARCHAR(5) | Short month name | Jan | - |
| `week` | INT | Week of year | 3 | Range: 1-53 |
| `day` | INT | Day of month | 15 | Range: 1-31 |
| `day_of_week` | INT | Day number (1=Sunday) | 2 | Range: 1-7 |
| `day_name` | VARCHAR(15) | Day of week name | Monday | - |
| `day_short` | VARCHAR(5) | Short day name | Mon | - |
| `is_weekend` | BOOLEAN | Weekend indicator | FALSE | - |
| `is_holiday` | BOOLEAN | Holiday indicator | FALSE | - |
| `holiday_name` | VARCHAR(50) | Name of holiday (if applicable) | New Year's Day | - |
| `fiscal_year` | INT | Fiscal year | 2024 | - |
| `fiscal_quarter` | INT | Fiscal quarter | 2 | Range: 1-4 |
| `season` | VARCHAR(10) | Season name | Winter | Winter/Spring/Summer/Fall |
| `hour` | INT | Hour of day | 14 | Range: 0-23 |
| `hour_range` | VARCHAR(20) | Hour range category | 12 PM - 3 PM | - |
| `time_of_day` | VARCHAR(15) | Time period | Afternoon | Morning/Afternoon/Evening/Night |

---

## Dimension Table: `dim_location`

| Column Name | Data Type | Description | Example | Constraints |
|------------|-----------|-------------|---------|-------------|
| `location_key` | INT | Surrogate key | 1001 | Primary Key |
| `district` | VARCHAR(5) | Police district code | 015 | NOT NULL |
| `district_name` | VARCHAR(50) | Full district name | Central District | - |
| `beat` | VARCHAR(10) | Police beat number | 1534 | - |
| `ward` | INT | City ward number | 42 | Range: 1-50 |
| `community_area` | INT | Community area number | 32 | Range: 1-77 |
| `community_name` | VARCHAR(50) | Community area name | Loop | - |
| `zip_code` | VARCHAR(10) | ZIP code | 60601 | - |
| `neighborhood` | VARCHAR(50) | Neighborhood name | Downtown | - |
| `latitude` | DECIMAL(10,7) | Latitude | 41.8781136 | - |
| `longitude` | DECIMAL(10,7) | Longitude | -87.6297982 | - |
| `geometry` | GEOMETRY | Spatial geometry point | POINT(...) | - |
| `location_type` | VARCHAR(50) | Type of location | STREET, RESIDENCE | - |
| `population` | INT | Area population | 29,283 | - |
| `area_sq_miles` | DECIMAL(8,2) | Area in square miles | 1.46 | - |
| `density` | INT | Population density per sq mile | 20,055 | - |
| `median_income` | DECIMAL(12,2) | Median household income | 68,403.00 | - |
| `police_station` | VARCHAR(100) | Nearest police station | Central Station | - |
| `station_address` | VARCHAR(150) | Police station address | 1718 S State St | - |

---

## Dimension Table: `dim_crime_type`

| Column Name | Data Type | Description | Example | Constraints |
|------------|-----------|-------------|---------|-------------|
| `crime_type_key` | INT | Surrogate key | 501 | Primary Key |
| `iucr_code` | VARCHAR(10) | Illinois UCR code | 0486 | Unique |
| `primary_type` | VARCHAR(100) | Primary crime classification | BATTERY | NOT NULL |
| `description` | VARCHAR(255) | Detailed description | DOMESTIC BATTERY SIMPLE | - |
| `fbi_code` | VARCHAR(5) | FBI classification code | 08B | - |
| `category` | VARCHAR(50) | Crime category | Violent Crime | NOT NULL |
| `severity_level` | INT | Severity rating (1-5) | 3 | Range: 1-5 |
| `severity_label` | VARCHAR(20) | Severity description | Medium | Low/Medium/High/Critical |
| `ucr_index` | VARCHAR(20) | UCR Part classification | Part I | Part I/Part II/Other |
| `is_violent` | BOOLEAN | Violent crime indicator | TRUE | - |
| `is_property` | BOOLEAN | Property crime indicator | FALSE | - |
| `maximum_penalty_years` | INT | Maximum prison sentence | 5 | - |
| `is_felony` | BOOLEAN | Felony classification | TRUE | - |
| `clearance_avg_days` | INT | Average days to clearance | 45 | - |

---

## Dimension Table: `dim_arrest`

| Column Name | Data Type | Description | Example | Constraints |
|------------|-----------|-------------|---------|-------------|
| `arrest_key` | INT | Surrogate key | 2001 | Primary Key |
| `arrest_status` | VARCHAR(20) | Arrest made (Yes/No/Pending) | Yes | NOT NULL |
| `arrest_date` | DATE | Date of arrest | 2024-01-16 | - |
| `days_to_arrest` | INT | Days from incident to arrest | 1 | - |
| `arrest_type` | VARCHAR(30) | Type of arrest | On-scene arrest | - |
| `officer_count` | INT | Number of officers involved | 2 | - |
| `charges_filed` | INT | Number of charges | 1 | - |
| `court_case_number` | VARCHAR(30) | Court case identifier | 2024-CF-001234 | - |
| `disposition` | VARCHAR(50) | Case outcome | Convicted | - |

---

## Measures & Calculations

### Key Performance Indicators (KPIs)

| Measure Name | Formula/Description | Example Value | Unit |
|-------------|---------------------|---------------|------|
| `Total Crimes` | Count of all crime records | 125,438 | Count |
| `Arrest Rate` | (Arrests / Total Crimes) × 100 | 21.3% | Percentage |
| `Response Time Avg` | Average minutes from call to arrival | 8.5 | Minutes |
| `Clearance Rate` | (Solved Cases / Total Cases) × 100 | 18.7% | Percentage |
| `Crime Density` | Crimes per 1,000 population | 42.3 | Per 1000 |
| `YoY Change` | ((Current - Previous) / Previous) × 100 | -12.5% | Percentage |

### Temporal Metrics

| Measure Name | Description | Example |
|-------------|-------------|---------|
| `MTD Crimes` | Month-to-date crime count | 3,245 |
| `QTD Crimes` | Quarter-to-date crime count | 9,876 |
| `YTD Crimes` | Year-to-date crime count | 98,234 |
| `30-Day Moving Avg` | 30-day rolling average | 342.5 |
| `Same Period Last Year` | Crimes in same period last year | 112,345 |

---

## Data Quality Rules

### Validation Rules

1. **Temporal Constraints**
   - `incident_datetime` must be <= current date
   - `arrest_date` must be >= `incident_datetime`
   - `updated_on` must be >= `incident_datetime`

2. **Geographic Constraints**
   - Latitude: -90 to 90
   - Longitude: -180 to 180
   - Ward: 1 to 50 (city-specific)
   - Community Area: 1 to 77 (city-specific)

3. **Business Rules**
   - If `arrest_made` = TRUE, then `arrest_date` must not be null
   - `days_to_arrest` must be >= 0
   - `severity_level` must be between 1 and 5

4. **Referential Integrity**
   - All foreign keys must reference existing dimension records
   - No orphan records in fact table

### Data Completeness Thresholds

| Field | Required | Completeness Target |
|-------|----------|-------------------|
| `crime_id` | Yes | 100% |
| `date_key` | Yes | 100% |
| `primary_type` | Yes | 100% |
| `latitude/longitude` | No | ≥ 95% |
| `arrest_made` | Yes | 100% |
| `description` | No | ≥ 90% |

---

## Data Sources

### Primary Sources
1. **City Police Department Open Data Portal**
   - API Endpoint: `https://data.cityname.org/api/crimes`
   - Update Frequency: Daily at 3:00 AM
   - Historical Data: 2001-Present

2. **FBI Uniform Crime Reporting (UCR)**
   - Crime Classification Codes
   - National Statistics for Benchmarking

### Supplementary Sources
3. **US Census Bureau**
   - Demographic Data
   - Population Estimates

4. **Municipal GIS Department**
   - District Boundaries
   - Community Area Shapefiles

---

## Data Refresh Schedule

| Dataset | Frequency | Time (CST) | Duration |
|---------|-----------|------------|----------|
| Crime Incidents | Daily | 3:00 AM | ~15 min |
| Demographics | Annually | January 1 | ~1 hour |
| Boundaries | As needed | - | ~30 min |
| Weather Data | Hourly | Every hour | ~2 min |

---

## Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 2.0 | 2024-12-01 | Added arrest dimension, expanded crime types | Data Team |
| 1.5 | 2024-09-01 | Added geographic hierarchy | Data Team |
| 1.0 | 2024-06-01 | Initial data model | Data Team |

---

## Contact for Data Issues

For questions or issues regarding this data:
- **Data Steward**: [Your Name]
- **Email**: your.email@example.com
- **Department**: Analytics Team
- **Last Updated**: December 2024

