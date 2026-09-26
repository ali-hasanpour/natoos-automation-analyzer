# Natoos & GoSafir Automation & Security Analysis

A multi-threaded Python automation engine built to analyze, parse, and interact with specific institutional endpoints, demonstrating dynamic token generation, session handling, and credential management.

## 🛠️ Technical Overview & Architecture

This project automates a multi-step verification and profile retrieval sequence across API endpoints:

1. **Dynamic Session Initialization (`GetIframeToken`)**: 
   - Dynamically fetches fresh iframe tokens, URL-encodes them, and formats authorization characters to match browser security constraints.
2. **Receipt Data Scraping (`GetPlacementReceipt`)**: 
   - Scans and extracts personal records, registration dates, levels, and unique National Codes from HTML responses using robust regex patterns.
3. **Automated Credential Generation (`CreateToken`)**: 
   - Programmatically exchanges extracted identifiers (`NationalCode`) to mint active session JWT Bearer tokens.
4. **Authenticated Profile Retrieval (`GetUserInfo`)**: 
   - Queries user profile endpoints using authenticated headers to compile comprehensive records.

## ⚡ Performance & Features
- **High-Speed Concurrency**: Built with Python's `ThreadPoolExecutor` to support scalable multi-threaded checking.
- **Live Terminal Telemetry**: Real-time tracking of processed items, operational speed (Checks-Per-Second), and success/failure distribution.
- **Structured Logging**: Clean separation of valid matches and error tracking.

## ⚠️ Disclaimer
This research and tooling were developed for educational and authorized auditing purposes only. All testing was performed with explicit permission.