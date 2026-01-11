#!/usr/bin/env python3
"""
PDF Splitter - Splits PDF files larger than 4MB into smaller chunks
"""

import os
import sys
import argparse
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter


def get_file_size_mb(file_path):
    """Get file size in MB"""
    return os.path.getsize(file_path) / (1024 * 1024)


def split_pdf(input_path, max_size_mb=4):
    """Split a PDF file if it exceeds the maximum size"""
    file_size_mb = get_file_size_mb(input_path)
    
    if file_size_mb <= max_size_mb:
        print(f"✓ {input_path.name} is already under {max_size_mb}MB ({file_size_mb:.2f}MB)")
        return []
    
    print(f"⚡ Splitting {input_path.name} ({file_size_mb:.2f}MB)...")
    
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    
    # Estimate pages per chunk based on file size
    pages_per_chunk = max(1, int(total_pages * max_size_mb / file_size_mb))
    
    output_files = []
    chunk_num = 1
    current_page = 0
    
    while current_page < total_pages:
        writer = PdfWriter()
        chunk_start = current_page
        
        # Add pages to current chunk
        for _ in range(pages_per_chunk):
            if current_page >= total_pages:
                break
            writer.add_page(reader.pages[current_page])
            current_page += 1
        
        # Create output filename
        output_path = input_path.parent / f"{input_path.stem}_part{chunk_num}.pdf"
        
        # Write the chunk
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        # Check if we need to split this chunk further
        chunk_size_mb = get_file_size_mb(output_path)
        
        if chunk_size_mb > max_size_mb and (current_page - chunk_start) > 1:
            # Remove the oversized chunk and reduce pages per chunk
            os.remove(output_path)
            current_page = chunk_start
            pages_per_chunk = max(1, pages_per_chunk // 2)
            continue
        
        output_files.append(output_path)
        print(f"  → Created {output_path.name} ({chunk_size_mb:.2f}MB)")
        chunk_num += 1
    
    return output_files


def process_pdfs(input_pattern, max_size_mb=4):
    """Process all PDF files matching the pattern"""
    input_path = Path(input_pattern)
    
    if input_path.is_file():
        pdf_files = [input_path] if input_path.suffix.lower() == '.pdf' else []
    elif input_path.is_dir():
        pdf_files = [f for f in input_path.glob('*.pdf') if not f.name.endswith('.Identifier')]
    else:
        # Treat as glob pattern
        pdf_files = [f for f in Path('.').glob(input_pattern) if f.suffix.lower() == '.pdf' and not f.name.endswith('.Identifier')]
    
    if not pdf_files:
        print("No PDF files found!")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to process\n")
    
    total_split = 0
    for pdf_file in pdf_files:
        try:
            split_files = split_pdf(pdf_file, max_size_mb)
            if split_files:
                total_split += 1
        except Exception as e:
            print(f"✗ Error processing {pdf_file.name}: {e}")
    
    print(f"\nProcessing complete! Split {total_split} file(s).")


def main():
    parser = argparse.ArgumentParser(
        description='Split PDF files larger than a specified size',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s *.pdf                    # Process all PDFs in current directory
  %(prog)s document.pdf             # Process a single PDF
  %(prog)s /path/to/pdfs/          # Process all PDFs in directory
  %(prog)s "*.pdf" --max-size 2    # Split PDFs larger than 2MB
        '''
    )
    
    parser.add_argument('input', help='PDF file(s) to process (file, directory, or glob pattern)')
    parser.add_argument('--max-size', type=float, default=4.0,
                      help='Maximum file size in MB (default: 4.0)')
    
    args = parser.parse_args()
    
    if args.max_size <= 0:
        print("Error: Maximum size must be greater than 0")
        sys.exit(1)
    
    process_pdfs(args.input, args.max_size)


if __name__ == '__main__':
    main()