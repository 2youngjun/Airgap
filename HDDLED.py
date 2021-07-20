import zlib
import binascii
import os
import time

BLOCK_SIZE = 512

if hasattr(os, 'sync'):
    sync = os.sync
else:
    import ctypes
    libc = ctypes.CDLL("libc.so.6")

    def sync():
        libc.sync()