from pyspark import SparkContext
from pyspark.sql import SparkSession
from functools import reduce
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator

def string_to_index(df, label):
     return StringIndexer(inputCol=label,
                          outputCol="i-"+label).fit(df) \
                                               .transform(df)

if __name__ == "__main__":

    spark = SparkSession.builder \
               .master("local") \
               .appName("Decision Trees") \
               .getOrCreate()

    df = spark.read.csv("mushrooms.data", header=True, inferSchema=True)

    categories = ['cap-shape', 'cap-surface', 'cap-color']
    df = reduce(string_to_index, categories, df)

    df = VectorAssembler(inputCols=["i-cap-shape","i-cap-surface", "i-cap-color"],
                         outputCol="features").transform(df)

    df = StringIndexer(inputCol='edible?', outputCol='label').fit(df).transform(df)

    tree = DecisionTreeClassifier()
    model = tree.fit(df)
    #print(model.toDebugString)

    bce = BinaryClassificationEvaluator()

    auc = bce.evaluate(model.transform(df))
    print("Decision Tree AUC: {:0.4f}".format(auc))
