from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType, DoubleType

from iot_producer.config import configuration


def main():
    spark = SparkSession.builder.appName("SmartCityStreaming") \
        .config("spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
                "org.apache.hadoop:hadoop-aws:3.3.1,"
                "com.amazonaws:aws-java-sdk:1.11.469") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.access.key", configuration.get('AWS_ACCESS_KEY')) \
        .config("spark.hadoop.fs.s3a.secret.key", configuration.get('AWS_SECRET_KEY')) \
        .config('spark.hadoop.fs.s3a.aws.credentials.provider',
                'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider') \
        .getOrCreate()

    # Adjust the log level to minimize the console output on executors
    spark.sparkContext.setLogLevel('WARN')

    # vehicle schema
    vehicleSchema = StructType([
        StructField("id", StringType(), True),
        StructField("vehicle_id", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("location", StringType(), True),
        StructField("speed", DoubleType(), True),
        StructField("direction", StringType(), True),
        StructField("make", StringType(), True),
        StructField("model", StringType(), True),
        StructField("year", IntegerType(), True),
        StructField("fuelType", StringType(), True),
    ])

    # gps schema
    gpsSchema = StructType([
        StructField("id", StringType(), True),
        StructField("vehicle_id", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("speed", DoubleType(), True),
        StructField("direction", StringType(), True),
        StructField("vehicleType", StringType(), True)
    ])

    # traffic schema
    trafficSchema = StructType([
        StructField("id", StringType(), True),
        StructField("vehicle_id", StringType(), True),
        StructField("camera_id", StringType(), True),
        StructField("location", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("snapshot", StringType(), True)
    ])

    # weather schema
    weatherSchema = StructType([
        StructField("id", StringType(), True),
        StructField("vehicle_id", StringType(), True),
        StructField("location", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("temperature", DoubleType(), True),
        StructField("weatherCondition", StringType(), True),
        StructField("precipitation", DoubleType(), True),
        StructField("windSpeed", DoubleType(), True),
        StructField("humidity", IntegerType(), True),
        StructField("airQualityIndex", DoubleType(), True),
    ])

    # emergency schema
    emergencySchema = StructType([
        StructField("id", StringType(), True),
        StructField("vehicle_id", StringType(), True),
        StructField("incidentId", StringType(), True),
        StructField("type", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("location", StringType(), True),
        StructField("status", StringType(), True),
        StructField("description", StringType(), True),
    ])

    def read_kafka_topic(topic, schema):
        return (spark.readStream
                .format('kafka')
                .option('kafka.bootstrap.servers', 'broker:29092')
                .option('subscribe', topic)
                .option('startingOffsets', 'earliest')
                .load()
                .selectExpr('CAST(value AS STRING)')
                .select(from_json(col('value'), schema).alias('data'))
                .select('data.*')
                .withWatermark('timestamp', '2 minutes')
                )

    def streamWriter(input_df: DataFrame, checkpoint_folder: str, output_path: str):
        return (input_df.writeStream
                .format('parquet')
                .option('checkpointLocation', checkpoint_folder)
                .option('path', output_path)
                .outputMode('append')
                .start())

    # Read from Kafka
    vehicleDF = read_kafka_topic('vehicle_data', vehicleSchema)
    gpsDF = read_kafka_topic('gps_data', gpsSchema)
    trafficDF = read_kafka_topic('traffic_data', trafficSchema)
    weatherDF = read_kafka_topic('weather_data', weatherSchema)
    emergencyDF = read_kafka_topic('emergency_data', emergencySchema)

    # Write to S3 (Parquet)
    query1 = streamWriter(
        vehicleDF,
        's3a://spark-streaming-data-atharv/checkpoints/vehicle_data',
        's3a://spark-streaming-data-atharv/data/vehicle_data'
    )
    query2 = streamWriter(
        gpsDF,
        's3a://spark-streaming-data-atharv/checkpoints/gps_data',
        's3a://spark-streaming-data-atharv/data/gps_data'
    )
    query3 = streamWriter(
        trafficDF,
        's3a://spark-streaming-data-atharv/checkpoints/traffic_data',
        's3a://spark-streaming-data-atharv/data/traffic_data'
    )
    query4 = streamWriter(
        weatherDF,
        's3a://spark-streaming-data-atharv/checkpoints/weather_data',
        's3a://spark-streaming-data-atharv/data/weather_data'
    )
    query5 = streamWriter(
        emergencyDF,
        's3a://spark-streaming-data-atharv/checkpoints/emergency_data',
        's3a://spark-streaming-data-atharv/data/emergency_data'
    )

    # Keep Spark streaming running
    query5.awaitTermination()


if __name__ == "__main__":
    main()




