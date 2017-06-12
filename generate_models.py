from sklearn.svm import SVC
from sklearn.externals import joblib
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import Pipeline
from coffeebrain import dataset
import os

if __name__ == "__main__":
    print "loading training data"
    left_training_labels, left_training_features = dataset.load_dataset_from_disk('left', 'training')
    left_testing_labels, left_testing_features = dataset.load_dataset_from_disk('left', 'testing')

    print "loading testing data"
    right_training_labels, right_training_features = dataset.load_dataset_from_disk('right', 'training')
    right_testing_labels, right_testing_features = dataset.load_dataset_from_disk('right', 'testing')

    print "training left classifier"
    search_params = {
        'kernel': ['linear'],
        'C': [100]
    }

    estimators = [
        ('normalize', Normalizer()),
        ('svm', SVC(kernel='linear', C=100, probability=True))
    ]

    left_classifier = Pipeline(estimators)
    left_classifier.fit(left_training_features, left_training_labels)

    left_accuracy = left_classifier.score(left_testing_features, left_testing_labels)
    print "left classifier accuracy is %.2f" % (left_accuracy * 100)

    print "training right classifier"
    right_classifier = Pipeline(estimators)
    right_classifier.fit(right_training_features, right_training_labels)

    right_accuracy = right_classifier.score(right_testing_features, right_testing_labels)

    print "right classifier accuracy is %.2f" % (right_accuracy * 100)

    print "saving models"

    if not os.path.exists("classifiers"):
        os.makedirs("classifiers")

    joblib.dump(left_classifier, "classifiers/left.gz", compress=('gzip', 3))
    joblib.dump(right_classifier, "classifiers/right.gz", compress=('gzip', 3))
