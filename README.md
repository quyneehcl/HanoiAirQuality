Intro to Data Science Final Project
# Predicting Hanoi Air Quality Warnings
This project investigates whether weather and time-related conditions can predict hourly air-quality warning events in Hanoi using supervised and unsupervised machine learning techniques.

## Team Members

Group C

- Bui Anh Minh
- Dam Viet Thanh
- Dang Dang Minh
- Huynh Le Hoang Ngoc
- Le Hai Ngoc
- Nguyen Hoang Minh Tri
- Nguyen Minh Quyen
- Pham Thao Linh
- Tran Tuan Phong

## Research Questions

### Task 2 (Supervised Learning)

Can weather and time-related features predict whether Hanoi’s hourly air quality reaches a warning level?

### Task 3 (Unsupervised Learning)

Can hourly weather observations be clustered into distinct meteorological regimes, and do these regimes correspond to different air-quality warning risks?

## Dataset

Source:
- Open-Meteo Weather Archive API
- Open-Meteo Air Quality API

Location:
- Hanoi, Vietnam

Period:
- January 1, 2025 – December 31, 2025

Observations:
- 8,760 hourly records

### Compulsory Features

Weather:
- Temperature
- Humidity
- Wind Speed
- Pressure

Time:
- Hour
- Day of Week

Air Quality:
- AQI
- PM2.5

## Notebook Rendering

If GitHub fails to render the notebooks, view them using:
https://nbviewer.org/github/quyneehcl/HanoiAirQuality

## References

[1] Open-Meteo. (2025). *Open-Meteo Weather Archive and Air Quality API*. Licensed under CC BY 4.0. Available at: https://open-meteo.com

[2] AQICN. *AQI Scale*. Available at: https://aqicn.org/scale/vn/

[3] Nguyen, et al. (2024). *An exploration of meteorological effects on PM2.5 air quality in several provinces and cities in Vietnam*. Journal of Environmental Sciences, 145, 139–151. Available at: https://doi.org/10.1016/j.jes.2023.07.020