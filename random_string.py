# -*- coding: utf-8 -*-
import string
import random

def generate_random_string(length):
    excluded_chars = "\"'\\`^"
    characters = ''.join(c for c in (string.ascii_letters + string.digits + string.punctuation) if c not in excluded_chars)
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

length = int(input())

for i in range(50):
    print(generate_random_string(length))
