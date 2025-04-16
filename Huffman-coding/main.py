from bitarray import bitarray
from collections import Counter
from heapq import heappush, heappop, heapify
from math import log2
import ast

ALPHABET = ' abcdefghijklmnopqrstuvwxyz0123456789'


def analyze_text(text):
    count = Counter(c for c in text if c in ALPHABET)
    total = sum(count.values())
    return {char: freq / total for char, freq in count.items()}


def build_huffman_code(freqs):
    heap = [[weight, [symbol, '']] for symbol, weight in freqs.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    codebook = {symbol: code for symbol, code in heap[0][1:]}
    return codebook



def invert_codebook(codebook):
    return {code: symbol for symbol, code in codebook.items()}


def average_code_length(freqs, codebook):
    return sum(len(codebook[symbol]) * freq for symbol, freq in freqs.items())


def entropy(freqs):
    return -sum(p * log2(p) for p in freqs.values())

def decode(bits, decode_map):
    output = []
    buffer = ''
    for bit in bits.to01():
        buffer += bit
        if buffer in decode_map:
            output.append(decode_map[buffer])
            buffer = ''
    return ''.join(output)


def encode(text, codebook):
    bits = bitarray()
    for c in text:
        if c in codebook:
            bits.extend(codebook[c])
    return bits


def save(encoded, codebook, encoded_path='encoded_output.bin', code_path='codebook.txt'):
    with open(encoded_path, 'wb') as f:
        length = len(encoded)
        f.write(length.to_bytes(4, byteorder='big'))
        f.write(encoded.tobytes())

    with open(code_path, 'w', encoding='utf-8') as f:
        for symbol, code in codebook.items():
            f.write(f'{repr(symbol)}:{code}\n')


def load(encoded_path='encoded_output.bin', code_path='codebook.txt'):
    with open(encoded_path, 'rb') as f:
        length_bytes = f.read(4)
        length = int.from_bytes(length_bytes, byteorder='big')
        bits = bitarray()
        bits.frombytes(f.read())
        bits = bits[:length]

    codebook = {}
    with open(code_path, 'r', encoding='utf-8') as f:
        for line in f:
            symbol_repr, code = line.strip().split(':', 1)
            symbol = ast.literal_eval(symbol_repr)
            codebook[symbol] = code

    decode_map = invert_codebook(codebook)
    return bits, codebook, decode_map

def read_file(path, limit=0):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().lower()
    return ''.join(c for c in content if c in ALPHABET)[:limit] if limit > 0 else ''.join(c for c in content if c in ALPHABET)


sample_text = read_file('norm_wiki_sample.txt')
sample_text = ''.join(c for c in sample_text if c in ALPHABET)

freqs = analyze_text(sample_text)
codebook = build_huffman_code(freqs)
decode_map = invert_codebook(codebook)
compressed = encode(sample_text, codebook)
save(compressed, codebook)
loaded_bits, loaded_codebook, loaded_decode_map = load()
restored_text = decode(loaded_bits, loaded_decode_map)

H = entropy(freqs)
L = average_code_length(freqs, codebook)
eff = H / L

print(f"Entropia H = {H:.4f}")
print(f"Średnia długość kodu L = {L:.4f}")
print(f"Efektywność kodowania = {eff * 100:.2f}%")

if restored_text == sample_text:
    print("Tekst został poprawnie odtworzony")
else:
    print("Oryginalny i przywrócony tekst różnią się")

