import json
import sys
from pyspark import SparkContext
from pyspark.sql import SparkSession
from functools import reduce
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

def string_to_index(df, label):
     return StringIndexer(inputCol=label,
                          outputCol="i-"+label).fit(df) \
                                               .transform(df)

def group_crashes(x):
    if int(x['Number of Vehicles Involved']) > 3:
        x['Number of Vehicles Involved'] = "3"
    return x

def improve_times(x):
    time = x['Time']
    if time < "5:00":
        x['Time'] = "Early morning"
    elif time < "7:00":
        x['Time'] = "Morning"
    elif time < "9:00":
        x['Time'] = "Morning commute"
    elif time < "12:00":
        x['Time'] = "Late morning"
    elif time < "16:00":
        x['Time'] = "Afternoon"
    elif time < "18:30":
        x['Time'] = "Evening commute"
    elif time < "22:00":
        x['Time'] = "Evening"
    else:
        x['Time'] = "Late night"
    return x

if __name__ == "__main__":

    sc = SparkContext(appName="Crash counts")
    spark = SparkSession.builder \
               .master("local") \
               .getOrCreate()

    mce = MulticlassClassificationEvaluator()

    nb = NaiveBayes()
    # read in lines to RDD
    crashes = sc.textFile(sys.argv[1])
    xs = crashes.flatMap(lambda x:x.split('\n')) \
                .map(json.loads) \
                .map(group_crashes) \
                .map(improve_times)

    # conver to DF
    df = spark.createDataFrame(xs)

    feature_labels = df.columns
    feature_labels.pop(feature_labels.index('Number of Vehicles Involved'))
    df = reduce(string_to_index, feature_labels, df)
    indexes = ["i-"+f for f in feature_labels]

    df = VectorAssembler(inputCols=indexes,
                         outputCol="features").transform(df)

    df = StringIndexer(inputCol='Number of Vehicles Involved',
                       outputCol='label').fit(df).transform(df)

    grid = ParamGridBuilder().addGrid(nb.smoothing, [1.0, 1.5]) \
                             .build()

    cv = CrossValidator(estimator=nb, estimatorParamMaps=grid,
                            evaluator=mce,numFolds=5,
                            parallelism=4)
    cv_model = cv.fit(df)
    transformed = cv_model.transform(df)
    f1 = mce.evaluate(transformed)
    print("NB F1: {:0.4f}".format(f1))
    cv_model.bestModel.save(sys.argv[2])
