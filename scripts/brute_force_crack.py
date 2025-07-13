#!/usr/bin/env python3

import pikepdf
import sys
import itertools
import multiprocessing as mp
import string
from pathlib import Path
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

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

def generate_brute_force_passwords(charset, min_length=1, max_length=6):
    """Generate all possible passwords for given charset and length range"""
    for length in range(min_length, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            yield ''.join(combo)

def generate_smart_patterns():
    """Generate smart password patterns based on common conventions"""
    patterns = []
    
    # Common number patterns
    patterns.extend([f"{i:02d}" for i in range(100)])  # 00-99
    patterns.extend([f"{i:03d}" for i in range(1000)])  # 000-999
    patterns.extend([f"{i:04d}" for i in range(10000)])  # 0000-9999
    
    # Birth years and recent years
    for year in range(1940, 2030):
        patterns.append(str(year))
        patterns.append(str(year)[-2:])
    
    # Phone number patterns (US format variations)
    for area in ['123', '555', '000', '911']:
        for exchange in ['123', '555', '000']:
            for number in ['0000', '1234', '5678']:
                patterns.append(f"{area}{exchange}{number}")
                patterns.append(f"{area}-{exchange}-{number}")
    
    # Social Security Number patterns (XXX-XX-XXXX)
    common_ssn_prefixes = ['123', '555', '000', '111', '222']
    for prefix in common_ssn_prefixes:
        for middle in ['12', '34', '56', '00', '11']:
            for last in ['1234', '5678', '0000', '1111']:
                patterns.append(f"{prefix}{middle}{last}")
                patterns.append(f"{prefix}-{middle}-{last}")
    
    return patterns

def main():
    if len(sys.argv) not in [2, 3]:
        print("Usage: python brute_force_crack.py <pdf_file> [max_length]")
        print("Default max_length is 4 (increase carefully - exponential growth!)")
        sys.exit(1)
    
    pdf_file = Path(sys.argv[1])
    if not pdf_file.exists():
        print(f"Error: {pdf_file} does not exist")
        sys.exit(1)
    
    max_length = int(sys.argv[2]) if len(sys.argv) == 3 else 4
    
    num_processes = mp.cpu_count()
    print(f"🔥 Brute Force PDF Password Cracker (M4 Pro Optimized)")
    print(f"📁 Target: {pdf_file}")
    print(f"⚡ Using {num_processes} CPU cores")
    print(f"🔢 Max password length: {max_length}")
    print()
    
    strategies = [
        ("🔢 Numeric brute force", string.digits, 1, min(6, max_length)),
        ("🔤 Lowercase letters", string.ascii_lowercase, 1, min(4, max_length)),
        ("🔠 Mixed case letters", string.ascii_letters, 1, min(3, max_length)),
        ("🎯 Smart patterns", None, 0, 0),  # Special case
    ]
    
    if max_length >= 5:
        print("⚠️  Warning: Brute forcing passwords longer than 4 characters may take a very long time!")
        print("💡 Consider using targeted wordlists or known password patterns instead.")
        print()
    
    total_start_time = time.time()
    
    for strategy_name, charset, min_len, max_len in strategies:
        print(f"\n{strategy_name}")
        print("=" * 50)
        
        if charset is None:  # Smart patterns
            passwords = generate_smart_patterns()
            passwords = list(passwords)  # Convert to list for batching
        else:
            # Estimate total passwords for this strategy
            total_passwords = sum(len(charset)**i for i in range(min_len, max_len + 1))
            print(f"📊 Estimated passwords to test: {total_passwords:,}")
            
            if total_passwords > 10000000:  # 10 million
                response = input("⚠️  This will test over 10 million passwords. Continue? (y/N): ")
                if response.lower() != 'y':
                    print("Skipping this strategy...")
                    continue
            
            passwords = generate_brute_force_passwords(charset, min_len, max_len)
        
        # Convert generator to list in chunks to avoid memory issues
        batch_size = 1000
        strategy_start_time = time.time()
        passwords_tested = 0
        found = False
        
        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            batch = []
            batch_id = 0
            
            for password in passwords:
                batch.append(password)
                
                if len(batch) >= batch_size:
                    # Submit batch
                    future = executor.submit(try_password_batch, (pdf_file, batch, batch_id))
                    
                    # Check result
                    success, found_password, bid, tested_count = future.result()
                    passwords_tested += tested_count
                    
                    elapsed = time.time() - strategy_start_time
                    rate = passwords_tested / elapsed if elapsed > 0 else 0
                    
                    print(f"🔍 Tested: {passwords_tested:,} | Rate: {rate:,.0f} pwd/sec", end="\r")
                    
                    if success:
                        elapsed_total = time.time() - total_start_time
                        print(f"\n🎉 SUCCESS! Password found: '{found_password}'")
                        print(f"⏱️  Total time: {elapsed_total:.2f} seconds")
                        print(f"📈 Total tested: {passwords_tested:,} passwords")
                        
                        # Decrypt and save
                        decrypt_pdf(pdf_file, found_password)
                        return
                    
                    batch = []
                    batch_id += 1
            
            # Process remaining passwords in final batch
            if batch:
                future = executor.submit(try_password_batch, (pdf_file, batch, batch_id))
                success, found_password, bid, tested_count = future.result()
                passwords_tested += tested_count
                
                if success:
                    elapsed_total = time.time() - total_start_time
                    print(f"\n🎉 SUCCESS! Password found: '{found_password}'")
                    print(f"⏱️  Total time: {elapsed_total:.2f} seconds")
                    print(f"📈 Total tested: {passwords_tested:,} passwords")
                    
                    decrypt_pdf(pdf_file, found_password)
                    return
        
        strategy_elapsed = time.time() - strategy_start_time
        print(f"\n❌ Strategy completed: {passwords_tested:,} passwords in {strategy_elapsed:.2f}s")
    
    total_elapsed = time.time() - total_start_time
    print(f"\n❌ All strategies exhausted in {total_elapsed:.2f} seconds")
    print("\n💡 Recommendations:")
    print("1. Try a targeted dictionary attack with domain-specific words")
    print("2. Use professional tools like Hashcat with GPU acceleration")
    print("3. Check if there are any hints in the document metadata")
    print("4. Contact the document owner for the password")

def decrypt_pdf(pdf_file, password):
    """Decrypt the PDF and save it"""
    output_file = pdf_file.with_name(f"{pdf_file.stem}_decrypted.pdf")
    
    try:
        print(f"\n💾 Decrypting and saving...")
        with pikepdf.open(pdf_file, password=password) as pdf:
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
