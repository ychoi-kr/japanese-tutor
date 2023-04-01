import re

def split_text_by_brackets(text):
    inside_brackets_pattern = r'\((.*?)\)'
    outside_brackets_pattern = r'(.*?)(?=\()|(?<=\))(.*?)(?=\()|(?<=\))(.*?)'

    inside_brackets = re.findall(inside_brackets_pattern, text)
    outside_brackets = [match[0] or match[1] or match[2] for match in re.findall(outside_brackets_pattern, text)]

    return ''.join(outside_brackets), ''.join(inside_brackets)


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

