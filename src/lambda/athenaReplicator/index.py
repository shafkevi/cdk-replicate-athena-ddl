import os
import boto3

# TODO: Datasources/databases/workgroups must also be sync'd
# TODO: If partitions change, they should be replicated here too.

def handler(event, context):

    print(event)
    region = os.getenv("REGION")
    raw_regions = os.getenv("REGIONS")
    if raw_regions:
        regions = raw_regions.split(",")
    else:
        return {"message": "No regions to replicate to", "success": True}


    query_execution_id = event.get("detail").get("queryExecutionId")
    work_group = event.get("detail").get("workGroupName")

    primary_athena_client = boto3.client('athena', region_name=region)
    query_execution = primary_athena_client.get_query_execution(
        QueryExecutionId=query_execution_id
    )
    print("Original Query Execution:")
    print(query_execution)
    query = query_execution.get("QueryExecution").get("Query")
    query_execution_context = query_execution.get("QueryExecution").get("QueryExecutionContext")

    for r in regions:
        print("Replicating in Region",r)
        regional_query = query.replace(region, r)
        print("Regional Query",regional_query)
        regional_athena_client = boto3.client('athena', region_name=r)
        regional_ddl = regional_athena_client.start_query_execution(
            QueryString=regional_query,
            WorkGroup=work_group,
            QueryExecutionContext=query_execution_context
        )
        print("Regional DDL Response")
        print(regional_ddl)

    return {"message": "DDL Executed in {}".format(raw_regions), "success": True}