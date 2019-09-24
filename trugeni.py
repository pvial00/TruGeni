import sys, time, subprocess
from os import urandom

class RC4:
    def __init__(self, key):
        self.state = self.init(key)

    def init(self, key):
        state = []
        for i in range(256):
            state.append(i)
        j = 0
        for i in range(256):
            j = (j + state[i] + ord(key[i % len(key)])) % 256
            state[i], state[j] = state[j], state[i]
        return state

    def crypt(self, inbuf):
        j = i = 0
        cipher_text = ""
        for x in range(len(inbuf)):
            i = (i + 1) % 256
            j = (j + self.state[i]) % 256
            self.state[i], self.state[j] = self.state[j], self.state[i]
            k = self.state[(self.state[i] + self.state[j]) % 256]
            cipher_text += chr(k ^ ord(inbuf[x]))
        return cipher_text

def freei():
    cmd = ['df']
    out = subprocess.check_output(cmd)
    free = out.split('\n')[1].split()[6]
    i = int(free[len(free) - 3:]) % 256
    return i


def memtropy():
    cmd = ['vm_stat']
    out = subprocess.check_output(cmd)
    pagesfree = int(out.split('\n')[1].split()[2].strip('.'))
    m = pagesfree % 256
    return m

def numprocs():
    cmd = ['ps', '-ef']
    out = subprocess.check_output(cmd)
    lines = out.split('\n')
    return len(lines) % 256

def sumrxpkts():
    cmd = ['netstat','-b']
    out = subprocess.check_output(cmd)
    lines = out.split('\n')
    lines.pop(0)
    lines.pop(0)
    val = 0
    for line in lines:
        try:
            val = val + int(line.split()[3])
        except (ValueError,IndexError) as ver:
            pass
    return val % 256

def countlines():
    cmd = ['netstat']
    out = subprocess.check_output(cmd)
    lines = out.split('\n')
    return len(lines)

def getinput():
    t = str(int(time.time()))
    s = int(t[len(t) - 3:])
    block = raw_input("Give me entropy!!!")
    t = str(int(time.time()))
    e = int(t[len(t) - 3:])
    diff = e - s
    diff = int((diff % 256))
    return block, diff

def gettime():
    t = str(int(time.time()))
    s = int(t[len(t) - 3:])
    return s % 256

def rc4shuffle():
    msg = "Hello World"
    t = str(int(time.time()))
    s = int(t[len(t) - 3:])
    key = urandom(32)
    ctxt = RC4(key).crypt(msg)
    t = str(int(time.time()))
    e = int(t[len(t) - 3:])
    diff = e - s
    diff = int((diff % 256))
    return diff

def shuffle():
    t = str(int(time.time()))
    s = int(t[len(t) - 3:])
    j = 0
    c = 0
    S = range(256)
    for x in range(768):
        j = (j + S[j]) % 256
        S[c], S[j] = S[j], S[c]
        c = (c + 1) % 256
    t = str(int(time.time()))
    e = int(t[len(t) - 3:])
    diff = e - s
    diff = int((diff % 256))
    return diff
    



def read(filename, bufsize):
    f = open(filename, "a+")
    buf = []
    k = 0
    while True:
        #block, d = getinput()
        i = freei()
        m = memtropy()
        n1 = countlines() % 256
        n2 = numprocs()
        #k = 0
        #for byte in block:
        #    k = (k + ord(byte)) % 256
        s = shuffle()
        r = rc4shuffle()
        p = sumrxpkts()
        k ^= m
        k ^= s
        k ^= r
        k ^= n1
        k ^= n2
        k ^= i
        k ^= p
        #f.write(chr(k))
        buf.append(chr(k))
        if len(buf) == bufsize:
            f.write("".join(buf))
            buf = []

filename = "mybytes"
bufsize = 32
read(filename, bufsize)
