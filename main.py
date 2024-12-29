import boto3
import pymysql
import os

def read_from_s3(bucket_name, file_key):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    return response['Body'].read().decode('utf-8')

def push_to_rds(data, db_endpoint, db_user, db_password, db_name):
    try:
        connection = pymysql.connect(host=db_endpoint,
                                     user=db_user,
                                     password=db_password,
                                     database=db_name)
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS data_table (id INT AUTO_INCREMENT PRIMARY KEY, data TEXT NOT NULL)")
            cursor.execute("INSERT INTO data_table (data) VALUES (%s)", (data,))
            connection.commit()
    finally:
        connection.close()

def push_to_glue(data, glue_database, glue_table):
    glue = boto3.client('glue')
    # Assuming you have a crawler setup to read data from S3 into Glue Database
    glue.put_data(data, DatabaseName=glue_database, TableName=glue_table)

def main():
    bucket_name = os.environ['S3_BUCKET']
    file_key = os.environ['S3_KEY']
    db_endpoint = os.environ['RDS_ENDPOINT']
    db_user = os.environ['RDS_USER']
    db_password = os.environ['RDS_PASSWORD']
    db_name = os.environ['RDS_DB']
    glue_database = os.environ['GLUE_DATABASE']
    glue_table = os.environ['GLUE_TABLE']

    data = read_from_s3(bucket_name, file_key)

    try:
        push_to_rds(data, db_endpoint, db_user, db_password, db_name)
    except Exception as e:
        print(f"Failed to push to RDS: {e}")
        push_to_glue(data, glue_database, glue_table)

if __name__ == "__main__":
    main()

