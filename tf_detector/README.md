# Setup Instructions 

1. Follow environment setup and installations in:

https://gist.github.com/khanhlvg/bbeb5e4ccfca6cbcf18508a44f5964be

It's important to create a Python environment and `activate` it whenever we use the detector. To activate run in terminal:

```
source ~/tflite/bin/activate
```

2. See object detector usage info at [tf_INFO.md](tf_INFO.md)

# Run the OD on images

1. Place and locate images in the `/test_imgs` folder.
2. In the `main.py` file change image route in `_IMAGE_FILE` constant.
3. Run `python main.py`.

Don't forget to `activate` the Python environment.
