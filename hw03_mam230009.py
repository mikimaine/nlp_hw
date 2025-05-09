#!/usr/bin/env python3

################################################################################
#
# FILE:
#   hw03_mam230009.py
# AUTHOR:
#   Mikiyas Amdu Midru
#   MAM230009
# DESCRIPTION:
#   This program implements an N-gram language model for text generation using
#   natural language processing techniques. It reads text input from a file
#   (default: "gatsby_book.txt"), tokenizes the text into sentences and words,
#   builds various N-gram models (bigram, trigram, 4-gram, and 5-gram), and
#   generates random sentences based on these models.
#
#   The program demonstrates simple language modeling by:
#   1. Processing and tokenizing input text
#   2. Building probability distributions based on N-gram frequencies
#   3. Using these distributions for random text generation
#   4. Handling various text formatting issues including quotation marks and punctuation
#
#   Each generated sentence follows the statistical patterns found in the source text,
#   with higher-order N-grams (4-gram, 5-gram) generally producing more coherent output
#   that better resembles the original text's style and structure.
#
# DEPENDENCIES:
#   - Python 3.12.2 or higher
#   - nltk (Natural Language Toolkit) - for text tokenization
#   - re (Regular Expressions) - for text processing and cleaning
#   - random - for probabilistic sentence generation
#   - sys - for file handling and error reporting
#
# USAGE:
#   Ensure the input text file (gatsby_book.txt) is in the same directory,
#   then run the program with: python hw03_mam230009.py
################################################################################

import re
import random
import sys
import nltk

MAX_LENGTH_STANDARD = 25
MAX_LENGTH_EXTENDED = 100
TRAINING_FILE = "gatsby_book.txt"

def check_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading required NLTK resources...")
        nltk.download('punkt')

def tokenize_into_sentences(text):
    """
    Split text into sentences using NLTK's sentence tokenizer.

    Args:
        text (str): The input text to tokenize

    Returns:
        list: A list of sentences
    """
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    sentences = nltk.sent_tokenize(text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def tokenize_into_words(sentence):
    """
    Split a sentence into words using NLTK's word tokenizer.

    Args:
        sentence (str): The input sentence to tokenize

    Returns:
        list: A list of tokens
    """
    return nltk.word_tokenize(sentence)

def build_ngram_dict(tokens, n):
    """
    Build an n-gram dictionary from a list of tokens.

    Args:
        tokens (list): List of tokens
        n (int): Size of n-gram

    Returns:
        dict: Dictionary mapping n-grams to their counts
    """
    ngram_dict = {}
    for i in range(len(tokens) - n + 1):
        ngram = tuple(tokens[i:i+n])
        ngram_dict[ngram] = ngram_dict.get(ngram, 0) + 1
    return ngram_dict


def build_model_for_generation(ngram_counts, n):
    """
    Transform raw n-gram counts into a model suitable for text generation.

    Args:
        ngram_counts (dict): Dictionary of n-gram counts
        n (int): Size of n-gram

    Returns:
        dict: A dictionary mapping (n-1)-gram prefixes to possible next tokens with counts
    """
    model = {}
    for ngram, count in ngram_counts.items():
        prefix = ngram[:-1]
        next_tok = ngram[-1]
        if prefix not in model:
            model[prefix] = {}
        model[prefix][next_tok] = model[prefix].get(next_tok, 0) + count
    return model


def clean_token_sequence(tokens):
    """
    Clean a sequence of tokens by handling quotation marks and spacing.

    Args:
        tokens (list): List of tokens from the generated sequence

    Returns:
        list: Cleaned list of tokens
    """
    cleaned = [t for t in tokens if t != '``' and t != "''"]
    result = []
    in_quote = False

    for i, token in enumerate(cleaned):
        if token == '"' or token == '``':
            in_quote = True
            result.append('"')
        elif token == '"' or token == "''":
            in_quote = False
            result.append('"')
        else:
            result.append(token)

    return result


def generate_sentence(ngram_counts, n, seed=None, max_length=MAX_LENGTH_STANDARD):
    """
    Generate a sentence using an n-gram model.

    Args:
        ngram_counts (dict): Dictionary of n-gram counts
        n (int): Size of n-gram
        seed (tuple, optional): Starting prefix for generation
        max_length (int, optional): Maximum length of generated sentence

    Returns:
        str: A generated sentence
    """
    model = build_model_for_generation(ngram_counts, n)

    prefix_size = n - 1
    all_prefixes = list(model.keys())
    if not all_prefixes:
        return ""

    if seed is None:
        seed = random.choice(all_prefixes)
    else:
        if len(seed) != prefix_size:
            raise ValueError(f"Seed must have length {prefix_size} for an {n}-gram model")

    current_prefix = seed
    sentence_tokens = list(seed)

    for _ in range(max_length):
        if current_prefix not in model:
            break

        possible_next_dict = model[current_prefix]
        total_counts = sum(possible_next_dict.values())
        rand_val = random.randint(1, total_counts)

        cumulative = 0
        next_token = None
        for token, count in possible_next_dict.items():
            cumulative += count
            if rand_val <= cumulative:
                next_token = token
                break
        sentence_tokens.append(next_token)
        if next_token in [".", "!", "?"] or re.match(r'[.?!]["\']?$', next_token):
            break
        current_prefix = tuple(sentence_tokens[-prefix_size:])

    last_tok = sentence_tokens[-1]
    if not re.match(r'[.?!]["\']?$', last_tok):
        sentence_tokens.append(".")

    clean_tokens = clean_token_sequence(sentence_tokens)

    generated = " ".join(clean_tokens)
    generated = re.sub(r'\s+([,.;:?!])', r'\1', generated)
    generated = re.sub(r'"\s+', '"', generated)
    generated = re.sub(r'\s+"', '"', generated)
    generated = re.sub(r'``|\'\'', '"', generated)
    generated = re.sub(r'\s{2,}', ' ', generated)

    if generated and generated[0].islower():
        generated = generated[0].upper() + generated[1:]

    return generated


def colored_print(text):
    return "\x1b[6;30;42m" + text + "\x1b[0m"


def process_text_file(filename):
    """
    Read and process a text file, building n-gram models and generating sample sentences.

    Args:
        filename (str): Path to the text file
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"File {filename} not found.")
        sys.exit(1)

    sentences = tokenize_into_sentences(text)
    print(f"Processed {len(sentences)} sentences from {filename}")

    ngram_dicts = {2: {}, 3: {}, 4: {}, 5: {}}

    for idx, sentence in enumerate(sentences, start=1):
        print(f"Sentence {idx:03d} ----------------------------")
        print(sentence)
        print()

        tokens = tokenize_into_words(sentence)

        for n in ngram_dicts:
            if len(tokens) >= n:  # Only update if sentence has enough tokens
                sentence_ngrams = build_ngram_dict(tokens, n)
                for ngram, count in sentence_ngrams.items():
                    ngram_dicts[n][ngram] = ngram_dicts[n].get(ngram, 0) + count

    for n, ngram_dict in ngram_dicts.items():
        print(f"\n==== Example: Generating a random sentence {colored_print(f'({n}-gram)')} ===\n")
        max_len = MAX_LENGTH_EXTENDED if n > 3 else MAX_LENGTH_STANDARD
        random_sentence = generate_sentence(ngram_dict, n, seed=None, max_length=max_len)
        print(random_sentence)


def main():
    check_nltk_resources()
    process_text_file(TRAINING_FILE)


if __name__ == "__main__":
    main()