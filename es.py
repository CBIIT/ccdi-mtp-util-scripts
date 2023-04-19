from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from opensearchpy.helpers import bulk
import boto3
import json
host = 'https://vpc-mtp-opensearch-dev-akmgxd5o76x3at6t7conzlciam.us-east-1.es.amazonaws.com' # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-1' # e.g. us-west-1
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region)
index_name = 'movies'
client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = False,
    connection_class = RequestsHttpConnection
)
print(client.info())
import os
 
# Get the list of all files and directories
path = "/Users/wangx51/Documents/ot_2211/rmtl_output/target"
dir_list = os.listdir(path)
 
print("Files and directories in '", path, "' :")
 
# prints all files
for item in dir_list:
  file1=open(path+"/"+item)
  Lines = file1.readlines()
  for line in Lines:
    jsonfile = json.loads(line)
    #response=client.index(body=jsonfile,index="target")
    #print(response)
