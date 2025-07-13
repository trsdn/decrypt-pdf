#!/usr/bin/env python3

import pikepdf
import sys
import itertools
import string
from pathlib import Path

def try_password(pdf_path, password):
    """Try to open PDF with given password using pikepdf"""
    try:
        with pikepdf.open(pdf_path, password=password):
            return True
    except pikepdf.PasswordError:
        return False
    except Exception:
        return False

def generate_number_passwords(min_length=1, max_length=8):
    """Generate numeric passwords"""
    for length in range(min_length, max_length + 1):
        for combo in itertools.product('0123456789', repeat=length):
            yield ''.join(combo)

def generate_common_patterns():
    """Generate common password patterns"""
    patterns = []
    
    # Years
    for year in range(1950, 2030):
        patterns.append(str(year))
    
    # Dates (DDMM, MMDD, DDMMYY, MMDDYY)
    for day in range(1, 32):
        for month in range(1, 13):
            patterns.append(f"{day:02d}{month:02d}")
            patterns.append(f"{month:02d}{day:02d}")
            for year in [21, 22, 23, 24, 25]:
                patterns.append(f"{day:02d}{month:02d}{year}")
                patterns.append(f"{month:02d}{day:02d}{year}")
    
    return patterns

def main():
    if len(sys.argv) != 2:
        print("Usage: python advanced_crack.py <pdf_file>")
        sys.exit(1)
    
    pdf_file = Path(sys.argv[1])
    if not pdf_file.exists():
        print(f"Error: {pdf_file} does not exist")
        sys.exit(1)
    
    print(f"Advanced password cracking for: {pdf_file}")
    
    # First try common passwords
    common_passwords = [
        "", "password", "123456", "password123", "admin", "user", "guest",
        "police", "Police", "POLICE", "document", "pdf", "secret", "unlock",
        "open", "test", "demo", "sample", "default", "qwerty", "abc123",
        "123123", "111111", "000000", "root", "toor", "pass", "1234", "12345",
        "1234567890", pdf_file.stem, pdf_file.stem.lower(), pdf_file.stem.upper()
    ]
    
    print(f"Phase 1: Trying {len(common_passwords)} common passwords...")
    for i, password in enumerate(common_passwords, 1):
        print(f"[{i:2d}/{len(common_passwords)}] Trying: '{password}'", end=" ... ")
        if try_password(pdf_file, password):
            print("SUCCESS!")
            print(f"Password found: '{password}'")
            decrypt_pdf(pdf_file, password)
            return
        print("failed")
    
    print("\nPhase 2: Trying numeric passwords (1-6 digits)...")
    count = 0
    for password in generate_number_passwords(1, 6):
        count += 1
        if count % 10000 == 0:
            print(f"Tried {count} numeric passwords...")
        
        if try_password(pdf_file, password):
            print(f"SUCCESS! Password found: '{password}'")
            decrypt_pdf(pdf_file, password)
            return
    
    print(f"\nPhase 3: Trying date patterns...")
    patterns = generate_common_patterns()
    for i, password in enumerate(patterns):
        if i % 1000 == 0:
            print(f"Tried {i} date patterns...")
        
        if try_password(pdf_file, password):
            print(f"SUCCESS! Password found: '{password}'")
            decrypt_pdf(pdf_file, password)
            return
    
    print("\nPassword not found. You may need:")
    print("1. A more targeted wordlist based on context")
    print("2. Professional password recovery tools")
    print("3. The original password from the document owner")

def decrypt_pdf(pdf_file, password):
    """Decrypt the PDF and save it"""
    output_file = pdf_file.with_name(f"{pdf_file.stem}_decrypted.pdf")
    
    try:
        with pikepdf.open(pdf_file, password=password) as pdf:
            pdf.save(output_file)
        print(f"Decrypted PDF saved as: {output_file}")
        
        # Verify it's not encrypted anymore
        try:
            with pikepdf.open(output_file):
                print("Verification: Decrypted PDF opens without password")
        except:
            print("Warning: Could not verify decryption")
            
    except Exception as e:
        print(f"Error saving decrypted PDF: {e}")

if __name__ == "__main__":
    main()
