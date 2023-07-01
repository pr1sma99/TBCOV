from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType
from pyspark.sql.functions import col

conf = SparkConf().setAppName('Twitter').setMaster('local')
sc = SparkContext(conf=conf)
spark = SparkSession(sc)

schema = StructType([
    StructField("tweet_id", IntegerType(), True),
    StructField("date_time", DateType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("retweeted_id", IntegerType(), True),
    StructField("quoted_id", IntegerType(), True),
    StructField("in_reply_to_id", IntegerType(), True),
    StructField("salary", IntegerType(), True)
])

df_covid = spark.read.format("csv") \
    .option("sep", "\t") \
    .option("header", True) \
    .load("united_kingdom_01.tsv")

# %%

cols = ['tweet_id', 'date_time', 'user_id', 'retweeted_id', 'quoted_id', 'in_reply_to_id']
df = df_covid.select(cols).withColumn("date_time", df_covid.date_time.cast(DateType()))

df.show(10)
df.printSchema()

# %%
df.alias("df1").join(df.alias("df2"), col("df1.retweeted_id") == col("df2.tweet_id"),"inner") \
   .show(truncate=False)
