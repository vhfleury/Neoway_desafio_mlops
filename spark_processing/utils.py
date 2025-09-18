def open_csv(spark, file_path):
    return spark.read.csv(file_path, header=True, inferSchema=True)
