# !pip install python-multipart
# !pip install tensorflow
# !pip install fastapi
# !pip install Pillow
# python -m pip install uvicorn gunicorn

# 터미널에 입력하면 서버 켜짐
# uvicorn server:app --port 5000 --reload

import numpy as np
import io
from PIL import Image, ImageOps
from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
from tensorflow import keras
app = FastAPI()


@app.get('/')
async def root():
    return{'message': 'Hello World'}


@app.get('/test')
async def test():
    return{'message': 'test'}

# use swagger
## localhost : 5000/docs
# localhost : 5000/docs로 접속하면 postman 안하고 가능

loaded_model = keras.models.load_model('my_mnist')
print('Loaded model', loaded_model)

# 텐서플로우를 사용해서 사람들이 그린 숫자를 해석해줌 (0~9까지 젤 높은 확률인 숫자를 출력)


@app.post('/uploadfile/')
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    pil_image = Image.open(io.BytesIO(contents))
    img_gray = pil_image.convert('L')
    img_inverted = ImageOps.invert(img_gray)
    pixel_list = np.asfarray(img_inverted).flatten().tolist()
    inputs = (np.asfarray(pixel_list)/255.0*0.99)+0.01
    preds = loaded_model.predict(inputs.reshape((1, 28, 28, 1)), batch_size=1)
    return{'result_cnn': str(preds[0].argmax()), 'scores_cnn': str(preds[0].tolist())}
