# PDF Decryption Automation

This repository provides tools and scripts to automate the decryption of password-protected PDF files using GPU-accelerated and CPU-based methods. It is designed for batch processing and supports both modern and legacy PDF encryption.

## Directory Structure

- `scripts/` — Python and shell scripts for automation (hash extraction, batch processing, etc.)
- `data/` — Place to store input PDF files (not included in repo)
- `results/` — Output directory for decrypted PDFs (gitignored)
- `docs/` — Documentation and usage notes

## Usage

1. **Install requirements:**

   ```bash
   pip install -r requirements.txt
   brew install pdfcrack qpdf
   ```

2. **Prepare your wordlist:**
   - Place your `date_wordlist.txt` (or other wordlists) in the repo root or reference its path in your scripts.
   - **Do not commit wordlists to the repository.**
3. **Run scripts:**
   - Use scripts in `scripts/` to automate hash extraction, password cracking, and decryption.

## Security Notice

- **Never commit password lists or sensitive data to the repository.**
- The `.gitignore` is configured to prevent accidental inclusion of wordlists and results.

## Requirements

## Wordlists Used

This project uses custom and public wordlists for password cracking, including:

- `wordlists/date_wordlist.txt` — A custom list of date-based passwords in various formats (not included in the repository).
- [rockyou.txt](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt) — The classic password list from the RockYou leak.
- [SecLists](https://github.com/danielmiessler/SecLists) — A comprehensive collection of multiple wordlists for security testing.
- [CrackStation](https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm) — A large human-readable password list.

To use these, download them from their official sources and place them in the `wordlists/` directory.

**Note:** Wordlists are not included in the repository. Place your wordlists in the `wordlists/` directory as described in the documentation. Only `README.md` in that folder is tracked by git.

## Example Workflow

1. Extract hash from PDF (if needed)
2. Crack password using your wordlist
3. Decrypt PDF in place or to `results/`
4. Or simply run `auto_crack.py` to let the tool choose the best method

## License

MIT License

## Custom Scripts

The `scripts/` directory contains several tools for password analysis and PDF password cracking:

- `pdf_decrypt.py`: Batch decrypts PDF files in a directory using a provided password (uses qpdf).
- `time_calculator.py`: Estimates time required to brute-force various password patterns on an M4 Pro GPU.
- `m4_optimized_crack.py`: Multi-core CPU brute-force and smart wordlist attack, optimized for Apple M4 Pro.
- `gpu_crack.py`: Automates hash extraction and runs hashcat (GPU) with a generated wordlist for PDF cracking.
- `brute_force_crack.py`: Multi-core brute-force attack with numeric, alphabetic, and smart pattern strategies.
- `advanced_crack.py`: Tries common, numeric, and date-based passwords for a given PDF.
- `auto_crack.py`: Automatically selects the best cracking method (GPU or CPU) and exposes
  different cracking modes.

See each script's help or comments for usage details.

## Prerequisites

You will need the following tools installed on your system:

1. **Python 3.6 or higher**
2. **qpdf** — PDF decryption and manipulation
3. **pdfcrack** — For legacy PDF password recovery
4. **john** (John the Ripper, jumbo version recommended) — For hash extraction and password cracking
5. **hashcat** — GPU-accelerated password cracking

### Quick Install (macOS & Ubuntu/Debian)

You can install all required external tools with the provided script:

```bash
./install_tools.sh
```

### Manual Installation

- On macOS (Homebrew):

  ```bash
  brew install qpdf pdfcrack john hashcat
  ```

- On Ubuntu/Debian:

  ```bash
  sudo apt-get install qpdf pdfcrack john hashcat
  ```

- On Windows:
  - Download and install [qpdf](https://qpdf.sourceforge.io/), [John the Ripper](https://www.openwall.com/john/), and [hashcat](https://hashcat.net/hashcat/) from their official sites.
  - For `pdfcrack`, see [https://pdfcrack.sourceforge.net/](https://pdfcrack.sourceforge.net/)

## Installation

1. Clone this repository
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Script Usage

Run the script from the command line:

```bash
python pdf_decrypt.py /path/to/input/directory /path/to/output/directory
```

The script will:

1. Find all PDF files in the input directory
2. Attempt to decrypt each PDF file
3. Save the decrypted versions to the output directory
4. Print progress and results

## Example

```bash
python pdf_decrypt.py ./encrypted_pdfs ./decrypted_pdfs
```

You can also let the toolkit decide between GPU or CPU modes:

```bash
python scripts/auto_crack.py Police_.pdf
```

## Notes

- The script will create the output directory if it doesn't exist
- Original files are not modified
- The script will maintain the original filenames in the output directory
- Progress and any errors will be displayed in the console
