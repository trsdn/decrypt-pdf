#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

def try_decrypt_pdf(pdf_path, password, output_path):
    """Try to decrypt PDF with given password"""
    try:
        cmd = ['qpdf', '--password=' + password, '--decrypt', str(pdf_path), str(output_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python crack_pdf.py <pdf_file>")
        sys.exit(1)
    
    pdf_file = Path(sys.argv[1])
    if not pdf_file.exists():
        print(f"Error: {pdf_file} does not exist")
        sys.exit(1)
    
    output_file = pdf_file.with_name(f"{pdf_file.stem}_decrypted.pdf")
    
    # Common passwords to try
    passwords = [
        "",  # Empty password
        "password",
        "123456",
        "password123",
        "admin",
        "user",
        "guest",
        "police",
        "Police",
        "POLICE",
        "document",
        "pdf",
        "secret",
        "unlock",
        "open",
        "test",
        "demo",
        "sample",
        "default",
        "qwerty",
        "abc123",
        "123123",
        "111111",
        "000000",
        "root",
        "toor",
        "pass",
        "1234",
        "12345",
        "1234567890",
        pdf_file.stem,  # Try the filename as password
        pdf_file.stem.lower(),
        pdf_file.stem.upper(),
    ]
    
    print(f"Attempting to crack password for: {pdf_file}")
    print(f"Trying {len(passwords)} common passwords...")
    
    for i, password in enumerate(passwords, 1):
        print(f"[{i:2d}/{len(passwords)}] Trying password: '{password}'", end=" ... ")
        
        if try_decrypt_pdf(pdf_file, password, output_file):
            print("SUCCESS!")
            print(f"Password found: '{password}'")
            print(f"Decrypted file saved as: {output_file}")
            
            # Verify the decrypted file
            if output_file.exists() and output_file.stat().st_size > 0:
                print("Decryption verified - file created successfully.")
                # Show encryption status of decrypted file
                try:
                    result = subprocess.run(['qpdf', '--show-encryption', str(output_file)], 
                                          capture_output=True, text=True)
                    print("Decrypted file encryption status:")
                    print(result.stdout.strip())
                except:
                    pass
            return
        else:
            print("failed")
    
    print(f"\nPassword not found among {len(passwords)} common passwords.")
    print("You may need to:")
    print("1. Try a custom password list")
    print("2. Use specialized PDF password cracking tools")
    print("3. Contact the document owner for the password")

if __name__ == "__main__":
    main()
