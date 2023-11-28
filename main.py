import os
import sys
import argparse
import logging
import ebooklib
from ebooklib import epub
from collections import Counter
from nltk.tokenize import word_tokenize
from pathlib import Path
import nltk

# Setup logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

# Ensure that the required NLTK data is available
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        logging.info('Downloading NLTK punkt tokenizer data...')
        nltk.download('punkt')

def extract_words_from_epub(file_path):
    """Extracts words from an EPUB file."""
    try:
        book = epub.read_epub(file_path)
    except Exception as e:
        logging.error(f"Error reading EPUB file: {e}")
        return []

    words = []

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.get_content().decode('utf-8')
            words.extend(word_tokenize(content))

    return words

def process_words(words, min_frequency):
    """Filters and cleans words."""
    words = [word.lower() for word in words if word.isalpha()]
    word_freq = Counter(words)
    filtered_words = [word for word, freq in word_freq.items() if freq >= min_frequency]

    return filtered_words

def export_vocabulary(words, output_file):
    """Exports words to a text file."""
    with open(output_file, 'w') as f:
        for word in words:
            f.write(f"{word}\n")

def main():
    parser = argparse.ArgumentParser(description='Process an EPUB file and export its vocabulary.')
    parser.add_argument('epub_file', type=str, help='Path to the EPUB file to process')
    parser.add_argument('--min_freq', type=int, default=3, help='Minimum frequency of a word to be included')
    parser.add_argument('--output', type=str, help='Output file path (default is same as input with .txt extension)')
    
    args = parser.parse_args()

    input_file = Path(args.epub_file)
    if not input_file.exists() or input_file.suffix != '.epub':
        logging.error('Please provide a valid EPUB file.')
        sys.exit(1)

    # Set output file path
    if args.output:
        output_file = Path(args.output)
        if output_file.suffix != '.txt':
            logging.error('Output file must have a .txt extension.')
            sys.exit(1)
    else:
        output_file = input_file.with_suffix('.txt')

    # Download NLTK punkt tokenizer data if necessary
    download_nltk_data()

    # Extract words from the EPUB file
    words = extract_words_from_epub(input_file)
    if not words:
        logging.error('No words extracted from the EPUB file.')
        sys.exit(1)
    
    logging.info(f"Total words in the book: {len(words)}")

    # Process words based on frequency
    processed_words = process_words(words, args.min_freq)
    logging.info(f"Number of words with a minimum frequency of {args.min_freq}: {len(processed_words)}")

    # Export the vocabulary to a text file
    export_vocabulary(processed_words, output_file)
    logging.info(f"Vocabulary exported to {output_file}")

if __name__ == "__main__":
    main()

