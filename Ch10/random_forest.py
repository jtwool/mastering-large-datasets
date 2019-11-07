from pyspark import SparkContext
from pyspark.sql import SparkSession
from functools import reduce
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

def string_to_index(df, label):
     return StringIndexer(inputCol=label,
                          outputCol="i-"+label).fit(df) \
                                               .transform(df)

if __name__ == "__main__":

    spark = SparkSession.builder \
               .master("local") \
               .appName("Random Forests") \
               .getOrCreate()

    bce = BinaryClassificationEvaluator()

    forest = RandomForestClassifier()
    df = spark.read.csv("mushrooms.data", header=True, inferSchema=True)

    categories = df.columns
    categories.pop(categories.index('edible?'))
    df = reduce(string_to_index, categories, df)
    indexes = ["i-"+c for c in categories]
    df = VectorAssembler(inputCols=indexes,
                         outputCol="features").transform(df)
    df = StringIndexer(inputCol='edible?',
                       outputCol='label').fit(df).transform(df)

    grid = ParamGridBuilder().addGrid(forest.maxDepth, [0, 2]).build()
    cv = CrossValidator(estimator=forest, estimatorParamMaps=grid,
                            evaluator=bce,numFolds=10,
                            parallelism=4)
    cv_model = cv.fit(df)
    area_under_curve = bce.evaluate(cv_model.transform(df))
    print("Random Forest AUC: {:0.4f}".format(area_under_curve))
    print(cv_model.bestModel.toDebugString)
