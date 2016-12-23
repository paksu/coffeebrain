from coffeebrain import image
from coffeebrain import constants
import os


def load_labeled_dataset_from_disk(side, dataset_path, label):
    """
    Load a labled dataset for one side
    args:
    - side: Which side? Accepts 'right' or 'left'
    - dataset_path: Path of the dataset directory
    - label: What label are we loading. Accepts 'unknown', 'empty', 'little', 'plenty', 'full'
    """

    assert side in constants.SIDES
    assert label in constants.LABELS.keys()

    features = []
    # Loop through each image and load them as feature
    for image_file in os.listdir('%s/%s_%s' % (dataset_path, side, label)):
        # build image path
        image_path = '%s/%s_%s/%s' % (dataset_path, side, label, image_file)
        # Extract image features from the given path
        left_features, right_features = image.process_image(image_path=image_path)

        # depending which side we are looking for then only save those features
        features.append(left_features) if side == 'left' else features.append(right_features)

    # Returns label and feature matrices
    return [constants.LABELS[label]] * len(features), features


def load_dataset_from_disk(side, dataset_type):
    """
    Load a full labeled dataset

    Returns a tuple of (labels, features)
    """
    assert side in constants.SIDES
    assert dataset_type in constants.DATASETS

    labels = []
    features = []

    # Loop through all the the possible labels and load the features for those
    for label in constants.LABELS.keys():
        dataset_labels, dataset_features = load_labeled_dataset_from_disk(side, '%s_data' % dataset_type, label)
        # Append the labeled data to the current dataset
        labels = labels + dataset_labels
        features = features + dataset_features

    return labels, features
