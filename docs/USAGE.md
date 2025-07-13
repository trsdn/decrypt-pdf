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

## Adding New PDFs

- Add new files to `data/` or reference their location.
- Run the automation scripts as needed.
