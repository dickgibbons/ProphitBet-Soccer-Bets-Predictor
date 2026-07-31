from src.models.classifiers.decisiontree import DecisionTree
from src.models.classifiers.discriminant import DiscriminantAnalysisClassifier
from src.models.classifiers.extremeboosting import XGBoost
from src.models.classifiers.knn import KNN
from src.models.classifiers.logistic import LogisticRegressor
from src.models.classifiers.naivebayes import NaiveBayes
from src.models.classifiers.randomforest import RandomForest
from src.models.classifiers.svm import SVM

# TensorFlow DNN is optional (desktop full install only; web MVP omits TF).
try:
    from src.models.classifiers.neuralnets.nn import NeuralNetwork
except ImportError:  # pragma: no cover
    NeuralNetwork = None  # type: ignore
