# Usage Guide

## Batch Decryption

- Place PDFs in `data/` or reference their absolute paths.
- Use scripts in `scripts/` to automate hash extraction and decryption.
- Store decrypted files in `results/` (gitignored).

## Wordlists

- Place your wordlists (e.g., `date_wordlist.txt`) in a dedicated `wordlists/` directory at the project root for better organization.
- The `wordlists/` directory should be listed in `.gitignore` to prevent accidental commits.
- Reference your wordlist in scripts or via command line as `wordlists/date_wordlist.txt`.
- **Never commit wordlists to the repository.**

## Example Commands

```bash
pdfcrack -w date_wordlist.txt /path/to/file.pdf
qpdf --password=PASSWORD --replace-input --decrypt /path/to/file.pdf
```

## Automatic Cracking Helper

Use `auto_crack.py` to automatically choose between GPU and CPU modes. The script also exposes different cracking strategies via the `--mode` option:

```bash
python scripts/auto_crack.py secure.pdf
# or specify a mode
python scripts/auto_crack.py secure.pdf --mode optimized
```

Available modes are:

- `auto` *(default)* – Detect GPU support and dispatch accordingly
- `quick` – Run `advanced_crack.py` for common password patterns
- `optimized` – Use the CPU-optimized wordlist attack
- `brute` – Perform a full brute-force attack

## Adding New PDFs

- Add new files to `data/` or reference their location.
- Run the automation scripts as needed.
