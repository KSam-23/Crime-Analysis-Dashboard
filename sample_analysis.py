"""
Crime Data Analysis Script
==========================

This script demonstrates data extraction, cleaning, transformation, and analysis
of crime data for the Crime Analysis Dashboard project.

Author: [Your Name]
Date: December 2024
Version: 1.0
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')


class CrimeDataAnalyzer:
    """
    A comprehensive class for analyzing crime data with methods for
    data loading, cleaning, transformation, and statistical analysis.
    """

    def __init__(self, data_path: str = None):
        """
        Initialize the CrimeDataAnalyzer.

        Args:
            data_path: Path to the crime data CSV file
        """
        self.data_path = data_path
        self.df = None
        self.clean_df = None

    def load_data(self, data_path: str = None) -> pd.DataFrame:
        """
        Load crime data from CSV file.

        Args:
            data_path: Path to CSV file (optional if set during init)

        Returns:
            DataFrame containing the loaded data

        Example:
            >>> analyzer = CrimeDataAnalyzer()
            >>> df = analyzer.load_data('data/raw/crimes.csv')
        """
        path = data_path or self.data_path

        if path is None:
            raise ValueError("Data path must be provided")

        print(f"📊 Loading data from {path}...")

        try:
            self.df = pd.read_csv(path, parse_dates=['date'], low_memory=False)
            print(f"✅ Loaded {len(self.df):,} records")
            return self.df

        except FileNotFoundError:
            print(f"❌ Error: File not found at {path}")
            raise
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            raise

    def explore_data(self) -> dict:
        """
        Perform initial data exploration.

        Returns:
            Dictionary containing exploration statistics

        Example:
            >>> stats = analyzer.explore_data()
            >>> print(f"Total crimes: {stats['total_records']}")
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        print("\n" + "=" * 60)
        print("DATA EXPLORATION")
        print("=" * 60)

        stats = {
            'total_records': len(self.df),
            'columns': len(self.df.columns),
            'date_range': (self.df['date'].min(), self.df['date'].max()),
            'missing_values': self.df.isnull().sum().sum(),
            'duplicate_records': self.df.duplicated().sum()
        }

        # Display basic info
        print(f"\n📊 Dataset Overview:")
        print(f"   Total Records: {stats['total_records']:,}")
        print(f"   Total Columns: {stats['columns']}")
        print(f"   Date Range: {stats['date_range'][0]} to {stats['date_range'][1]}")
        print(f"   Missing Values: {stats['missing_values']:,}")
        print(f"   Duplicate Records: {stats['duplicate_records']:,}")

        # Column data types
        print(f"\n📋 Data Types:")
        print(self.df.dtypes.value_counts())

        # Missing values by column
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df) * 100).round(2)

        if missing.sum() > 0:
            print(f"\n⚠️  Columns with Missing Values:")
            missing_df = pd.DataFrame({
                'Missing': missing[missing > 0],
                'Percentage': missing_pct[missing > 0]
            })
            print(missing_df)

        return stats

    def clean_data(self) -> pd.DataFrame:
        """
        Clean the crime data by handling missing values, duplicates,
        and data quality issues.

        Returns:
            Cleaned DataFrame

        Example:
            >>> clean_df = analyzer.clean_data()
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        print("\n" + "=" * 60)
        print("DATA CLEANING")
        print("=" * 60)

        df = self.df.copy()

        # Remove exact duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        duplicates_removed = initial_count - len(df)
        print(f"✅ Removed {duplicates_removed:,} duplicate records")

        # Handle missing values
        # Strategy: Drop rows with missing critical fields, fill others
        critical_fields = ['date', 'primary_type', 'latitude', 'longitude']

        # Count rows that will be removed
        missing_critical = df[critical_fields].isnull().any(axis=1).sum()
        df = df.dropna(subset=critical_fields)
        print(f"✅ Removed {missing_critical:,} records with missing critical fields")

        # Fill missing non-critical fields
        if 'description' in df.columns:
            df['description'] = df['description'].fillna('UNKNOWN')

        if 'location_description' in df.columns:
            df['location_description'] = df['location_description'].fillna('UNKNOWN')

        # Convert boolean fields
        if 'arrest' in df.columns:
            df['arrest'] = df['arrest'].fillna(False).astype(bool)

        if 'domestic' in df.columns:
            df['domestic'] = df['domestic'].fillna(False).astype(bool)

        # Standardize text fields
        text_columns = df.select_dtypes(include=['object']).columns
        for col in text_columns:
            if col not in ['date']:
                df[col] = df[col].str.strip().str.upper()

        print(f"✅ Standardized text fields")
        print(f"📊 Clean dataset: {len(df):,} records")

        self.clean_df = df
        return self.clean_df

    def engineer_features(self) -> pd.DataFrame:
        """
        Create new features from existing data for analysis.

        Returns:
            DataFrame with engineered features

        Example:
            >>> df_features = analyzer.engineer_features()
        """
        if self.clean_df is None:
            raise ValueError("Data not cleaned. Call clean_data() first.")

        print("\n" + "=" * 60)
        print("FEATURE ENGINEERING")
        print("=" * 60)

        df = self.clean_df.copy()

        # Temporal features
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['month_name'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['is_weekend'] = df['day_of_week'].isin([5, 6])

        print(f"✅ Created temporal features")

        # Time of day categories
        def categorize_time(hour):
            if 6 <= hour < 12:
                return 'Morning'
            elif 12 <= hour < 18:
                return 'Afternoon'
            elif 18 <= hour < 24:
                return 'Evening'
            else:
                return 'Night'

        df['time_of_day'] = df['hour'].apply(categorize_time)
        print(f"✅ Created time of day categories")

        # Season
        def get_season(month):
            if month in [12, 1, 2]:
                return 'Winter'
            elif month in [3, 4, 5]:
                return 'Spring'
            elif month in [6, 7, 8]:
                return 'Summer'
            else:
                return 'Fall'

        df['season'] = df['month'].apply(get_season)
        print(f"✅ Created seasonal categories")

        # Crime severity (example logic)
        if 'primary_type' in df.columns:
            violent_crimes = ['HOMICIDE', 'ASSAULT', 'BATTERY', 'ROBBERY',
                            'CRIMINAL SEXUAL ASSAULT', 'KIDNAPPING']
            df['is_violent'] = df['primary_type'].isin(violent_crimes)
            print(f"✅ Created crime severity indicators")

        self.clean_df = df
        return self.clean_df

    def analyze_trends(self) -> dict:
        """
        Perform temporal trend analysis.

        Returns:
            Dictionary containing trend statistics

        Example:
            >>> trends = analyzer.analyze_trends()
        """
        if self.clean_df is None:
            raise ValueError("Data not prepared. Call clean_data() first.")

        print("\n" + "=" * 60)
        print("TREND ANALYSIS")
        print("=" * 60)

        df = self.clean_df

        # Yearly trends
        yearly_crimes = df.groupby('year').size()
        print("\n📊 Crimes by Year:")
        print(yearly_crimes)

        # Calculate year-over-year change
        yoy_change = yearly_crimes.pct_change() * 100
        print("\n📈 Year-over-Year Change (%):")
        print(yoy_change.round(2))

        # Monthly average
        monthly_avg = df.groupby(['year', 'month']).size().groupby('month').mean()
        print("\n📅 Average Crimes by Month:")
        print(monthly_avg.round(0))

        # Day of week patterns
        dow_crimes = df.groupby('day_name').size()
        print("\n📆 Crimes by Day of Week:")
        print(dow_crimes.sort_values(ascending=False))

        # Hourly patterns
        hourly_crimes = df.groupby('hour').size()
        print("\n⏰ Crimes by Hour of Day:")
        peak_hour = hourly_crimes.idxmax()
        print(f"   Peak hour: {peak_hour}:00 with {hourly_crimes.max():,} crimes")

        return {
            'yearly_crimes': yearly_crimes.to_dict(),
            'yoy_change': yoy_change.to_dict(),
            'monthly_avg': monthly_avg.to_dict(),
            'peak_hour': peak_hour
        }

    def analyze_crime_types(self) -> pd.DataFrame:
        """
        Analyze distribution of crime types.

        Returns:
            DataFrame with crime type statistics

        Example:
            >>> crime_stats = analyzer.analyze_crime_types()
        """
        if self.clean_df is None:
            raise ValueError("Data not prepared. Call clean_data() first.")

        print("\n" + "=" * 60)
        print("CRIME TYPE ANALYSIS")
        print("=" * 60)

        df = self.clean_df

        # Top crime types
        crime_counts = df['primary_type'].value_counts()
        crime_pct = (crime_counts / len(df) * 100).round(2)

        crime_analysis = pd.DataFrame({
            'Count': crime_counts,
            'Percentage': crime_pct
        })

        print("\n🔝 Top 10 Crime Types:")
        print(crime_analysis.head(10))

        # Arrest rates by crime type
        if 'arrest' in df.columns:
            arrest_rates = df.groupby('primary_type')['arrest'].mean() * 100
            arrest_rates = arrest_rates.sort_values(ascending=False)

            print("\n🚨 Arrest Rates by Crime Type (Top 10):")
            print(arrest_rates.head(10).round(2))

        return crime_analysis

    def analyze_geographic(self) -> dict:
        """
        Analyze geographic distribution of crimes.

        Returns:
            Dictionary with geographic statistics

        Example:
            >>> geo_stats = analyzer.analyze_geographic()
        """
        if self.clean_df is None:
            raise ValueError("Data not prepared. Call clean_data() first.")

        print("\n" + "=" * 60)
        print("GEOGRAPHIC ANALYSIS")
        print("=" * 60)

        df = self.clean_df

        # District analysis
        if 'district' in df.columns:
            district_crimes = df['district'].value_counts()
            print("\n🗺️  Top 10 Districts by Crime Count:")
            print(district_crimes.head(10))

        # Location type analysis
        if 'location_description' in df.columns:
            location_crimes = df['location_description'].value_counts()
            print("\n📍 Top 10 Location Types:")
            print(location_crimes.head(10))

        return {
            'district_crimes': district_crimes.to_dict() if 'district' in df.columns else None,
            'location_types': location_crimes.to_dict() if 'location_description' in df.columns else None
        }

    def calculate_kpis(self) -> dict:
        """
        Calculate key performance indicators.

        Returns:
            Dictionary of KPIs

        Example:
            >>> kpis = analyzer.calculate_kpis()
            >>> print(f"Arrest Rate: {kpis['arrest_rate']:.2f}%")
        """
        if self.clean_df is None:
            raise ValueError("Data not prepared. Call clean_data() first.")

        print("\n" + "=" * 60)
        print("KEY PERFORMANCE INDICATORS")
        print("=" * 60)

        df = self.clean_df

        kpis = {}

        # Total crimes
        kpis['total_crimes'] = len(df)

        # Arrest rate
        if 'arrest' in df.columns:
            kpis['arrest_rate'] = (df['arrest'].sum() / len(df) * 100)

        # Domestic crime percentage
        if 'domestic' in df.columns:
            kpis['domestic_pct'] = (df['domestic'].sum() / len(df) * 100)

        # Violent crime percentage
        if 'is_violent' in df.columns:
            kpis['violent_pct'] = (df['is_violent'].sum() / len(df) * 100)

        # Average crimes per day
        date_range_days = (df['date'].max() - df['date'].min()).days
        kpis['avg_crimes_per_day'] = len(df) / date_range_days

        # Display KPIs
        print("\n📊 Key Metrics:")
        print(f"   Total Crimes: {kpis.get('total_crimes', 0):,}")
        print(f"   Arrest Rate: {kpis.get('arrest_rate', 0):.2f}%")
        print(f"   Domestic Crimes: {kpis.get('domestic_pct', 0):.2f}%")
        print(f"   Violent Crimes: {kpis.get('violent_pct', 0):.2f}%")
        print(f"   Avg Crimes/Day: {kpis.get('avg_crimes_per_day', 0):.2f}")

        return kpis

    def export_clean_data(self, output_path: str):
        """
        Export cleaned and processed data to CSV.

        Args:
            output_path: Path where to save the cleaned data

        Example:
            >>> analyzer.export_clean_data('data/processed/crimes_clean.csv')
        """
        if self.clean_df is None:
            raise ValueError("No cleaned data to export. Call clean_data() first.")

        try:
            self.clean_df.to_csv(output_path, index=False)
            print(f"\n✅ Clean data exported to {output_path}")
            print(f"   Records: {len(self.clean_df):,}")
            print(f"   Columns: {len(self.clean_df.columns)}")
        except Exception as e:
            print(f"❌ Error exporting data: {str(e)}")
            raise

    def generate_summary_report(self) -> str:
        """
        Generate a comprehensive text summary report.

        Returns:
            String containing the full report

        Example:
            >>> report = analyzer.generate_summary_report()
            >>> print(report)
        """
        if self.clean_df is None:
            raise ValueError("Data not prepared. Call clean_data() first.")

        report = []
        report.append("=" * 70)
        report.append("CRIME DATA ANALYSIS SUMMARY REPORT")
        report.append("=" * 70)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # Dataset overview
        report.append("DATASET OVERVIEW")
        report.append("-" * 70)
        report.append(f"Total Records: {len(self.clean_df):,}")
        report.append(f"Date Range: {self.clean_df['date'].min()} to {self.clean_df['date'].max()}")
        report.append(f"Unique Crime Types: {self.clean_df['primary_type'].nunique()}")
        report.append("")

        # KPIs
        kpis = self.calculate_kpis()
        report.append("KEY PERFORMANCE INDICATORS")
        report.append("-" * 70)
        report.append(f"Arrest Rate: {kpis.get('arrest_rate', 0):.2f}%")
        report.append(f"Domestic Crimes: {kpis.get('domestic_pct', 0):.2f}%")
        report.append(f"Violent Crimes: {kpis.get('violent_pct', 0):.2f}%")
        report.append("")

        # Top crime types
        report.append("TOP 5 CRIME TYPES")
        report.append("-" * 70)
        top_crimes = self.clean_df['primary_type'].value_counts().head(5)
        for crime, count in top_crimes.items():
            pct = (count / len(self.clean_df) * 100)
            report.append(f"{crime}: {count:,} ({pct:.2f}%)")
        report.append("")

        report.append("=" * 70)

        return "\n".join(report)


def main():
    """
    Main function to demonstrate the CrimeDataAnalyzer usage.
    """
    print("\n" + "=" * 70)
    print("CRIME DATA ANALYSIS PIPELINE")
    print("=" * 70)

    # Initialize analyzer
    analyzer = CrimeDataAnalyzer()

    # Load sample data (replace with your actual data path)
    try:
        analyzer.load_data('data/raw/crimes.csv')
    except Exception as e:
        print(f"\n⚠️  Could not load data: {str(e)}")
        print("Please ensure data file exists at 'data/raw/crimes.csv'")
        return

    # Explore data
    analyzer.explore_data()

    # Clean data
    analyzer.clean_data()

    # Engineer features
    analyzer.engineer_features()

    # Run analyses
    analyzer.analyze_trends()
    analyzer.analyze_crime_types()
    analyzer.analyze_geographic()
    analyzer.calculate_kpis()

    # Generate report
    report = analyzer.generate_summary_report()
    print("\n" + report)

    # Export clean data
    try:
        analyzer.export_clean_data('data/processed/crimes_clean.csv')
    except Exception as e:
        print(f"Could not export data: {str(e)}")

    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
