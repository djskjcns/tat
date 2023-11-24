import os
import re
import nltk
import ebooklib
from ebooklib import epub
from collections import Counter
from nltk.tokenize import word_tokenize

def extract_words_from_epub(file_path):
    book = epub.read_epub(file_path)
    words = []

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.get_content().decode('utf-8')
            words.extend(word_tokenize(content))

    return words

def process_words(words, min_frequency=3):
    words = [word.lower() for word in words if word.isalpha()]
    word_freq = Counter(words)
    filtered_words = [word for word, freq in word_freq.items() if freq >= min_frequency]

    return filtered_words

def export_vocabulary(words, output_file):
    with open(output_file, 'w') as f:
        for word in words:
            f.write(f"{word}\n")

def main():
    input_file = 'tmora.epub'
    output_file = 'vocabulary.txt'

    words = extract_words_from_epub(input_file)
    print("书籍总单词数：", len(words))
    processed_words = process_words(words)
    print("导出单词数：", len(processed_words))
    export_vocabulary(processed_words, output_file)

if __name__ == "__main__":
    main()
