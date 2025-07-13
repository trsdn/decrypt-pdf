#!/usr/bin/env python3

import pikepdf
import sys
import itertools
import multiprocessing as mp
from pathlib import Path
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib

def try_password_batch(args):
    """Try a batch of passwords - designed for multiprocessing"""
    pdf_path, passwords, batch_id = args
    
    for i, password in enumerate(passwords):
        try:
            with pikepdf.open(pdf_path, password=password):
                return (True, password, batch_id, i)
        except (pikepdf.PasswordError, pikepdf.PdfError):
            continue
        except Exception:
            continue
    
    return (False, None, batch_id, len(passwords))

def generate_password_batches(passwords, batch_size=1000):
    """Split passwords into batches for parallel processing"""
    for i in range(0, len(passwords), batch_size):
        yield passwords[i:i + batch_size]

def generate_comprehensive_wordlist(pdf_file):
    """Generate a comprehensive password list optimized for common PDF passwords"""
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
    
    # Numeric passwords (optimized ranges)
    for length in range(1, 9):
        if length <= 4:
            # For short numbers, try all combinations
            for num in range(10**length):
                passwords.add(f"{num:0{length}d}")
        else:
            # For longer numbers, try common patterns
            patterns = ["0", "1", "2", "9"]
            for pattern in patterns:
                passwords.add(pattern * length)
    
    # Years and dates
    current_year = 2025
    for year in range(1950, current_year + 10):
        passwords.add(str(year))
        passwords.add(str(year)[-2:])  # Two-digit year
    
    # Common date patterns
    for month in range(1, 13):
        for day in range(1, 32):
            passwords.add(f"{month:02d}{day:02d}")
            passwords.add(f"{day:02d}{month:02d}")
            passwords.add(f"{month:02d}{day:02d}{current_year}")
            passwords.add(f"{day:02d}{month:02d}{current_year}")
            passwords.add(f"{month:02d}{day:02d}{str(current_year)[-2:]}")
            passwords.add(f"{day:02d}{month:02d}{str(current_year)[-2:]}")
    
    # Common keyboard patterns
    keyboard_patterns = [
        "qwerty", "asdf", "zxcv", "123qwe", "qwe123", "asd123",
        "qwerty123", "123456789", "987654321", "abcdef", "fedcba"
    ]
    passwords.update(keyboard_patterns)
    
    # Simple variations with common suffixes/prefixes
    base_words = ["password", "admin", "user", "test", "demo", "police"]
    variations = ["123", "1", "!", "@", "#", "2024", "2025"]
    
    for word in base_words:
        for var in variations:
            passwords.add(word + var)
            passwords.add(var + word)
            passwords.add(word.capitalize() + var)
    
    return list(passwords)

def main():
    if len(sys.argv) != 2:
        print("Usage: python m4_optimized_crack.py <pdf_file>")
        sys.exit(1)
    
    pdf_file = Path(sys.argv[1])
    if not pdf_file.exists():
        print(f"Error: {pdf_file} does not exist")
        sys.exit(1)
    
    # Use all available CPU cores (M4 Pro has 10-12 cores)
    num_processes = mp.cpu_count()
    print(f"🚀 M4 Pro Optimized PDF Password Cracker")
    print(f"📁 Target: {pdf_file}")
    print(f"⚡ Using {num_processes} CPU cores for parallel processing")
    
    # Generate comprehensive password list
    print("📝 Generating password wordlist...")
    passwords = generate_comprehensive_wordlist(pdf_file)
    print(f"📊 Generated {len(passwords):,} passwords to test")
    
    # Split into batches for parallel processing
    batch_size = max(100, len(passwords) // (num_processes * 4))
    batches = list(generate_password_batches(passwords, batch_size))
    print(f"🔄 Split into {len(batches)} batches of ~{batch_size} passwords each")
    
    start_time = time.time()
    passwords_tested = 0
    
    # Process batches in parallel
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Submit all batches
        future_to_batch = {
            executor.submit(try_password_batch, (pdf_file, batch, i)): i 
            for i, batch in enumerate(batches)
        }
        
        try:
            for future in as_completed(future_to_batch):
                success, password, batch_id, tested_count = future.result()
                passwords_tested += tested_count
                
                # Show progress
                progress = (passwords_tested / len(passwords)) * 100
                elapsed = time.time() - start_time
                rate = passwords_tested / elapsed if elapsed > 0 else 0
                
                print(f"🔍 Progress: {progress:5.1f}% | "
                      f"Tested: {passwords_tested:,}/{len(passwords):,} | "
                      f"Rate: {rate:,.0f} pwd/sec", end="\r")
                
                if success:
                    elapsed = time.time() - start_time
                    print(f"\n🎉 SUCCESS! Password found: '{password}'")
                    print(f"⏱️  Time taken: {elapsed:.2f} seconds")
                    print(f"📈 Tested {passwords_tested:,} passwords at {rate:,.0f} pwd/sec")
                    
                    # Decrypt and save
                    decrypt_pdf(pdf_file, password)
                    return
                    
        except KeyboardInterrupt:
            print(f"\n⏹️  Interrupted by user")
            print(f"📊 Tested {passwords_tested:,} passwords in {time.time() - start_time:.2f} seconds")
            return
    
    elapsed = time.time() - start_time
    print(f"\n❌ Password not found after testing {len(passwords):,} passwords")
    print(f"⏱️  Total time: {elapsed:.2f} seconds")
    print(f"📈 Average rate: {len(passwords)/elapsed:,.0f} passwords/second")
    print("\n💡 Next steps:")
    print("1. Try a larger custom wordlist")
    print("2. Use specialized tools like Hashcat or John the Ripper")
    print("3. Consider the document's context for password hints")

def decrypt_pdf(pdf_file, password):
    """Decrypt the PDF and save it"""
    output_file = pdf_file.with_name(f"{pdf_file.stem}_decrypted.pdf")
    
    try:
        print(f"\n💾 Decrypting and saving...")
        with pikepdf.open(pdf_file, password=password) as pdf:
            # Remove all encryption
            pdf.save(output_file)
        
        print(f"✅ Decrypted PDF saved as: {output_file}")
        
        # Verify decryption
        try:
            with pikepdf.open(output_file) as verify_pdf:
                pages = len(verify_pdf.pages)
                print(f"✅ Verification successful: {pages} pages, no password required")
        except Exception as e:
            print(f"⚠️  Verification warning: {e}")
            
    except Exception as e:
        print(f"❌ Error saving decrypted PDF: {e}")

if __name__ == "__main__":
    main()
