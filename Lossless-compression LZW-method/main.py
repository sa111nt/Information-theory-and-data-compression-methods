
def lzw_compress(input_bytes, max_dict_size=None):
    dict_size = 256
    dictionary = {bytes([i]): i for i in range(dict_size)}
    w = b""
    result = []

    for c in input_bytes:
        wc = w + bytes([c])
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            if max_dict_size is None or dict_size < max_dict_size:
                dictionary[wc] = dict_size
                dict_size += 1
            w = bytes([c])
    if w:
        result.append(dictionary[w])
    return result

def lzw_decompress(compressed, max_dict_size=None):
    dict_size = 256
    dictionary = {i: bytes([i]) for i in range(dict_size)}
    result = bytearray()

    w = bytes([compressed.pop(0)])
    result += w

    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[:1]
        else:
            raise ValueError("Nieprawidłowy kod: %s" % k)
        result += entry
        if max_dict_size is None or dict_size < max_dict_size:
            dictionary[dict_size] = w + entry[:1]
            dict_size += 1
        w = entry
    return bytes(result)

def compress_and_analyze(input_path, max_dict_size=None):
    with open(input_path, 'rb') as f:
        original_data = f.read()

    compressed = lzw_compress(original_data, max_dict_size)
    decompressed = lzw_decompress(compressed.copy(), max_dict_size)

    assert original_data == decompressed, "Błąd: dane po dekompresji nie są identyczne z oryginałem"

    original_size = len(original_data)
    compressed_size = len(compressed) * 3  # 3 bajty na kod
    ratio = (compressed_size / original_size) * 100
    return original_size, compressed_size, ratio

if __name__ == "__main__":
    files = ["norm_wiki_sample.txt", "wiki_sample.txt", "lena.bmp"]
    dict_limits = [None, 2**12, 2**18]

    for file in files:
        print(f"\nAnaliza pliku: {file}")
        for limit in dict_limits:
            tag = "bez ograniczeń" if limit is None else f"słownik {limit}"
            try:
                orig, comp, ratio = compress_and_analyze(file, limit)
                print(f"  {tag:>15}: {comp} bajtów ({ratio:.2f}%)")
            except Exception as e:
                print(f"  {tag:>15}: Błąd — {e}")
