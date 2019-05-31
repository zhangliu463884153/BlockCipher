
import sys
sys.path.append('..')

import os
import random

try:
    from StringIO import StringIO
except:
    import io
    StringIO = io.BytesIO

import pyaes
from pyaes.blockfeeder import Decrypter, Encrypter
from pyaes import decrypt_stream, encrypt_stream
from pyaes.util import to_bufferable


key = os.urandom(32)

plaintext = os.urandom(1000)

for mode_name in pyaes.AESModesOfOperation:
    mode = pyaes.AESModesOfOperation[mode_name]
    print(mode.name)

    kw = dict(key = key)
    if mode_name in ('cbc', 'cfb', 'ofb'):
        kw['iv'] = os.urandom(16)

    encrypter = Encrypter(mode(**kw))
    ciphertext = to_bufferable('')

    # Feed the encrypter random number of bytes at a time
    index = 0
    while index < len(plaintext):
        length = random.randint(1, 128)
        if index + length > len(plaintext): length = len(plaintext) - index
        ciphertext += encrypter.feed(plaintext[index: index + length])
        index += length
    ciphertext += encrypter.feed(None)

    decrypter = Decrypter(mode(**kw))
    decrypted = to_bufferable('')

    # Feed the decrypter random number of bytes at a time
    index = 0
    while index < len(ciphertext):
        length = random.randint(1, 128)
        if index + length > len(ciphertext): length = len(ciphertext) - index
        decrypted += decrypter.feed(ciphertext[index: index + length])
        index += length
    decrypted += decrypter.feed(None)

    passed = decrypted == plaintext
    cipher_length = len(ciphertext)
    print("  cipher-length=%(cipher_length)s passed=%(passed)s" % locals())

# Test block modes of operation with no padding
plaintext = os.urandom(1024)

for mode_name in ['ecb']:
    mode = pyaes.AESModesOfOperation[mode_name]
    print(mode.name + ' (no padding)')

    kw = dict(key = key)

    encrypter = Encrypter(mode(**kw), padding = pyaes.PADDING_NONE)
    ciphertext = to_bufferable('')

    # Feed the encrypter random number of bytes at a time
    index = 0
    while index < len(plaintext):
        length = random.randint(1, 128)
        if index + length > len(plaintext): length = len(plaintext) - index
        ciphertext += encrypter.feed(plaintext[index: index + length])
        index += length
    ciphertext += encrypter.feed(None)

    if len(ciphertext) != len(plaintext):
        print('  failed to encrypt with correct padding')

    decrypter = Decrypter(mode(**kw), padding = pyaes.PADDING_NONE)
    decrypted = to_bufferable('')

    # Feed the decrypter random number of bytes at a time
    index = 0
    while index < len(ciphertext):
        length = random.randint(1, 128)
        if index + length > len(ciphertext): length = len(ciphertext) - index
        decrypted += decrypter.feed(ciphertext[index: index + length])
        index += length
    decrypted += decrypter.feed(None)

    passed = decrypted == plaintext
    cipher_length = len(ciphertext)
    print("  cipher-length=%(cipher_length)s passed=%(passed)s" % locals())

plaintext = os.urandom(1000)

for mode_name in pyaes.AESModesOfOperation:
    mode = pyaes.AESModesOfOperation[mode_name]
    print(mode.name + ' (stream operations)')

    kw = dict(key = key)
    if mode_name in ('cbc', 'cfb', 'ofb'):
        kw['iv'] = os.urandom(16)

    moo = mode(**kw)
    output = StringIO()
    pyaes.encrypt_stream(moo, StringIO(plaintext), output)
    output.seek(0)
    ciphertext = output.read()

    moo = mode(**kw)
    output = StringIO()
    pyaes.decrypt_stream(moo, StringIO(ciphertext), output)
    output.seek(0)
    decrypted = output.read()

    passed = decrypted == plaintext
    cipher_length = len(ciphertext)
    print("  cipher-length=%(cipher_length)s passed=%(passed)s" % locals())

