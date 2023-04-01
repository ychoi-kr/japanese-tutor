def contains_japanese(text):
    for char in text:
        if ('\u3040' <= char <= '\u309F'  # Hiragana
                or '\u30A0' <= char <= '\u30FF'  # Katakana
                or '\u4E00' <= char <= '\u9FFF'):  # CJK Unified Ideographs
            return True
    return False


def contains_korean(text):
    for char in text:
        if ('\uAC00' <= char <= '\uD7A3'  # Hangul Syllables
                or '\u1100' <= char <= '\u11FF'  # Hangul Jamo
                or '\u3130' <= char <= '\u318F'):  # Hangul Compatibility Jamo
            return True
    return False

