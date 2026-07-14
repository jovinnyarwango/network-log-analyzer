# Network Log Analyzer & Reporter

A lightweight, automated Python utility designed to parse raw network log files, isolate critical system errors, and export structured data reports. This tool is built to bridge traditional Network Operations Center (NOC) log monitoring with modern DevOps/SysOps troubleshooting workflows.

## Features
- **Regex-Based Parsing:** Efficiently scans syslog-style logs to extract timestamps, log levels, and messages.
- **Anomalous IP Tracking:** Leverages regular expressions to isolate IP addresses tied to connection timeouts or unauthorized access.
- **Automatic Report Generation:** Compiles and exports structured, clean `critical_errors_report.csv` files.
- **Console Dashboard:** Outputs a clean execution summary of network health directly to the terminal.

## Technologies Used
- **Language:** Python 3.x
- **Libraries:** `re` (Regular Expressions), `csv` (Data Export), `collections` (Frequency Analysis)

## How It Works
The script processes raw logs line-by-line, matching them against a strict pattern:
`YYYY-MM-DD HH:MM:SS [LEVEL] [MESSAGE]`

If an `ERROR` flag is raised, the script isolates the source IP and writes the entry to an automated report.

## How to Run This Project

1. **Clone this repository:**
   ```bash
   git clone https://github.com/jovinnyarwango/network-log-analyzer.git
   cd network-log-analyzer