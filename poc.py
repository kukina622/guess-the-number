import os
import random
import re
import socket
import time
def inverse_right(res, shift, bits=32):
    tmp = res
    for i in range(bits // shift):
        tmp = res ^ tmp >> shift
    return tmp


# right shift with mask inverse
def inverse_right_mask(res, shift, mask, bits=32):
    tmp = res
    for i in range(bits // shift):
        tmp = res ^ tmp >> shift & mask
    return tmp

# left shift inverse
def inverse_left(res, shift, bits=32):
    tmp = res
    for i in range(bits // shift):
        tmp = res ^ tmp << shift
    return tmp


# left shift with mask inverse
def inverse_left_mask(res, shift, mask, bits=32):
    tmp = res
    for i in range(bits // shift):
        tmp = res ^ tmp << shift & mask
    return tmp


def extract_number(y):
    y = y ^ y >> 11
    y = y ^ y << 7 & 2636928640
    y = y ^ y << 15 & 4022730752
    y = y ^ y >> 18
    return y&0xffffffff

def recover(y):
    y = inverse_right(y,18)
    y = inverse_left_mask(y,15,4022730752)
    y = inverse_left_mask(y,7,2636928640)
    y = inverse_right(y,11)
    return y&0xffffffff

def _int32(x):
    return int(0xFFFFFFFF & x)


def twist(state):
    for i in range(0, 624):
        y = _int32((state[i] & 0x80000000) + (state[(i + 1) % 624] & 0x7fffffff))
        state[i] = (y >> 1) ^ state[(i + 397) % 624]

        if y % 2 != 0:
            state[i] = state[i] ^ 0x9908b0df
    return state



def netcat(hostname, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(20)
    s.connect((hostname, port))
    s.recv(1024).decode(encoding='UTF-8')

    state = []
    while 1:
        if len(state) < 624:
            time.sleep(0.3)
            s.sendall("123\n".encode())
            time.sleep(0.3)
            data = s.recv(1024).decode(encoding='UTF-8')
            print(data)
            x = re.findall("[0-9]+", data)[0]
            state.append(recover(int(x)))
            print(f"state count:{len(state)}")
        else:
            print(len(state))
            state = twist(state)
            next = extract_number(state[0])
            s.sendall(f"{next}\n".encode())
            time.sleep(0.2)
            print(f"BBB{next}")
            time.sleep(0.2)
            data = s.recv(1024).decode(encoding='UTF-8')

            print("Received:", data)
            break
    
    s.shutdown(socket.SHUT_WR)
    print("Connection closed.")
    s.close()


netcat("127.0.0.1",8005)
