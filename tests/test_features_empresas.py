import pytest
from pyspark.sql import SparkSession
from spark_processing import features_empresas


@pytest.fixture(scope="module")
def spark():
    spark = SparkSession.builder.master("local[1]").appName("pytest-spark").getOrCreate()
    yield spark
    spark.stop()


def test_city_features(spark):
    data = [
        ("CNPJ1", "2025-07-28T09:00:00Z", "São Paulo", "SP", 50000.00),
        ("CNPJ2", "2025-07-28T10:00:00Z", "São Paulo", "SP", 100000.00),
        ("CNPJ3", "2025-07-28T11:00:00Z", "Rio de Janeiro", "RJ", 75000.00)
    ]
    columns = ["cnpj", "data_abertura", "cidade", "estado", "capital_social"]
    df = spark.createDataFrame(data, schema=columns)
    result_df = features_empresas.city_features(df)

    result = {
        row['cidade']: (
            row['capital_social_total'],
            row['quantidade_empresas'],
            round(row['capital_social_medio'], 2)
        )
        for row in result_df.collect()
    }

    assert "São Paulo" in result
    total_sp, count_sp, avg_sp = result["São Paulo"]
    assert total_sp == 150000.0
    assert count_sp == 2
    assert round(avg_sp, 2) == 75000.00

    assert "Rio de Janeiro" in result
    total_rj, count_rj, avg_rj = result["Rio de Janeiro"]
    assert total_rj == 75000.0
    assert count_rj == 1
    assert round(avg_rj, 2) == 75000.00
