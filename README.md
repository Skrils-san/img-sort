# img-sort

## Prerequisites

 - [Tensorflow]()
 - [Pillow]()
 - [Numpy]()
 - [ffmpeg-python]()
 - ... or just use `pip install -r requierments.txt`


```python
# Expand if you have more than 2 labels
# Change class_name[0:last char position of label]
if (class_name[0:4] == "Cats"):
    shutil.move(f"{APP_FOLDER}/{img}", f"output/output-0/{img}")
elif(class_name[0:4] == "Dogs"):
    shutil.move(f"{APP_FOLDER}/{img}", f"output/output-1/{img}")
```