import json
import boto3 as aws
from functools import reduce
from pyspark import SparkContext
from pyspark.sql import SparkSession
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

def read_s3_object(x):
    s3 = aws.resource("s3")
    obj = s3.Object(x[0], x[1])
    return obj.get()['Body'].read().decode('ascii')


if __name__ == "__main__":
    sc = SparkContext(appName="Crash model")
    spark = SparkSession.builder \
                      .master("local") \
                      .getOrCreate()

    s3 = aws.resource("s3")

    bucket = s3.Bucket("s3://path/to/your/bucket")
    objects = [(obj.bucket_name, obj.key) for obj
                                          in bucket.objects.all()]
    xs = sc.parallelize(objects) \
           .map(read_s3_object) \
           .flatMap(lambda x:x.split("\n")) \
           .filter(lambda x:x) \
           .map(json.loads) \
           .map(group_crashes) \
           .map(improve_times)

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


    mce = MulticlassClassificationEvaluator()
    nb = NaiveBayes()
    cv = CrossValidator(estimator=nb, estimatorParamMaps=grid,
                      evaluator=mce,numFolds=5,
                      parallelism=4)
    cv_model = cv.fit(df)
    transformed = cv_model.transform(df)
    f1 = mce.evaluate(transformed)
    print("NB F1: {:0.4f}".format(f1))
    cv_model.bestModel.save("s3://path/to/your/bucket")
