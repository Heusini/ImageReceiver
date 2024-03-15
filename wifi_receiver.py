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


class ImageReceiver:
    def __init__(self, host, port, queue):
        self.host = host
        self.port = port
        self.queue = queue

    def accecpt_client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            connection, addr = s.accept()
            print("Connected by", addr)
            return connection


    def start(self):
        while True:
            print("Starting server...")
            print("Waiting for connection...")
            self.con = self.accecpt_client()
            print("Client connected")
            image_size = self.receive_bytes(4)
            image_width = self.receive_bytes(4)
            image_height = self.receive_bytes(4)
            image_channels = self.receive_bytes(4)
            image_datatype = int.from_bytes(self.receive_bytes(1), byteorder="big")
            print("Received image info...")

            data_type = np.uint8
            match image_datatype:
                case 0:
                    data_type = np.uint8
                case 1:
                    data_type = np.uint16
                case 2:
                    data_type = np.float32
                case 3:
                    data_type = np.float64
                case _:
                    data_type = np.uint8

            img_info = ImageInfo(
                size=int.from_bytes(image_size, byteorder="big"),
                width=int.from_bytes(image_width, byteorder="big"),
                height=int.from_bytes(image_height, byteorder="big"),
                channels=int.from_bytes(image_channels, byteorder="big"),
            )

            while True:
                data = self.receive_bytes(img_info.size)
                if not data:
                    print("Connection closed")
                    break
                img = Image(
                    width=img_info.width,
                    height=img_info.height,
                    channels=img_info.channels,
                    data_type=np.dtype(data_type),
                    data=data,
                )
                self.queue.put(img)


    def receive_bytes(self, len_bytes):
        data = bytearray()
        while len(data) < len_bytes:
            net_data = self.con.recv(len_bytes - len(data))
            if not net_data:
                return net_data
            data.extend(net_data)
        return data


def display_img(img_queue):
    last_tick = time.time()
    while True:
        try:
            img_bytes = img_queue.get(False)
            print(f"Len received data: {len(img_bytes.data)}")
            bayer_im = np.frombuffer(img_bytes.data, dtype=img_bytes.data_type)
            bayer_im = bayer_im.reshape(
                (img_bytes.height, img_bytes.width, img_bytes.channels)
            )

            frame_period = time.time() - last_tick
            last_tick = time.time()
            frame_rate = 1 / frame_period

            cv2.putText(img=bayer_im, text="{:10.2f}fps".format(frame_rate), org=(20, 30),
                                            fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                                            fontScale=1, color=(255, 0, 0), thickness=1)

            bgr = cv2.cvtColor(bayer_im, cv2.IMREAD_COLOR)
            cv2.imshow("image", bgr)
            cv2.waitKey(1)


        except:
            # print("No new image")
            cv2.waitKey(1)


if __name__ == "__main__":
    image_queue = Queue(maxsize=0)
    host = "127.0.0.1"  # Standard loopback interface address (localhost)
    port = 3333

    img_receiver = ImageReceiver(host, port, image_queue)

    receive_thread = threading.Thread(
        target=img_receiver.start,
    )

    display_thread = threading.Thread(
        target=display_img,
        args=(image_queue,),
    )

    receive_thread.start()
    display_thread.start()
