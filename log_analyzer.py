#!/usr/bin/env python3
"""
Network Log Analyzer & Reporter
Author: Jovin Nyarwango
Description: Automates the parsing of raw network logs, isolates ERROR levels,
             identifies high-frequency error-generating IPs, and exports reports.
"""

import re
import csv
from collections import Counter

# Regular expression to parse the log: Timestamp | Log Level | Message (with IP isolation)
# Matches format: YYYY-MM-DD HH:MM:SS LEVEL Message
LOG_PATTERN = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) '
    r'(?P<level>INFO|WARNING|ERROR) '
    r'(?P<message>.*)'
)

# Regex to safely extract IP addresses from log messages
IP_PATTERN = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

def analyze_logs(log_file_path, output_csv_path):
    print(f"[*] Starting analysis on: {log_file_path}")
    
    total_logs = 0
    error_count = 0
    warning_count = 0
    info_count = 0
    
    error_ips = []
    error_records = []

    try:
        with open(log_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                total_logs += 1
                match = LOG_PATTERN.match(line)
                
                if match:
                    data = match.groupdict()
                    level = data['level']
                    message = data['message']
                    timestamp = data['timestamp']
                    
                    # Track log level distributions
                    if level == 'ERROR':
                        error_count += 1
                        # Find if there is an IP in this error message
                        ip_match = IP_PATTERN.search(message)
                        ip_address = ip_match.group(0) if ip_match else "Unknown"
                        
                        if ip_address != "Unknown":
                            error_ips.append(ip_address)
                            
                        # Save details for the CSV report
                        error_records.append({
                            'Timestamp': timestamp,
                            'Level': level,
                            'Source_IP': ip_address,
                            'Message': message
                        })
                        
                    elif level == 'WARNING':
                        warning_count += 1
                    elif level == 'INFO':
                        info_count += 1

        # Calculate high-frequency offenders (IPs causing the most errors)
        ip_frequencies = Counter(error_ips)
        most_common_ips = ip_frequencies.most_common(3)

        # Output analysis terminal summary
        print("\n" + "="*40)
        print("          ANALYSIS SUMMARY")
        print("="*40)
        print(f"Total Log Lines Processed : {total_logs}")
        print(f"INFO Logs                 : {info_count}")
        print(f"WARNING Logs              : {warning_count}")
        print(f"ERROR Logs                : {error_count}")
        print("-"*40)
        print("Top IP Addresses Generating Errors:")
        for ip, count in most_common_ips:
            print(f" - {ip} : {count} occurrences")
        print("="*40)

        # Write the isolated errors to a CSV report
        if error_records:
            with open(output_csv_path, 'w', newline='') as csvfile:
                fieldnames = ['Timestamp', 'Level', 'Source_IP', 'Message']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(error_records)
            print(f"\n[+] Detailed error report exported successfully to: {output_csv_path}\n")
        else:
            print("\n[!] No ERRORS found. CSV report was not created.")

    except FileNotFoundError:
        print(f"[Error] The file path '{log_file_path}' does not exist.")
    except Exception as e:
        print(f"[Error] An unexpected failure occurred: {e}")

if __name__ == "__main__":
    # Define input and output targets
    log_input = "network_traffic.log"
    csv_output = "critical_errors_report.csv"
    
    analyze_logs(log_input, csv_output)