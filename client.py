#!/usr/bin/env python3

import cryptography
import cryptography.fernet
import sys
import socket

KEY="KM0ZRVIljWKiBLy293Al4Qm1VqbLF2at4gxLfoqtT7o="
HOST = "0.0.0.0"
PORT = 65123

f = cryptography.fernet.Fernet(KEY)

msg = "\n".join([line for line in sys.stdin])
msg = f.encrypt(msg.encode("ascii"))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(msg)

    data = []
    while True:
        recvd = s.recv(1024)
        data.append(recvd)
        if len(recvd) < 1024:
            break

    data = b''.join(data)
    try:
        response = f.decrypt(data)
    except Exception as e:
        print("Failed to decode response: {}".format(e))
        sys.exit(1)

    print(response.decode("ascii"))

