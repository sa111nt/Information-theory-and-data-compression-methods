import random
import re
import numpy as np
from string import ascii_lowercase

def clean_text(text):
    text = re.sub(r'\d+', '', text)
    return re.sub(r' +', ' ', text)

def get_ngram_probs(text, n):
    ngram_counts = {}
    for i in range(len(text) - n + 1):
        ngram = text[i:i + n]
        if not any(char.isdigit() for char in ngram):
            ngram_counts[tuple(ngram)] = ngram_counts.get(tuple(ngram), 0) + 1
    total_count = sum(ngram_counts.values())
    return {k: v / total_count for k, v in ngram_counts.items()}

def get_conditional_probs(text, n):
    ngram_probs = get_ngram_probs(text, n)
    ngram_plus_one_probs = get_ngram_probs(text, n + 1)
    cond_probs = {}
    for ngram in ngram_probs:
        cond_probs[ngram] = {}
        for letter in ascii_lowercase + ' ':
            cond_probs[ngram][letter] = ngram_plus_one_probs.get(ngram + (letter,), 0) / ngram_probs[ngram]
        total_prob = sum(cond_probs[ngram].values())
        if total_prob > 0:
            for letter in cond_probs[ngram]:
                cond_probs[ngram][letter] /= total_prob
    return cond_probs

def generate_text(start_seq, source_text, n, length):
    cond_probs = get_conditional_probs(source_text, n)
    generated_text = start_seq
    for _ in range(length):
        next_ngram = tuple(generated_text[-n:])
        next_letter = random.choices(list(ascii_lowercase + ' '), weights=cond_probs.get(next_ngram, {}).values(), k=1)
        generated_text += next_letter[0]
    return generated_text

def get_avg_word_length(text):
    words = text.split()
    return round(np.mean([len(word) for word in words]), 2)

with open("norm_hamlet.txt", 'r') as file:
    text = clean_text(file.read(1000000))

for order in [1, 3, 5]:
    print(f"\norder {order}:\n")
    generated = generate_text('probability', text, order, 2000)
    print(generated)
    print(f"\nAverage word length: {get_avg_word_length(generated)}")
