import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum, count as spark_count, col, lit
import connections.cache as cache
from spark_processing import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def city_features(df):
    agg_df = df.groupBy("cidade").agg(
        spark_sum("capital_social").alias("capital_social_total"),
        spark_count("*").alias("quantidade_empresas")
    )

    agg_df = agg_df.withColumn(
        "capital_social_medio",
        col("capital_social_total") / col("quantidade_empresas")
    )

    logger.info(f"total cities calculated: {agg_df.count()}")
    return agg_df


def save_features_to_redis(features_df):
    client = cache.get_client()
    for row in features_df.collect():
        cidade = row["cidade"]
        mapping = {
            "capital_social_total": float(row["capital_social_total"]),
            "quantidade_empresas": int(row["quantidade_empresas"]),
            "capital_social_medio": float(row["capital_social_medio"])
        }

        cache.save_hset(client, cidade, mapping)
        logger.info(f"'{cidade}' - saved successfully: {mapping}")
    logger.info("Data successfully saved to Redis")


def write_parquet(df, output_dir, run_date: str):
    (
        df.withColumn("run_date", lit(run_date))
          .write
          .mode("overwrite")
          .partitionBy("run_date")
          .option("compression", "snappy")
          .parquet(output_dir)
    )
    logger.info("Data successfully saved to Parquet")


def run_feature(input_path: str, output_dir: str, run_date: str):
    try:
        spark = SparkSession.builder.master("local[*]").appName("FeaturePipeline").getOrCreate()
        logger.info(f"open csv on path {input_path} ...")
        df = utils.open_csv(spark, input_path)

        logger.info("Calculating aggregated features by city...")
        df_features = city_features(df)

        logger.info("save features on Redis ...")
        save_features_to_redis(df_features)

        logger.info("save features parquet ...")
        write_parquet(df_features, output_dir, run_date)

        spark.stop()

        logger.info("Pipeline de feature engineering concluído com sucesso.")
    except Exception as e:
        logger.error(f"Error in feature engineering: {e}", exc_info=True)
        raise
