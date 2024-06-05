import socket
import threading
import time
from dataclasses import dataclass
from queue import Queue

import cv2
import numpy as np


@dataclass
class ImageInfo:
    size: int
    width: int
    height: int
    channels: int


@dataclass
class Image:
    width: int
    height: int
    channels: int
    data_type: np.dtype
    data: bytearray


class ImageFromFiles:
    def __init__(self, path: str, queue):
        self.queue = queue

    def start(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            print("Connected to server")
            # keep the tcp listener up if the client diesconnects
            size = 128
            # all_data = []
            received_data = 0
            while True:
                data = s.recv(size)
                received_data += len(data)
                print(received_data)
                # all_data.append(data)
                # if received_data == 244 * 324 * 2:
                #     print("received image")
                #     image = np.frombuffer(b"".join(all_data), dtype=np.uint8)
                #     image = np.reshape(image, (244, 324, 2))
                #     image = np.hstack((image[:, :, 0], image[:, :, 1]))
                #     self.queue.put(image)
                #     all_data = []
                #     received_data = 0

                # if data:
                #     image = np.frombuffer(data, dtype=np.uint8)
                #     image = np.reshape(image, (244, 324, 2))
                #     image = np.hstack((image[:, :, 0], image[:, :, 1]))
                #     self.queue.put(image)
