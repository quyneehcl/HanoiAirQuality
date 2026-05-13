"""
DATA1010 Final Project - Hanoi Air Quality
Source: Open-Meteo API (Weather Archive + Air Quality)
 
Features
--------
Compulsory (6):
  temperature, humidity, wind_speed, pressure, hour, day_of_week
 
Backup (4):
  is_weekend, wind_direction, precipitation, cloud_cover
 
Target:
  is_warning = 1 if AQI > 100 else 0
 
Validation only (not used in model):
  aqi, pm25
"""

import requests
import pandas as pd
from datetime import datetime, timedelta


LAT = 21.0285   # Hanoi latitude
LON = 105.8542  # Hanoi longitude

# 6 months of hourly data (~4380 rows)
END_DATE   = datetime.today().strftime("%Y-%m-%d")
START_DATE = (datetime.today() - timedelta(days=180)).strftime("%Y-%m-%d")

OUTPUT_FILE = "hanoi_air_quality.csv"

# STEP 1: Fetch weather data
# Compulsory: temperature, humidity, wind_speed, pressure
# Backup:     wind_direction, precipitation, cloud_cover

def fetch_weather():
    print("Fetching weather data...")

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude":  LAT,
        "longitude": LON,
        "start_date": START_DATE,
        "end_date":   END_DATE,
        "hourly": ",".join([
            "temperature_2m",       # compulsory
            "relative_humidity_2m", # compulsory
            "wind_speed_10m",       # compulsory (km/h → convert to m/s)
            "surface_pressure",     # compulsory
            "wind_direction_10m",   # backup
            "precipitation",        # backup
            "cloud_cover",          # backup
        ]),
        "timezone": "Asia/Bangkok",  # UTC+7
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()["hourly"]

    df = pd.DataFrame({
        "timestamp":       data["time"],
        # Compulsory
        "temperature":     data["temperature_2m"],
        "humidity":        data["relative_humidity_2m"],
        "wind_speed":      [x / 3.6 if x is not None else None
                            for x in data["wind_speed_10m"]],  # km/h → m/s
        "pressure":        data["surface_pressure"],
        # Backup
        "wind_direction":  data["wind_direction_10m"],   # degrees (0–360)
        "precipitation":   data["precipitation"],         # mm
        "cloud_cover":     data["cloud_cover"],           # %
    })

    print(f"  ✅ Weather data: {len(df)} rows")
    return df

# STEP 2: Fetch air quality data
# AQI → target variable
# PM2.5 → validation only

def fetch_air_quality():
    print("Fetching air quality data...")

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude":   LAT,
        "longitude":  LON,
        "start_date": START_DATE,
        "end_date":   END_DATE,
        "hourly":     "us_aqi,pm2_5",
        "timezone":   "Asia/Bangkok",
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()["hourly"]

    df = pd.DataFrame({
        "timestamp": data["time"],
        "aqi":       data["us_aqi"],   # used to compute target
        "pm25":      data["pm2_5"],    # validation only
    })

    print(f"  ✅ Air quality data: {len(df)} rows")
    return df

# STEP 3: Merge + derive features + clean
def process_data(weather_df, air_df):
    print("Merging and processing data...")

    # Merge on timestamp
    df = pd.merge(weather_df, air_df, on="timestamp", how="inner")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Derive time features
    df["hour"]          = df["timestamp"].dt.hour         # compulsory
    df["day_of_week"]   = df["timestamp"].dt.dayofweek   # backup (0=Mon, 6=Sun)
    df["is_weekend"]    = (df["day_of_week"] >= 5).astype(int)  # backup

    # Target variable: AQI > 100 = Warning level
    df["is_warning"] = (df["aqi"] > 100).astype(int)

    # Drop rows with any missing values
    before = len(df)
    df = df.dropna().reset_index(drop=True)
    print(f"  Dropped {before - len(df)} rows with missing values")

    # Final column order
    df = df[[
        "timestamp",
        # --- Compulsory features ---
        "temperature",      # °C
        "humidity",         # %
        "wind_speed",       # m/s
        "pressure",         # hPa
        "hour",             # 0–23
        # --- Backup features ---
        "day_of_week",      # 0–6
        "is_weekend",       # 0/1
        "wind_direction",   # degrees
        "precipitation",    # mm
        "cloud_cover",      # %
        # --- Target ---
        "is_warning",       # 0/1
        # --- Validation only (do NOT use in model) ---
        "aqi",
        "pm25",
    ]]

    return df

# STEP 4: Summary
def summarize(df):
    print("\n=== Dataset Summary ===")
    print(f"Total rows : {len(df)}")
    print(f"Date range : {df['timestamp'].min()} → {df['timestamp'].max()}")

    print(f"\nMissing values:\n{df.isnull().sum()}")

    compulsory = ["temperature", "humidity", "wind_speed", "pressure", "hour"]
    backup     = ["day_of_week", "is_weekend", "wind_direction", "precipitation", "cloud_cover"]

    print(f"\nCompulsory feature stats:")
    print(df[compulsory].describe().round(2))

    print(f"\nBackup feature stats:")
    print(df[backup].describe().round(2))

    counts = df["is_warning"].value_counts()
    total  = len(df)
    print(f"\nTarget distribution:")
    print(f"  No warning (0): {counts.get(0,0):>5} samples  ({100*counts.get(0,0)//total}%)")
    print(f"  Warning    (1): {counts.get(1,0):>5} samples  ({100*counts.get(1,0)//total}%)")

    if total >= 100:
        print(f"\n✅ Sufficient data: {total} samples")
    else:
        print(f"\n⚠️  Only {total} samples — increase DAYS_BACK")

    print(f"\nPreview (first 5 rows):")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    print(f"Collecting Hanoi AQI data: {START_DATE} → {END_DATE}\n")

    weather_df = fetch_weather()
    air_df     = fetch_air_quality()
    df         = process_data(weather_df, air_df)

    summarize(df)

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ Saved to '{OUTPUT_FILE}'")
