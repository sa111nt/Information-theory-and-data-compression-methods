import math
import operator
from collections import defaultdict

CHAR_SET = ' abcdefghijklmnopqrstuvwxyz0123456789'


def compute_frequencies(data, n):
    freqs = defaultdict(int)
    total = len(data) - n + 1
    for i in range(total):
        sequence = tuple(data[i:i + n])
        freqs[sequence] += 1
    for seq in freqs:
        freqs[seq] /= total
    return freqs


def entropy(freqs):
    return -sum(p * math.log2(p) for p in freqs.values())


def entropy_conditional(freqs, cond_freqs):
    return -sum(freqs[k + (sub_k,)] * math.log2(p) for k, v in cond_freqs.items() for sub_k, p in v.items())


def normalize_probs(freqs):
    total = sum(freqs.values())
    for key in freqs:
        freqs[key] /= total


def conditional_probabilities(data, n):
    cond_freqs = defaultdict(lambda: defaultdict(float))
    freqs_n = compute_frequencies(data, n)
    freqs_np1 = compute_frequencies(data, n + 1)

    for seq in freqs_np1:
        cond_freqs[seq[:-1]][seq[-1]] = freqs_np1[seq] / freqs_n[seq[:-1]]

    for seq in cond_freqs:
        normalize_probs(cond_freqs[seq])

    return freqs_np1, cond_freqs




def analyze_text(file_path, lang):
    with open(file_path, 'r') as file:
        content = file.read()
    words = content.split()

    print(lang)
    print('Entropy (characters):', entropy(compute_frequencies(content, 1)))

    for i in range(1, 4):
        freqs, cond_freqs = conditional_probabilities(content, i)
        print(f'Conditional Entropy (order {i}):', entropy_conditional(freqs, cond_freqs))

    print('\nEntropy (words):', entropy(compute_frequencies(words, 1)))

    for i in range(1, 4):
        freqs, cond_freqs = conditional_probabilities(words, i)
        print(f'Conditional Entropy (order {i}):', entropy_conditional(freqs, cond_freqs))

    print('\n' + '-' * 50 + '\n')


language_files = {
    'English': 'norm_wiki_en.txt',
    'Latin': 'norm_wiki_la.txt',
    'Esperanto': 'norm_wiki_eo.txt',
    'Estonian': 'norm_wiki_et.txt',
    'Haitian': 'norm_wiki_ht.txt',
    'Navaho': 'norm_wiki_nv.txt',
    'Somali': 'norm_wiki_so.txt'
}

for lang, file in language_files.items():
    analyze_text(file, lang)

for i in range(0,6):
    analyze_text(f'sample{i}.txt', f'SAMPLE {i}')
