import boto3
import json
import base64

def lambda_handler(event, context):
    secret_name = "arn:aws:secretsmanager:us-east-1:087074250104:secret:Lambda_Secrets-dlcHIw"
    # Create a Secrets Manager client
    secretClient = boto3.client(
        service_name = 'secretsmanager',
        region_name = 'us-east-1'
    )

    get_secret_value_response = secretClient.get_secret_value(
        SecretId=secret_name
    )
    secret = get_secret_value_response['SecretString']
    Table_name = 'AWS_Highschool'
    
    print('DynamoDB Table creation started.')
    
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id = json.loads(secret).get('Access Key'),
        aws_secret_access_key = json.loads(secret).get('Secret Access Key'),
        region_name = 'us-east-1'
    )
    
    student_table = dynamodb.create_table(
        TableName = Table_name,
        KeySchema = [
            {
                'KeyType': 'HASH',
                'AttributeName': 'StudId'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'StudId',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 2,
            'WriteCapacityUnits': 2
        }
    )
    
    # Wait until the Table gets created
    student_table.meta.client.get_waiter('table_exists').wait(TableName = Table_name)
    print('DynamoDB Table Creation Completed.')
    
    print('Insert Student data to table started.')
    # Insert 1st item into DynamoDB table
    table = dynamodb.Table(Table_name)
    table.put_item(
    Item = {
            'StudId': 100,
            'FirstName': 'Johnny',
            'LastName': 'Bravo',
            'Dept': 'AP',
            'Age': 20
        }
    )
    
    # Insert 2nd item into DynamoDB table
    table.put_item(
    Item = {
            'StudId': 200,
            'FirstName': 'John',
            'LastName': 'Cena',
            'Dept': 'OPS',
            'Age': 46
        }
    )
    
    # Insert 3rd item into DynamoDB table
    table.put_item(
    Item = {
            'StudId': 300,
            'FirstName': 'Bart',
            'LastName': 'Simpson',
            'Dept': 'SA',
            'Age': 10
        }
    )
    print('Insert Student data to table Completed.')
    