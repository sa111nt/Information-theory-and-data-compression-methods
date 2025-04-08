from bitarray import bitarray
from math import log2, ceil
from collections import Counter

ALPHABET = ' abcdefghijklmnopqrstuvwxyz0123456789'


def analyze_text(text):
    count = Counter(c for c in text if c in ALPHABET)
    sorted_letters = [char for char, _ in count.most_common()]
    return sorted_letters


def generate_codebook(symbols):
    bit_len = ceil(log2(len(symbols)))
    encode_map = {char: format(i, f'0{bit_len}b') for i, char in enumerate(symbols)}
    decode_map = {v: k for k, v in encode_map.items()}
    return encode_map, decode_map, bit_len


def read_file(path, limit=0):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content[:limit] if limit > 0 else content


def encode(text, codebook):
    bits = bitarray()
    for c in text:
        bits.extend(codebook[c])
    pad_size = (8 - (len(bits) + 3) % 8) % 8
    offset_bits = format(pad_size, '03b')
    result = bitarray(offset_bits) + bits + bitarray('0' * pad_size)
    return result


def decode(bits, decode_map, bit_len):
    pad = int(bits[:3].to01(), 2)
    data = bits[3:len(bits) - pad]
    output = []
    for i in range(0, len(data), bit_len):
        chunk = data[i:i + bit_len].to01()
        output.append(decode_map[chunk])
    return ''.join(output)


def save(encoded, codebook, encoded_path='encoded_output.bin', code_path='codebook.txt'):
    with open(encoded_path, 'wb') as file:
        file.write(encoded.tobytes())
    with open(code_path, 'w', encoding='utf-8') as file:
        file.write(''.join(codebook.keys()))


def load(encoded_path='encoded_output.bin', code_path='codebook.txt'):
    with open(encoded_path, 'rb') as file:
        bits = bitarray()
        bits.frombytes(file.read())
    with open(code_path, 'r', encoding='utf-8') as file:
        symbols = list(file.read())
    enc, dec, bit_len = generate_codebook(symbols)
    return bits, enc, dec, bit_len


sample_text = read_file('norm_wiki_sample.txt')
symbols = analyze_text(sample_text)
encode_map, decode_map, code_len = generate_codebook(symbols)
compressed = encode(sample_text, encode_map)
save(compressed, encode_map)
loaded_bits, enc_map, dec_map, loaded_len = load()
restored_text = decode(loaded_bits, dec_map, loaded_len)

if restored_text == sample_text:
    print("tekst został przywrócony bez błędów.")
else:
    print("oryginalny i przywrócony tekst różnią się.")
