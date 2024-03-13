import socket
import time

import cv2
import numpy as np

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3333  # The port used by the server

if __name__ == "__main__":
    width = 344
    height = 244
    channels = 3
    data_type = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        images = []
        for i in range(1, 4):
            img = cv2.imread(f"test_images/test_img{i}.jpg", cv2.IMREAD_COLOR)
            resized = cv2.resize(
                img, dsize=(width, height), interpolation=cv2.INTER_CUBIC
            )
            images.append(resized)

        s.sendall(len(images[0].tobytes()).to_bytes(4, byteorder="big"))
        s.sendall(width.to_bytes(4, byteorder="big"))
        s.sendall(height.to_bytes(4, byteorder="big"))
        s.sendall(channels.to_bytes(4, byteorder="big"))
        s.sendall(data_type.to_bytes(1, byteorder="big"))  # padding

        for i in range(100):
            s.sendall(images[i % 3].tobytes())
            time.sleep(0.5)
