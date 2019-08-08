"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 08-08-2018
"""
from pyspark.sql import SparkSession


def print_instructions():

    instructions = """
    # Instructions for databricks remote configuration in Azure
    
        ## Find the configuration of your cluster
        DATABRICKS_ADDRESS=https://[region].azuredatabricks.net
        DATABRICKS_API_TOKEN=[user-token]
        DATABRICKS_CLUSTER_ID=####-######-########
        DATABRICKS_ORG_ID=################
        DATABRICKS_PORT=15001
        
        ## Uninstall your pyspark version if you have it
        pip uninstall pyspark
        
        ## Install databricks version
        pip install -U databricks-connect==5.1.*  # or 5.2.*, etc. to match your cluster version
        
        ## Configure your environment running
        databricks-connect configure
    """

    print(instructions)


def get_dbutils(spark):
    try:
        from pyspark.dbutils import DBUtils
        dbutils = DBUtils(spark)
    except ImportError:
        import IPython
        dbutils = IPython.get_ipython().user_ns["dbutils"]
    return dbutils


def get_spark():
    return SparkSession.builder.getOrCreate()


def get_databricks():
    spark = get_spark()
    dbutils = get_dbutils(spark)

    spark.sparkContext.setLogLevel("ERROR")

    return spark, dbutils


if __name__ == "__main__":
    print('Welcome to the project [pymake] created by [nenetto@gmail.com]')
    print_instructions()