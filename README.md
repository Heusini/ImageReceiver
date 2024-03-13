## Image Receiver with Opencv over TCP

Receive images with static size. First 17 bytes define the images that are beeing sent.
- First 4 bytes: define the size in bytes of the images
- Second 4 bytes: define width
- Third 4 bytes: define height
- Fourth 4 bytes: define channels
- Last 1 byte: type of the image values (0 = uint8, 1=uint16, 2=float32, 3=float64)

### Use
```sh
conda env install --file conda_env.yml
conda activate wifi_receiver

python wifi_receiver.py
```

### Test
```sh
# testing
python wifi_sender.py
```