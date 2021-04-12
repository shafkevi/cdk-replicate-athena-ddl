import boto3

def handler(event, context):

    print(event)
    # Pick which region you want this to run in
    us_east_1_client = boto3.client('athena', region_name="us-east-1")
    # us_west_1_client = boto3.client('athena', region_name="us-west-1")

    query_execution_id = event.get("detail").get("queryExecutionId")
    query_execution = us_east_1_client.get_query_execution(
        QueryExecutionId=query_execution_id
    )
    print(query_execution)
    
    return query_execution.get("QueryExecution").get("Query")