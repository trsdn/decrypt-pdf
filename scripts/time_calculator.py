#!/usr/bin/env python3
import math

def calculate_crack_time():
    """Calculate estimated cracking times for various password patterns"""
    
    # Hashcat performance on M4 Pro (from benchmark)
    hashcat_speed = 6567200  # 6.567 million hashes per second
    
    print("🚀 M4 Pro GPU Hashcat Performance Analysis")
    print("=" * 50)
    print(f"Hashcat speed: {hashcat_speed:,} hashes/second")
    print()
    
    # Calculate different attack scenarios
    attacks = [
        ("Dates since 1900 (DDMMYYYY, MMDDYYYY)", calculate_date_combinations()),
        ("Numeric passwords (1-8 digits)", calculate_numeric_combinations(1, 8)),
        ("Numeric passwords (1-12 digits)", calculate_numeric_combinations(1, 12)),
        ("Alphanumeric lowercase (1-6 chars)", calculate_alphanumeric_combinations(1, 6, 36)),
        ("Alphanumeric mixed case (1-5 chars)", calculate_alphanumeric_combinations(1, 5, 62)),
        ("Alphanumeric + symbols (1-4 chars)", calculate_alphanumeric_combinations(1, 4, 95)),
    ]
    
    for attack_name, combinations in attacks:
        seconds = combinations / hashcat_speed
        print(f"📊 {attack_name}")
        print(f"   Combinations: {combinations:,}")
        print(f"   Time: {format_time(seconds)}")
        print()

def calculate_date_combinations():
    """Calculate date combinations since 1900"""
    total = 0
    
    # DDMMYYYY format (01011900 to 31122025)
    for year in range(1900, 2026):
        for month in range(1, 13):
            days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                days_in_month[1] = 29  # Leap year
            
            for day in range(1, days_in_month[month - 1] + 1):
                total += 2  # DDMMYYYY and MMDDYYYY
    
    # Also add DDMMYY and MMDDYY formats
    for year in range(1900, 2026):
        for month in range(1, 13):
            days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                days_in_month[1] = 29
            
            for day in range(1, days_in_month[month - 1] + 1):
                total += 2  # DDMMYY and MMDDYY
    
    return total

def calculate_numeric_combinations(min_length, max_length):
    """Calculate total numeric combinations"""
    total = 0
    for length in range(min_length, max_length + 1):
        total += 10 ** length
    return total

def calculate_alphanumeric_combinations(min_length, max_length, charset_size):
    """Calculate alphanumeric combinations"""
    total = 0
    for length in range(min_length, max_length + 1):
        total += charset_size ** length
    return total

def format_time(seconds):
    """Format seconds into human-readable time"""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f} hours"
    elif seconds < 2592000:  # 30 days
        days = seconds / 86400
        return f"{days:.1f} days"
    elif seconds < 31536000:  # 365 days
        months = seconds / 2592000
        return f"{months:.1f} months"
    else:
        years = seconds / 31536000
        return f"{years:.1f} years"

if __name__ == "__main__":
    calculate_crack_time()
