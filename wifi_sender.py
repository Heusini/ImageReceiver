import socket
import sys
import time

import cv2
import numpy as np

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3333  # The port used by the server


def sample_test_images():
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

        for i in range(10000):
            s.sendall(images[i % 3].tobytes())
            # time.sleep(0.1)


def send_kitti():
    path = "data/kitti/05/image"
    img = cv2.imread(path + "_0/000000.png", cv2.IMREAD_GRAYSCALE)
    height = img.shape[0]
    # conncat images for stereo
    width = img.shape[1] * 2
    if len(img.shape) == 2:
        channels = 1
    else:
        channels = img.shape[2]

    print(f"width: {width}, height: {height}, channels: {channels}")

    data_type = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(len(img.tobytes() * 2).to_bytes(4, byteorder="big"))
        s.sendall(width.to_bytes(4, byteorder="big"))
        s.sendall(height.to_bytes(4, byteorder="big"))
        s.sendall(channels.to_bytes(4, byteorder="big"))
        s.sendall(data_type.to_bytes(1, byteorder="big"))  # padding

        for i in range(0, 2761):
            img1 = cv2.imread(
                path + "_0/" + str(i).zfill(6) + ".png", cv2.IMREAD_GRAYSCALE
            )
            img2 = cv2.imread(
                path + "_1/" + str(i).zfill(6) + ".png", cv2.IMREAD_GRAYSCALE
            )

            # conncat images for stereo
            stereo_img = np.concatenate((img1, img2), axis=1)
            s.sendall(stereo_img.tobytes())


if __name__ == "__main__":
    if sys.argv[1] == "test":
        sample_test_images()
    else:
        send_kitti()
