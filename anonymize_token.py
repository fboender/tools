#!/usr/bin/python

import argparse
import sys
import string
import random

char_class_mappings = [
    string.ascii_lowercase,
    string.ascii_uppercase,
    string.digits,
]

def get_anon_char(c, char_class_mapping, mask=False):
    if mask is True:
        if char_class_mapping is string.ascii_lowercase:
            return 'x'
        elif char_class_mapping is string.ascii_uppercase:
            return 'X'
        elif char_class_mapping is string.digits:
            return '0'
        else:
            return c
    else:
        return random.choice(char_class_mapping)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Anonymize a secret token (read from stdin)"
    )
    parser.add_argument(
        "-m",
        action="store_true",
        dest="mask",
        default=False,
        help="Mask instead of randomize"
    )
    args = parser.parse_args()

    sys.stdout.write("Token: ")
    if sys.version_info.major > 2:
        in_token = input()
    else:
        in_token = raw_input()

    # Go through each char in input and map it to a random matching char.
    result = ""
    for char in in_token:
        for char_class_mapping in char_class_mappings:
            if char in char_class_mapping:
                result += get_anon_char(char, char_class_mapping, args.mask)
                break  # Continue to next char
        else:
            # No match found. Just use original char
            result += char

    assert(len(in_token) == len(result))
    print(result)
