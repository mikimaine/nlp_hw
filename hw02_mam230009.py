#!/usr/bin/env python3

################################################################################
#
# FILE:
#   hw02_mam230009.py
# AUTHOR:
#   Mikiyas Amdu Midru
#   MAM230009
# DESCRIPTION:
#   Homework 2
#   Processes a text file ("text_news.txt") to extract and normalize dates from sentences.
#   It uses a custom NLTK tokenizer with additional abbreviations to improve sentence tokenizer.
#   The script performs the following key functions:
#       - Cleans paragraphs using predefined regex patterns.
#       - Identifies and normalizes various date formats to 'YYYY-MM-DD'.
#       - Computes the number of days between extracted dates and the current date.
#       - Filters out false positives like list numbers, isolated punctuation, and URLs.
#       - Reads input text from "text_news.txt" and prints extracted dates with contextual sentence numbering.
# DEPENDENCIES:
#       Created with Python env 3.12.2 (Python version)
#       Dependencies, re, nltk, datetime, dateutil
#
################################################################################

import nltk
import re
from datetime import datetime
from dateutil import parser

nltk.download('punkt')

custom_abbreviations = {
    "Dr.", "Mr.", "Mrs.", "Ms.", "Gov.", "Capt.", "Cmdr.", "Lt.", "Pfc.", "Sgt.", "Rev.", "Ste.", "Ala.", "Tex.",
    "Col.", "Gen.", "Sen.", "St.", "Co.", "Jr.", "Sr.", "Inc.", "Ltd.", "Corp.", "Mt.", "Ave.", "Univ.", "U.S.",
    "D.C.", "p.m.", "a.m.", "etc.", "No.", "i.e.", "e.g.", "pg", "drs", "a.e", "gov", "sgt", "capt"
}

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
tokenizer._params.abbrev_types.update(custom_abbreviations)

compiled_patterns = {
    'select_page_pattern': (re.compile(r'@@\d+'), ''),
    'select_multiple_at': (re.compile(r'(?:\s*@\s*){2,}'), ''),
    'select_multiple_question_marks': (re.compile(r'(?:\s*\?\s*){2,}'), '?'),
    'select_p_tag': (re.compile(r'<p>\s*'), ''),
    'select_h_tag': (re.compile(r'<h>\s*'), ''),
    'extra_space_one': (re.compile(r'\s+,'), ','),
    'extra_space_two': (re.compile(r'\s+\.'), '.'),
    'multiple_space': (re.compile(r'\s+'), ' '),
}

false_positive_patterns = [
    re.compile(r'^\s*\d+\.$'),  # List numbers (1., 2., 3.)
    re.compile(r'^\s*\$\d+(-\$\d+)?$'),  # Dollar amounts ($10, $30-$40)
    re.compile(r'^\s*\d{1,2}:\d{2} (a\.m\.|p\.m\.)$'),  # Time format (9:45 a.m.)
    re.compile(r'^\s*www\.\S+\.\S+$'),  # URLs (www.example.com)
    re.compile(r'^\s*[!?.,"]+\s*$'),  # Isolated punctuation (!, ?, "...")
    re.compile(r'^\s*\([a-zA-Z0-9]+\)$'),  # Parentheses with single words or numbers (pg., (24))
    re.compile(r'^\s*\*+$'),  # Asterisks or repeated symbols (***, **)
    re.compile(r'^\s*[A-Z]\.$'),  # Single-letter abbreviations (A., B., C.)
]

date_patterns = re.compile(
    r'\b(?:'
    r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.? \d{1,2}, \d{4}|'  # Jan. 4, 2025 or Jan 4, 2025
    r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.? \d{1,2}|'  # Jan. 4 or Jan 4 (no year)
    r'\d{4}-\d{2}-\d{2}|'  # YYYY-MM-DD
    r'\d{1,2}/\d{1,2}/\d{4}'  # M/D/YYYY
    r')\b', re.IGNORECASE
)


def clean_paragraph(paragraph: str) -> str:
    """Cleans a paragraph using pre-defined regex patterns."""
    for _, (pattern, replacement) in compiled_patterns.items():
        paragraph = pattern.sub(replacement, paragraph)
    return paragraph.strip()


def extract_dates(sentence: str):
    """Extracts dates from a sentence and normalizes them to YYYY-MM-DD."""
    matches = date_patterns.findall(sentence)
    normalized_dates = []

    for match in matches:
        try:
            if re.match(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.? \d{1,2}$', match, re.IGNORECASE):
                match += ", 2024"

            parsed_date = parser.parse(match)
            normalized_dates.append(parsed_date.date().isoformat())

        except Exception:
            pass

    return normalized_dates


def days_ago(date_str: str) -> int:
    today = datetime.today().date()
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (today - date_obj).days


def is_false_positive(sentence: str) -> bool:
    return any(pattern.match(sentence.strip()) for pattern in false_positive_patterns)


def main():
    try:
        with open("text_news.txt", "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print("Error: The file 'text_news.txt' was not found. Please ensure it exists in the current directory.")
        return

    paragraphs = text.split("\n")
    sentence_number = 0

    for paragraph in paragraphs:
        # sentences = nltk.sent_tokenize(clean_paragraph(paragraph))
        sentences = tokenizer.tokenize(
            clean_paragraph(paragraph))  # use custom tokenizer to identify custom_abbreviations

        for sentence in sentences:
            if is_false_positive(sentence):
                continue  # Skip false positives
            sentence_number += 1
            extracted_dates = extract_dates(sentence)

            if extracted_dates:
                print(f"\n----------------------- SENTENCE: {sentence_number:04d} -----------------------")
                print(f'"{sentence}"')

                for date in extracted_dates:
                    days_since = days_ago(date)
                    print(f"{date} {days_since} days ago")


if __name__ == "__main__":
    main()
