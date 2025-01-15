# API Documentation

## Overview
This API provides access to climate data, including precipitation measurements, station data, and temperature statistics. The data is sourced from a SQLite database containing historical climate data for Hawaii.

## Endpoints

### 1. Get All Precipitation Measurements
- **Endpoint:** `/measurements`
- **Method:** `GET`
- **Description:** Retrieves all precipitation measurements data.
- **Response:**
  ```json
  [
    {
      "id": 1,
      "station": "USC00519397",
      "date": "2010-01-01",
      "prcp": 0.08,
      "tobs": 65
    },
    ...
  ]
  ```
- **Example Usage:**
  ```bash
  curl http://<your-domain>/api/v1.0/measurements
  ```

### 2. Get All Station Data
- **Endpoint:** `/stations`
- **Method:** `GET`
- **Description:** Retrieves all station data.
- **Response:**
  ```json
  [
    {
      "id": 1,
      "station": "USC00519397",
      "name": "WAIKIKI 717.2, HI US",
      "latitude": 21.2716,
      "longitude": -157.8168,
      "elevation": 3.0
    },
    ...
  ]
  ```
- **Example Usage:**
  ```bash
  curl http://<your-domain>/api/v1.0/stations
  ```

### 3. Get All Measurements with Station Data
- **Endpoint:** `/measurements_Stations`
- **Method:** `GET`
- **Description:** Retrieves all measurements data along with station information.
- **Response:**
  ```json
  [
    {
      "date": "2010-01-01",
      "id": 1,
      "station": "USC00519397",
      "name": "WAIKIKI 717.2, HI US",
      "latitude": 21.2716,
      "longitude": -157.8168,
      "prcp": 0.08,
      "tobs": 65
    },
    ...
  ]
  ```
- **Example Usage:**
  ```bash
  curl http://<your-domain>/api/v1.0/measurements_Stations
  ```

### 4. Get Measurements with Station Data within a Date Range
- **Endpoint:** `/measurements_StationsInRange/<start_date>/<end_date>`
- **Method:** `GET`
- **Description:** Retrieves measurements data along with station information within a specified date range.
- **URL Parameters:**
  - `start_date` (string): Start date in `YYYY-MM-DD` format.
  - `end_date` (string): End date in `YYYY-MM-DD` format.
- **Response:**
  ```json
  [
    {
      "date": "2010-01-01",
      "id": 1,
      "station": "USC00519397",
      "name": "WAIKIKI 717.2, HI US",
      "latitude": 21.2716,
      "longitude": -157.8168,
      "prcp": 0.08,
      "tobs": 65
    },
    ...
  ]
  ```
- **Example Usage:**
  ```bash
  curl http://<your-domain>/api/v1.0/measurements_StationsInRange/2010-01-01/2010-12-31
  ```

### 5. Get Temperature Statistics for a Date Range
- **Endpoint:** `/temp_stats/<start>/<end>`
- **Method:** `GET`
- **Description:** Retrieves temperature statistics (min, avg, max) for a specified date range.
- **URL Parameters:**
  - `start` (string): Start date in `YYYY-MM-DD` format.
  - `end` (string): End date in `YYYY-MM-DD` format.
- **Response:**
  ```json
  {
    "Start Date": "2010-01-01",
    "End Date": "2010-12-31",
    "Minimum recorded Temperature": 56,
    "Average recorded Temperature": 74.5,
    "Maximum recorded Temperature": 87
  }
  ```
- **Example Usage:**
  ```bash
  curl http://<your-domain>/api/v1.0/temp_stats/2010-01-01/2010-12-31
  ```

### 6. Get Temperature Statistics for a Specific Station within a Date Range
- **Endpoint:** `/temp_stats_station/<station>/<start>/<end>`
- **Method:** `GET`
- **Description:** Retrieves temperature statistics (min, avg, max) for a specific station within a specified date range.
- **URL Parameters:**
  - `station` (string): Station ID.
  - `start` (string): Start date in `YYYY-MM-DD` format.
  - `end` (string): End date in `YYYY-MM-DD` format.
- **Response:**
  ```json
  {
    "Station": "USC00519397",
    "Start Date": "2010-01-01",
    "End Date": "2010-12-31",
    "Minimum recorded Temperature": 56,
    "Average recorded Temperature": 74.5,
    "Maximum recorded Temperature": 87
  }
  ```
- **Example Usage:**
  ```bash
  curl http://<your-domain>/api/v1.0/temp_stats_station/USC00519397/2010-01-01/2010-12-31
  ```

## Error Handling
The API returns the following error codes:

- **400 Bad Request:** Invalid input or date out of range.
- **404 Not Found:** Resource not found.
- **500 Internal Server Error:** An error occurred on the server.

## Notes
- Ensure that the date format is `YYYY-MM-DD`.
- The date range should be within the dataset's range.
```
