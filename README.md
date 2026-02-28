# CurrencyConverter
A live currency conversion web app built with Flask and vanilla JavaScript.

Fetches real-time exchange rates from the ExchangeRate-API and caches them for 24 hours to minimize API calls. Supports 160+ world currencies with full names and symbols. Users can type an amount or use the built-in numpad, and conversions update instantly as inputs change. The current exchange rate and last-updated timestamp are displayed alongside the result.

## Features
- Live exchange rates via ExchangeRate-API (24-hour cache)
- 160+ currencies with names and symbols
- Real-time conversion as you type or use the numpad
- Dark-themed single-page UI built with HTML/CSS/JavaScript
- Flask backend serving rates and currency metadata to the frontend

## Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **API:** ExchangeRate-API (v6)
