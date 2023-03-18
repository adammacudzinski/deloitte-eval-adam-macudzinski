import json
import requests
import numpy as np
import pathlib
from PIL import Image



class FashionClassifierAPIClient:
    """
    Client module to test that the Fashion MNMT Model successfully deployed
    """
    class_names = (
        'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot'
    )

    def __init__(self, api_url: str):
        self.api_url = api_url

    def classify_image(self, numpy_encoded_image):
        data = json.dumps({"signature_name": "serving_default", "instances": [numpy_encoded_image]})

        headers = {"content-type": "application/json"}
        json_response = requests.post(self.api_url, data=data, headers=headers)
        predictions = json.loads(json_response.text)['predictions']

        return self.class_names[np.argmax(predictions[0])]


if __name__ == "__main__":
    local_api_url = 'http://localhost:8101/v1/models/fashion_model'
    fashion_client = FashionClassifierAPIClient(local_api_url)

    curr_dir = pathlib.Path(__file__).parent.resolve()
    test_img_file = pathlib.Path(curr_dir, "data/img.png")

    img = Image.open(test_img_file)
    numpydata = np.asarray(img)

    category = fashion_client.classify_image(numpydata.tolist())

    assert category == "Trouser"