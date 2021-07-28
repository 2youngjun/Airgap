import zlib
import binascii
import os
import time

BLOCK_SIZE = 512

# os.sync(): is used to force write of everything to disk.
# sync() causes all buffered modifications to file metadata and data to be written to the underlying file systems.
# python call to do this
if hasattr(os, 'sync'):
    sync = os.sync
else:
    import ctypes
    libc = ctypes.CDLL("libc.so.6")

    def sync():
        libc.sync()

# linux cognizes all devices as file
def transmit_bits(tmpfile, bits, T0, readsize):
    sync()  # drop cache
    fp = open(tmpfile)
    offset = 0
    offsetincrement = BLOCK_SIZE
    fp.seek(offset)
    for b in list(bits):
        # sync()
        if (b == '0'):
            print("0 sleep " + str(T0))
            time.sleep(T0)
        if (b == '1'):
            sync()
            fp.seek(offset)
            print("1 read %d bytes" % len(fp.read(readsize)))
            offset += offsetincrement

# encoding method
def manchester(bits):
    r = ""
    for b in list(bits):
        if b == '0':
            r += '01'
        if b == '1':
            r += '10'
    return r


# replace integer -> binary, '0b' -> ''
def itob(i):
    return bin(i).replace('0b', '')


# str -> hexa str -> hexa int
def atob(a):
    return itob(int(binascii.hexlify(a), 16))


def itob32(i):
    return itob(i).zfill(32)


def itob16(i):
    return itob(i).zfill(16)


def transmit_packet(payload):
    preamble = "10101010"
    payload_size = len(payload)
    payload = payload.encode('utf8')
    print("preamble, size, payload, crc32")
    print(preamble, itob16(payload_size),
            atob(payload),
            itob32(zlib.crc32(payload)))
    dataONOFF = manchester(preamble +
                itob16(payload_size) +
                atob(payload) +
                itob32(zlib.crc32(payload)))
    print(dataONOFF)
    time.sleep(1)
    transmit_bits('/dev/disk3s6', dataONOFF, 0.01, 4096)


def main():
    while True:
        transmit_packet("leeyoungjun")


if __name__ == "__main__":
    main()