import requests
url ="https://vpc-mtp-opensearch-dev-akmgxd5o76x3at6t7conzlciam.us-east-1.es.amazonaws.com/target/_doc/_bulk?pretty"
headers ={'Content-Type':'application/json'}

import os
 
# Get the list of all files and directories
path = "/Users/wangx51/Documents/ot_2211/rmtl_output/target"
dir_list = os.listdir(path)
 
print("Files and directories in '", path, "' :")
 
# prints all files
for item in dir_list:
  file1=open(path+"/"+item)
  Lines = file1.read()
  res =requests.post(url, headers=headers, data=Lines.encode('utf-8'))
  print(res.content)