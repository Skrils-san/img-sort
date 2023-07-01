from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import os, shutil, ffmpeg

np.set_printoptions(suppress=True)
model = load_model("models/model.h5", compile=False)
class_names = open("models/labels.txt", "r").readlines()

APP_FOLDER = 'input'
totalFiles = 0
skipped = 0
de = 0

for base, dirs, files in os.walk(APP_FOLDER):
    for Files in files:
        totalFiles += 1

for i in range(totalFiles):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    img = os.listdir(APP_FOLDER)[0]
    
    if(img[-4:] in [".png", ".jpg", "jpeg", "webp", ".gif", ".mp4"]):

        if(img[-4:] in [".mp4"]):
            mp4 = f'{APP_FOLDER}/{img}'
            probe = ffmpeg.probe(mp4)
            time = float(probe['streams'][0]['duration']) // 1
            width = probe['streams'][0]['width']

            intervals = int(time // 2)
            interval_list = [(i * intervals, (i + 1) * intervals) for i in range(1)]
            i = 0

            for item in interval_list:
                (
                    ffmpeg
                    .input(mp4, ss=item[1])
                    .filter('scale', width, -1)
                    .output('ffmpeg-output/Image' + str(i) + '.jpg', vframes=1)
                    .run()
                )
            de = 1
            image = Image.open("ffmpeg-output/Image0.jpg").convert("RGB")

        else:
            image = Image.open(f"{APP_FOLDER}/{img}").convert("RGB")

        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data[0] = normalized_image_array
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]
        print("Class:", class_name, end="")
        print("Confidence Score:", confidence_score)

        # Expand if you have more than 2 labels
        # Change class_name[0:last char position of label]
        if (class_name[0:4] == "Cats"):
            shutil.move(f"{APP_FOLDER}/{img}", f"output/output-0/{img}")
        elif(class_name[0:4] == "Dogs"):
            shutil.move(f"{APP_FOLDER}/{img}", f"output/output-1/{img}")
        else:
            print("ERROR")
        
        if(de == 1):
            os.remove("ffmpeg-output/Image0.jpg")
            de = 0
    else:
        print("WRONG FILE FORMAT DETACTED!\nSKIPPING FILE!")
        shutil.move(f"{APP_FOLDER}/{img}", f"skipped/{img}")
        skipped += 1
        continue
    
print(f"{skipped} files skipped")