import os
import csv
import sys
import requests
import random
import shutil


def load_dataset_csv(path):
    rows = []
    with open(path, 'rb') as csvfile:
        rows = list(csv.reader(csvfile, delimiter=','))
    return rows


def fetch_data(rows):
    images = []

    for row in rows:
        image_name = row[0].split("/")[-1]
        image_path = "images/{}".format(image_name)
        images.append(image_name)

        # only fetch if the image does not exist
        if not os.path.isfile(image_path):
            print "fetching {}".format(image_name)
            image_data = requests.get(row[0])

            with open(image_path, 'wb') as f:
                f.write(image_data.content)
        else:
            print "already exists {}".format(image_name)

    return images


def categorize_and_split_dataset(rows):
    """
    Accepts rows from dataset csv

    Returns the dataset grouped by label and left/right
    """
    left_dataset = {}
    right_dataset = {}

    for row in rows:
        image_url, left_label, right_label = row
        image_name = image_url.split("/")[-1]

        if left_label not in left_dataset:
            left_dataset[left_label] = []
        if right_label not in right_dataset:
            right_dataset[right_label] = []

        left_dataset[left_label].append(image_name)
        right_dataset[right_label].append(image_name)

    return left_dataset, right_dataset


def link_images_to_dataset(side, dataset):
    for label, images in dataset.items():
        # Shuffle the dataset
        # random.shuffle(images)

        # Split the dataset into testing and training
        # Training data is 75%, testing data is 25%
        three_quarters = 3 * len(images) / 4

        training_images = images[0:three_quarters]
        testing_images = images[three_quarters:]

        for image_name in training_images:
            image_path = "training_data/{}_{}/{}".format(side, label, image_name)
            if not os.path.isfile(image_path):
                print "Linking {}".format(image_path)
                shutil.copyfile("images/{}".format(image_name), image_path)

        for image_name in testing_images:
            image_path = "testing_data/{}_{}/{}".format(side, label, image_name)
            if not os.path.isfile(image_path):
                print "Linking {}".format(image_path)
                shutil.copyfile("images/{}".format(image_name), image_path)


def create_directories(root=None):
    if not root:
        # If root is not given then use the current dir
        root = os.getcwd()

    if not os.path.exists("{}/images".format(root)):
        os.makedirs("{}/images".format(root))

    for dataset in ['training_data', 'testing_data']:
        for label in ['unknown', 'empty', 'little', 'plenty']:
            l = "{}/{}/left_{}".format(root, dataset, label)
            r = "{}/{}/right_{}".format(root, dataset, label)
            if not os.path.exists(l):
                os.makedirs(l)
            if not os.path.exists(r):
                os.makedirs(r)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "usage fetch_data.py <dataset.csv>"
        sys.exit()
    print "making directories"
    create_directories()
    print "loading dataset.csv"
    rows = load_dataset_csv(sys.argv[1])
    print "fetching data"
    fetch_data(rows)
    print "categorizing datasets"
    left_dataset, right_dataset = categorize_and_split_dataset(rows)
    print "linking left dataset"
    link_images_to_dataset('left', left_dataset)
    print "linking right dataset"
    link_images_to_dataset('right', right_dataset)
