#!/usr/bin/env python3

################################################################################
#
# FILE:
#   hw03_mam230009.py
# AUTHOR:
#   Mikiyas Amdu Midru
#   MAM230009
# DESCRIPTION:
#   Homework 3

# DEPENDENCIES:
#       Created with Python env 3.12.2 (Python version)
#       Dependencies, re, nltk, datetime, dateutil
#
################################################################################
import re
import random
import sys
import nltk

def tokenize_into_sentences(text):
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    sentences = nltk.sent_tokenize(text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def build_ngram_dicts():
    return {}, {}, {}, {}

def update_ngram_dict(ngram_dict, tokens, n):
    for i in range(len(tokens) - n +1):
        ngram = tuple(tokens[i:i+n])
        if ngram in ngram_dict:
            ngram_dict[ngram] += 1
        else:
            ngram_dict[ngram] = 1
def tokenize_into_words(sentence):
    return nltk.word_tokenize(sentence)

def build_model_for_generation(ngram_counts, n):
    model = {}
    for ngram, count in ngram_counts.items():
        prefix = ngram[:-1]
        next_tok = ngram[-1]
        if prefix not in model:
            model[prefix] = {}
        model[prefix][next_tok] = model[prefix].get(next_tok, 0) + count
    return model

def generate_sentence(ngram_counts, n, seed=None, max_length=25):
    model = build_model_for_generation(ngram_counts, n)

    prefix_size = n -1
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
            cumulative +=count
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
    generated = " ".join(sentence_tokens)
    return generated
def colored_print(text):
    return  "\x1b[6;30;42m" + text + "\x1b[0m"

def main():
    filename = "gatsby_book.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"File {filename} not found.")
        sys.exit(1)

    sentences = tokenize_into_sentences(text)

    bigram_dict, trigram_dict, fourgram_dict, fivegram_dict = build_ngram_dicts()

    for idx, sentence in enumerate(sentences, start=1):
        print(f"Sentence {idx:03d} ----------------------------")

        print(sentence)
        print()

        tokens = tokenize_into_words(sentence)

        update_ngram_dict(bigram_dict, tokens, 2)
        update_ngram_dict(trigram_dict, tokens, 3)
        update_ngram_dict(fourgram_dict, tokens, 4)
        update_ngram_dict(fivegram_dict, tokens, 5)

    print("\n==== Example: Generating a random sentence " + colored_print('(Bigram)') + " ===\n")
    bigram_random_sentence = generate_sentence(bigram_dict, 2, seed=None, max_length=25)
    print(bigram_random_sentence)

    print("\n==== Example: Generating a random sentence " + colored_print('(Trigram)') + " ===\n")
    trigram_random_sentence = generate_sentence(trigram_dict, 3, seed=None, max_length=25)
    print(trigram_random_sentence)

    print("\n==== Example: Generating a random sentence " + colored_print('(Fourgram)') + " ===\n")
    fourgram_random_sentence = generate_sentence(fourgram_dict, 4, seed=None, max_length=100)
    print(fourgram_random_sentence)

    print("\n==== Example: Generating a random sentence " + colored_print('(Fivegram)') + " ===\n")
    fivegram_random_sentence = generate_sentence(fivegram_dict, 5, seed=None, max_length=100)
    print(fivegram_random_sentence)

if __name__ == "__main__":
    main()
