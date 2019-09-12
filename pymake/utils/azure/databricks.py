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


def parse_type(spark_type, value):

    try:
        if spark_type == 'string':
            return str(value)
        elif spark_type == 'boolean':
            return bool(value)
        elif spark_type == 'double':
            return float(value)
        elif spark_type == 'long':
            return int(value)
        else:
            return None
    except:
        return None


def return_spark_type(v):

    if isinstance(v, str):
        return 'string'
    elif isinstance(v, bool):
        return 'boolean'
    elif isinstance(v, float):
        return 'double'
    elif isinstance(v, int):
        return 'long'
    else:
        return None


def spark_schema_from_value(name, value):
    schema = None

    typeofvalue = return_spark_type(value)
    if typeofvalue is not None:
        schema = {'type': typeofvalue,
                  'name': name,
                  'nullable': True,
                  'metadata': {}
                 }
    elif isinstance(value, list):
        typeofelement = 'string' if len(value) == 0 else return_spark_type(value[0])
        schema = {"name": name,
                  "type": {"elementType": typeofelement,
                           "type": "array",
                           "containsNull": True
                           },
                  "nullable": True,
                  "metadata": {}
                  }
    elif isinstance(value, dict):
        schema = {'type': 'struct',
                  'name': name,
                  'fields': [],
                  'nullable': True,
                  'metadata': {}}

        for k, v in value.items():
            schema['fields'].append(spark_schema_from_value(k, v))

    else:
        schema = {'type': 'string',
                  'name': name,
                  'nullable': True,
                  'metadata': {'error': 'NOT_PARSED_TYPE'}
                 }

    return schema


def spark_schema_from_pydict(dict_data):

    json_schema = {'type': 'struct',
                   'fields': []}

    for name, value in dict_data.items():
        json_schema['fields'].append(spark_schema_from_value(name, value))

    return json_schema


if __name__ == "__main__":
    print('Welcome to the project [pymake] created by [nenetto@gmail.com]')
    print_instructions()