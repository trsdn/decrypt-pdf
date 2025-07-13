#!/usr/bin/env python3

import os
import subprocess
import argparse
from pathlib import Path

def show_encryption_status(pdf_path: Path, label: str):
    """
    Print the encryption status of a PDF file using qpdf.
    """
    try:
        result = subprocess.run(
            ['qpdf', '--show-encryption', str(pdf_path)],
            capture_output=True,
            text=True
        )
        print(f"[{label}] {pdf_path.name} encryption status:")
        print(result.stdout.strip())
    except Exception as e:
        print(f"Error checking encryption status for {pdf_path.name}: {str(e)}")

def decrypt_pdf(input_path: Path, output_path: Path) -> bool:
    """
    Decrypt or unrestrict a PDF file using qpdf.
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path where the decrypted PDF will be saved
    
    Returns:
        bool: True if decryption was successful, False otherwise
    """
    try:
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Print encryption status before decryption
        show_encryption_status(input_path, "BEFORE")
        
        # Run qpdf command to decrypt the PDF
        result = subprocess.run(
            ['qpdf', '--decrypt', str(input_path), str(output_path)],
            capture_output=True,
            text=True
        )
        
        # Check if the output file was created and has content
        if output_path.exists() and output_path.stat().st_size > 0:
            if result.stderr and "WARNING" in result.stderr:
                print(f"Successfully decrypted/unrestricted with warnings: {input_path.name}")
            else:
                print(f"Successfully decrypted/unrestricted: {input_path.name}")
            show_encryption_status(output_path, "AFTER")
            return True
        else:
            print(f"Error decrypting/unrestricting {input_path.name}: Failed to create output file")
            return False
            
    except Exception as e:
        print(f"Error processing {input_path.name}: {str(e)}")
        return False

def process_directory(input_dir: Path, output_dir: Path):
    """
    Process all PDF files in the input directory.
    
    Args:
        input_dir: Directory containing encrypted PDFs
        output_dir: Directory where decrypted PDFs will be saved
    """
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all PDF files in the input directory
    pdf_files = list(input_dir.glob('*.pdf'))
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    # Process each PDF file
    successful = 0
    for pdf_file in pdf_files:
        output_path = output_dir / pdf_file.name
        if decrypt_pdf(pdf_file, output_path):
            successful += 1
    
    print(f"\nProcessing complete:")
    print(f"Successfully decrypted: {successful}/{len(pdf_files)} files")

def main():
    parser = argparse.ArgumentParser(description='Decrypt PDF files using qpdf')
    parser.add_argument('input_dir', type=str, help='Input directory containing encrypted PDFs')
    parser.add_argument('output_dir', type=str, help='Output directory for decrypted PDFs')
    
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist")
        return
    
    process_directory(input_dir, output_dir)

if __name__ == '__main__':
    main() 