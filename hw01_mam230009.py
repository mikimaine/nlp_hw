#!/usr/bin/env python3

################################################################################
#
# FILE:
#   hw01_mam230009.py
# AUTHOR:
#   Mikiyas Amdu Midru
#   MAM230009
# DESCRIPTION:
#   Homework 1
#   This script processes the edited Treasure Island text file (ti.txt) as follows:
#       1. Reads the file edited file.
#       2. Inserts spaces around punctuation so that every token is atomic.
#       3. Splits the text into a list of word tokens.
#       4. Counts word frequencies ignoring case.
#       5. Sorts the words by descending frequency.
#       6. Displays the top 10 most frequent words (ignoring punctuation),
#          along with the count and the relative frequency.
# DEPENDENCIES:
#       Created with Python env 3.12.2 (Python version)
#       Dependencies, re, string
#
################################################################################

import re
import string

def tokenize_text(text):
    """
    Tokenizes the input text into a list of word tokens.

    The function first inserts spaces around punctuation characters
    so that punctuation become separate tokens. Then it splits the text on whitespace.
    """
    punctuation_to_separate = string.punctuation.replace("'", "")
    pattern = r"([" + re.escape(punctuation_to_separate) + "])"

    # Insert spaces around each punctuation mark matched.
    # This will separate punctuation that is adjacent to letters.
    text_with_spaces = re.sub(pattern, r" \1 ", text)

    tokens = text_with_spaces.split()
    return tokens

def count_words(tokens):
    """
    Counts occurrences of each token in the tokens list, ignoring case.
    Returns a dictionary mapping lowercase token -> count.
    """
    counts = {}
    for token in tokens:
        token_lower = token.lower()
        counts[token_lower] = counts.get(token_lower, 0) + 1
    return counts

def main():
    try:
        with open("ti.txt", "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print("Error: The file 'ti.txt' was not found. Please ensure it exists in the current directory.")
        return

    tokens = tokenize_text(text)

    # print(tokens)
    # print(type(tokens))

    word_counts = count_words(tokens)

    # A set of punctuation tokens (we use string.punctuation).
    extra_punctuation = {"“", "”", "‘", "’", "”"}
    punctuation_set = set(string.punctuation) | extra_punctuation

    total_word_count = sum(count for token, count in word_counts.items() if token not in punctuation_set)

    print("Total words: {}".format(total_word_count))
    # sorted_words is a list of (token, count) tuples sorted descending by count.
    sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)

    print("Top 10 most frequent words (excluding punctuation):")
    print(f"{'Word':15} {'Count':5} {'Frequency':>10}")
    print("-" * 33)

    printed_entries = 0
    for token, count in sorted_words:
        if token in punctuation_set:
            continue

        frequency = count / total_word_count if total_word_count else 0

        print(f"{token:15} {count:5} {frequency:10.4f}")

        printed_entries += 1
        if printed_entries >= 10:
            break

if __name__ == "__main__":
    main()