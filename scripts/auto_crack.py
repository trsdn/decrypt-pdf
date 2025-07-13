#!/usr/bin/env python3
"""Unified PDF password cracking helper.

This script chooses the best cracking approach based on available
GPU support and exposes different cracking modes.

Usage:
    python auto_crack.py <pdf_file> [--mode MODE]

Modes:
    auto      Detect best method (default)
    quick     Use simple common/password patterns
    optimized Use CPU optimized wordlist attack
    brute     Full brute-force with CPU
"""

import argparse
import subprocess
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent

def gpu_available() -> bool:
    """Return True if hashcat with a GPU backend is available."""
    try:
        result = subprocess.run(['hashcat', '-I'], capture_output=True, text=True)
        return result.returncode == 0 and 'OpenCL' in result.stdout
    except FileNotFoundError:
        return False


def run_script(script_name: str, pdf: Path):
    """Run another cracking script located in the same directory."""
    script_path = SCRIPT_DIR / script_name
    subprocess.run(['python3', str(script_path), str(pdf)])


def auto_mode(pdf: Path):
    if gpu_available():
        print('GPU detected, using hashcat based cracking...')
        run_script('gpu_crack.py', pdf)
    else:
        print('GPU not available, using optimized CPU cracking...')
        run_script('m4_optimized_crack.py', pdf)


def main():
    parser = argparse.ArgumentParser(description='Auto-select PDF password cracking approach')
    parser.add_argument('pdf_file', help='Target PDF file')
    parser.add_argument('--mode', choices=['auto', 'quick', 'optimized', 'brute'], default='auto',
                        help='Cracking mode to use')
    args = parser.parse_args()

    pdf = Path(args.pdf_file)
    if not pdf.exists():
        parser.error(f"File not found: {pdf}")

    if args.mode == 'auto':
        auto_mode(pdf)
    elif args.mode == 'quick':
        run_script('advanced_crack.py', pdf)
    elif args.mode == 'optimized':
        run_script('m4_optimized_crack.py', pdf)
    elif args.mode == 'brute':
        run_script('brute_force_crack.py', pdf)


if __name__ == '__main__':
    main()
