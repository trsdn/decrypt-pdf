#!/bin/bash
# Install all required external tools for PDF decryption automation
# Supports macOS (Homebrew) and Ubuntu/Debian (apt)

set -e

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS. Installing with Homebrew..."
    brew install qpdf pdfcrack john hashcat
elif [[ -f "/etc/debian_version" ]]; then
    echo "Detected Ubuntu/Debian. Installing with apt..."
    sudo apt-get update
    sudo apt-get install -y qpdf pdfcrack john hashcat
else
    echo "Please install the following tools manually: qpdf, pdfcrack, john, hashcat"
    echo "Refer to the README for download links."
    exit 1
fi

echo "All required tools installed."
