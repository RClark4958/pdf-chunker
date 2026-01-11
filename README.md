# PDF Chunker

CLI tool to split large PDFs into smaller files based on size threshold.

## Stack

- **Language**: Python 3.8+
- **Library**: PyPDF2

## Usage

```bash
# Single file
python pdf_splitter.py document.pdf

# Custom max size (MB)
python pdf_splitter.py document.pdf --max-size 2

# Directory
python pdf_splitter.py ./documents/

# Glob pattern
python pdf_splitter.py "*.pdf"
```

## How It Works

1. Check if file exceeds max size (default 4MB)
2. Calculate pages per chunk based on average page size
3. Create chunks, retry with fewer pages if chunk exceeds limit
4. Output: `document_part1.pdf`, `document_part2.pdf`, etc.

## Setup

```bash
pip install -r requirements.txt
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--max-size` | 4 | Max chunk size in MB |

## Project Structure

```
pdf-chunker/
├── pdf_splitter.py   # Main script
└── requirements.txt  # PyPDF2==3.0.1
```

## License

MIT
