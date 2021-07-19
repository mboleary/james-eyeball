import time
from adafruit_servokit import ServoKit
import socket
import cryptography
import cryptography.fernet
import json

kit = ServoKit(channels=16)

KEY="KM0ZRVIljWKiBLy293Al4Qm1VqbLF2at4gxLfoqtT7o="
HOST = "172.31.1.234"
PORT = 65123
PANSERVO = 1
TILTSERVO = 0

f = cryptography.fernet.Fernet(KEY)

kit.servo[PANSERVO].angle = 100
kit.servo[TILTSERVO].angle = 100

global lasterror
lasterror = ""

def send_status(conn):
    try:
        conn.sendall(f.encrypt(json.dumps({
            "pan": kit.servo[PANSERVO].angle,
            "tilt": kit.servo[TILTSERVO].angle,
            "error": lasterror
        }).encode("ascii")))
    except Exception as e:
        print(e)

def handler(msg, conn):
    global lasterror
    print("got message of length {}".format(len(msg)))

    try:
        msg = f.decrypt(msg).decode("ascii").strip()
    except Exception as e:
        print("failed to decrypt message")
        lasterror = str(e)
        return

    print("decrypted message: {}".format(msg))

    if msg == "status":
        send_status(conn)

    elif len(msg.split()) == 2:
        cmd = msg.split()[0].strip()
        arg = msg.split()[1].strip()
        print("cmd='{}', arg='{}'".format(cmd, arg))
        try:
            arg = int(arg)
        except Exception as e:
            print("failed to decode argument: {}".format(e))
            lasterror = str(e)
            return

        try:
            if cmd == "left":
                kit.servo[PANSERVO].angle = kit.servo[PANSERVO].angle + arg

            elif cmd == "right":
                kit.servo[PANSERVO].angle = kit.servo[PANSERVO].angle - arg

            elif cmd == "up":
                if kit.servo[TILTSERVO].angle  > 75:
                    kit.servo[TILTSERVO].angle = kit.servo[TILTSERVO].angle - arg
                else:
                    kit.servo[TILTSERVO].angle = 75

            elif cmd == "down":
                kit.servo[TILTSERVO].angle = kit.servo[TILTSERVO].angle + arg
        except Exception as e:
            lasterror = str(e)
            print("failed to run command: {}".format(e))

        send_status(conn)

    else:
        conn.sendall(f.encrypt("don't know how to handle your command '{}'".format(msg).encode("ascii")))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()

    while True:
        print("waiting for connection... ")
        conn, addr = s.accept()
        with conn:
            lasterror = ""
            print("got connection from {}".format(addr))
            data = []
            while True:
                recvd = conn.recv(1024)
                data.append(recvd)
                if len(recvd) < 1024:
                    break
            handler(b''.join(data), conn)
            conn.close()

