#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path
import tempfile
import os

def check_hashcat():
    """Check if hashcat is installed"""
    try:
        result = subprocess.run(['hashcat', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def extract_pdf_hash(pdf_file):
    """Extract PDF hash for hashcat using pdf2john.py"""
    try:
        # Try to find pdf2john.py (part of John the Ripper)
        possible_paths = [
            '/usr/share/john/pdf2john.py',
            '/opt/homebrew/share/john/pdf2john.py',
            'pdf2john.py'
        ]
        
        pdf2john_path = None
        for path in possible_paths:
            if Path(path).exists():
                pdf2john_path = path
                break
        
        if not pdf2john_path:
            # Try to find it in PATH
            try:
                result = subprocess.run(['which', 'pdf2john.py'], capture_output=True, text=True)
                if result.returncode == 0:
                    pdf2john_path = result.stdout.strip()
            except:
                pass
        
        if pdf2john_path:
            result = subprocess.run(['python3', pdf2john_path, str(pdf_file)], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        
        return None
    except Exception as e:
        print(f"Error extracting PDF hash: {e}")
        return None

def create_wordlist(pdf_file):
    """Create a comprehensive wordlist file"""
    wordlist_file = pdf_file.parent / "wordlist.txt"
    
    passwords = set()
    
    # Common passwords
    common = [
        "", "password", "123456", "password123", "admin", "user", "guest",
        "police", "Police", "POLICE", "document", "pdf", "secret", "unlock",
        "open", "test", "demo", "sample", "default", "qwerty", "abc123",
        "123123", "111111", "000000", "root", "toor", "pass", "1234", "12345",
        "1234567890", "letmein", "welcome", "monkey", "dragon", "master"
    ]
    
    # File-based passwords
    filename_base = pdf_file.stem.replace("_", "").replace("-", "")
    filename_variants = [
        pdf_file.stem, filename_base, filename_base.lower(), filename_base.upper(),
        filename_base.title(), pdf_file.name, pdf_file.name.lower()
    ]
    
    passwords.update(common + filename_variants)
    
    # Numeric passwords
    for length in range(1, 9):
        if length <= 6:
            for num in range(10**length):
                passwords.add(f"{num:0{length}d}")
    
    # Years
    for year in range(1950, 2030):
        passwords.add(str(year))
        passwords.add(str(year)[-2:])
    
    # Date patterns
    for month in range(1, 13):
        for day in range(1, 32):
            passwords.add(f"{month:02d}{day:02d}")
            passwords.add(f"{day:02d}{month:02d}")
            for year in [24, 25]:
                passwords.add(f"{month:02d}{day:02d}{year}")
                passwords.add(f"{day:02d}{month:02d}{year}")
    
    # Write wordlist
    with open(wordlist_file, 'w') as f:
        for pwd in sorted(passwords):
            f.write(pwd + '\n')
    
    return wordlist_file

def crack_with_hashcat(pdf_file):
    """Try to crack PDF using hashcat (GPU-accelerated)"""
    print("🔥 Attempting GPU-accelerated cracking with hashcat...")
    
    # Extract hash
    pdf_hash = extract_pdf_hash(pdf_file)
    if not pdf_hash:
        print("❌ Could not extract PDF hash for hashcat")
        return False
    
    # Create hash file
    hash_file = pdf_file.parent / "pdf.hash"
    with open(hash_file, 'w') as f:
        f.write(pdf_hash)
    
    # Create wordlist
    wordlist_file = create_wordlist(pdf_file)
    print(f"📝 Created wordlist with {sum(1 for _ in open(wordlist_file))} passwords")
    
    # Run hashcat
    try:
        print("⚡ Running hashcat (this may take a while)...")
        result = subprocess.run([
            'hashcat', 
            '-m', '10500',  # PDF 1.4-1.6 (Acrobat 5-8) mode
            str(hash_file),
            str(wordlist_file),
            '--force'
        ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
        
        if "Cracked" in result.stdout or result.returncode == 0:
            # Extract the password from hashcat output
            lines = result.stdout.split('\n')
            for line in lines:
                if pdf_hash in line and ':' in line:
                    password = line.split(':')[-1].strip()
                    print(f"🎉 Hashcat found password: '{password}'")
                    
                    # Clean up
                    hash_file.unlink(missing_ok=True)
                    wordlist_file.unlink(missing_ok=True)
                    
                    return password
        
        print("❌ Hashcat didn't find the password")
        
    except subprocess.TimeoutExpired:
        print("⏰ Hashcat timed out after 5 minutes")
    except Exception as e:
        print(f"❌ Hashcat error: {e}")
    finally:
        # Clean up
        hash_file.unlink(missing_ok=True)
        wordlist_file.unlink(missing_ok=True)
    
    return False

def install_tools():
    """Provide instructions for installing tools"""
    print("🛠️  To maximize performance on your M4 Pro, consider installing:")
    print()
    print("1. Hashcat (GPU-accelerated):")
    print("   brew install hashcat")
    print()
    print("2. John the Ripper (includes pdf2john.py):")
    print("   brew install john")
    print()
    print("3. Hydra (network service cracker):")
    print("   brew install hydra")
    print()
    print("These tools can leverage your M4 Pro's GPU and multiple CPU cores more efficiently.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python gpu_crack.py <pdf_file>")
        sys.exit(1)
    
    pdf_file = Path(sys.argv[1])
    if not pdf_file.exists():
        print(f"Error: {pdf_file} does not exist")
        sys.exit(1)
    
    print(f"🚀 GPU-Optimized PDF Password Cracker for M4 Pro")
    print(f"📁 Target: {pdf_file}")
    print()
    
    # Check for hashcat
    if check_hashcat():
        password = crack_with_hashcat(pdf_file)
        if password:
            # Decrypt the PDF
            try:
                import pikepdf
                output_file = pdf_file.with_name(f"{pdf_file.stem}_decrypted.pdf")
                with pikepdf.open(pdf_file, password=password) as pdf:
                    pdf.save(output_file)
                print(f"✅ Decrypted PDF saved as: {output_file}")
                return
            except Exception as e:
                print(f"❌ Error decrypting PDF: {e}")
                return
    else:
        print("❌ Hashcat not found")
        install_tools()
        print()
        print("💡 Falling back to the optimized Python cracker...")
        print("Run: python m4_optimized_crack.py Police_.pdf")

if __name__ == "__main__":
    main()
