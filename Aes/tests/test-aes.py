

import sys
sys.path.append('..')

from pyaes import *

import os, time

# Python 3 doesn't have xrange and returns bytes from urandom
try:
    xrange
except NameError:
    xrange = range
else:
    pass

# compare against a known working implementation
for mode in [ 'ECB' ]:

    (tt_ksetup, tt_kencrypt, tt_kdecrypt) = (0.0, 0.0, 0.0)
    (tt_setup, tt_encrypt, tt_decrypt) = (0.0, 0.0, 0.0)
    count = 0

    for key_size in (128, 192, 256):

        for test in xrange(1, 8):
            key = os.urandom(key_size // 8)

            if mode == 'ECB':
                plaintext = [ os.urandom(16) for x in xrange(0, test) ]

                t0 = time.time()
                aes = AESModeOfOperationECB(key)
                tt_setup += time.time() - t0

            count += 1

            t0 = time.time()
            enc = [aes.encrypt(p) for p in plaintext]
            tt_encrypt += time.time() - t0

    print("Mode: %s" % mode)
    print("encrypt=%fs"  % (tt_encrypt / count))
    print("decrypt=%fs"  % (tt_decrypt / count))
    print("setup=%f" % (tt_setup / count))


