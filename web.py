from sklearn.externals import joblib
from coffeebrain import image
from coffeebrain import constants
from flask import Flask, request, jsonify, abort
import requests

app = Flask(__name__)

print "loading classifiers"
left_classifier = joblib.load("classifiers/left.gz")
right_classifier = joblib.load("classifiers/right.gz")

DOWNSIZED_IMAGE_SIZE = (100, 100)


@app.route("/predict", methods=['POST'], strict_slashes=False)
def predict():
    if not request.json or 'image_url' not in request.json:
        abort(400)

    # Download the image
    image_request = requests.get(request.json['image_url'])

    # Extract features from the image for both sides
    left_features, right_features = image.process_image(image_data=image_request.content)

    # since we have only one feature vector (the image that was given) we can safely pick that value
    left_pot_prediction = left_classifier.predict([left_features])[0]
    right_pot_prediction = right_classifier.predict([right_features])[0]

    return jsonify({
        "left_pot": constants.REVERSE_LABELS[left_pot_prediction],
        "right_pot": constants.REVERSE_LABELS[right_pot_prediction]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0')
