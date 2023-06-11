from potassium import Potassium, Request, Response

from transformers import pipeline
import torch
import cv2
import base64
import logging

app = Potassium("my_app")

# @app.init runs at startup, and loads models into the app's context
@app.init
def init():
    # device = 0 if torch.cuda.is_available() else -1
    # model = pipeline('fill-mask', model='bert-base-uncased', device=device)
   
    context = {
        # "model": model
    }

    return context

# @app.handler runs for every call
@app.handler()
def handler(context: dict, request: Request) -> Response:
    logging.info('handler')

    # prompt = request.json.get("prompt")
    # model = context.get("model")
    # outputs = model(prompt)

    image_data = request.get('image_data', None)
    image = Image.open(BytesIO(base64.b64decode(image_data))).convert("RGB") 

    logging.info('subprocess.run')
    subprocess.run("./upscayl-realesrgan -i output-0.png -o output.jpeg -s 2 -m models -n ultramix_balanced -f jpeg")
    logging.info('subprocess.run done')

    img = cv2.imread('output.jpeg')
    jpg_img = cv2.imencode('.jpeg', img)
    b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')

    return Response(
        json = {"base64": b64_string}, 
        status=200
    )

if __name__ == "__main__":
    app.serve()