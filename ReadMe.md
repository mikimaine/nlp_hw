# Homework Assignments Repository

This repository contains various NLP homework assignments completed by me. Each assignment is implemented in Python and processes different text files to perform specific tasks.

## Table of Contents

- [hw01_mam230009.py](#hw01_mam230009py)
- [hw02_mam230009.py](#hw02_mam230009py)
- [hw03_mam230009.py](#hw03_mam230009py)
- [Dependencies](#dependencies)
- [Usage](#usage)

## hw01_mam230009.py

**Description:**
This script processes the edited Treasure Island text file (`ti.txt`) as follows:
1. Reads the edited file.
2. Inserts spaces around punctuation so that every token is atomic.
3. Splits the text into a list of word tokens.
4. Counts word frequencies ignoring case.
5. Sorts the words by descending frequency.
6. Displays the top 10 most frequent words (ignoring punctuation), along with the count and the relative frequency.

**Dependencies:**
- Python 3.12.2
- `re`
- `string`

## hw02_mam230009.py

**Description:**
This script processes a text file (`text_news.txt`) to extract and normalize dates from sentences. It uses a custom NLTK tokenizer with additional abbreviations to improve sentence tokenization. The script performs the following key functions:
- Cleans paragraphs using predefined regex patterns.
- Identifies and normalizes various date formats to 'YYYY-MM-DD'.
- Computes the number of days between extracted dates and the current date.
- Filters out false positives like list numbers, isolated punctuation, and URLs.
- Reads input text from `text_news.txt` and prints extracted dates with contextual sentence numbering.

**Dependencies:**
- Python 3.12.2
- `re`
- `nltk`
- `datetime`
- `dateutil`

## hw03_mam230009.py

**Description:**
This program implements an N-gram language model for text generation using natural language processing techniques. It reads text input from a file (default: `gatsby_book.txt`), tokenizes the text into sentences and words, builds various N-gram models (bigram, trigram, 4-gram, and 5-gram), and generates random sentences based on these models. The program demonstrates simple language modeling by:
1. Processing and tokenizing input text.
2. Building probability distributions based on N-gram frequencies.
3. Using these distributions for random text generation.
4. Handling various text formatting issues including quotation marks and punctuation.

**Dependencies:**
- Python 3.12.2
- `nltk`
- `re`
- `random`
- `sys`

## Dependencies

All scripts are created with Python 3.12.2. The required dependencies for each script are mentioned in their respective sections.

## Usage

To run any of the scripts, ensure that the required text files are in the same directory as the script. Then, execute the script using Python:

```sh
python hw01_mam230009.py
python hw02_mam230009.py
python hw03_mam230009.py
```
Make sure to install the necessary dependencies using pip:

`pip install -r requirements.txt`
