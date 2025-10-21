# Explicit Content Wordlist

This repository contains known explicit bypasses for explicit text on the Roblox platform.

## Project Structure

```
data/
  all.txt              # General explicit content words
  specific/
    fetish.txt         # Fetish-related terms
    racist.txt         # Racist terms
    sexist.txt         # Sexist terms
    sexual.txt         # Sexual terms
```

## Contributing

Before contributing, run the duplicate checker:

```bash
python scripts/check_duplicates.py
```

The script automatically:
- Detects duplicates within and across files (case-insensitive)
- Removes duplicate entries
- Creates backup files (.bak) before making changes

GitHub Actions will run this automatically on all pushes and pull requests.

## Troubleshooting

**"python: command not found"**
- Install Python 3 or try `python3` instead of `python`

**GitHub Actions not running**
- Enable Actions in repository settings
- Verify `.github/workflows/` is at repository root

**Script not removing duplicates**
- Check write permissions on files
- Look for .bak backup files to see changes

## Support

[Join our Discord server](https://discord.blox.wtf) or open an issue if you need help.