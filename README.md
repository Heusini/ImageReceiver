## Image Receiver with Opencv over TCP

Receive images with static size. First 17 bytes define the images that are beeing sent.

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