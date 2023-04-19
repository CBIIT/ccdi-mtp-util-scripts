
# Step3's output, updated OT's checksum
OT_UPDATED_CHECKSUM_ADDR = "/Users/wangx51/Documents/OpenTargetFile/etl_json/updated_release_data_integrity.sha1"
# step2's output, downloaded files' checksum
DOWNLOAD_FILE_CHECKSUM_ADDR = "/Users/wangx51/Documents/OpenTargetFile/etl_json/openssldownloaded.sha1"




dic_download ={}

# create key/value pair in a dic for each check up. 
# key : file path
# value: checksum
# root:  downloaded file's checksum


download_checksum_file = open(DOWNLOAD_FILE_CHECKSUM_ADDR, 'r')
download_checksum_file_lines = download_checksum_file.readlines()


for line in download_checksum_file_lines:
    array = line.split(")= ")
    value = array[1].strip()
    key = str("/".join(array[0].split("/")[-2:]))
    #print(key)
    dic_download[key]=value

    
#comparsion the checksum

ot_checksum_file = open(OT_UPDATED_CHECKSUM_ADDR, 'r')
ot_checksum_file_lines = ot_checksum_file.readlines()

diff_err_count = 0
miss_err_count = 0
for line in ot_checksum_file_lines:
    array = line.split()
    value = array[0].strip()
    if "error" not in array[1]:
        key = str("/".join(array[1].split("/")[-2:]))
        if key in dic_download.keys():
            if dic_download[key] != value:
                diff_err_count += 1 
                print("[ERROR] File", key, "Not identical with OT")
        else:
                miss_err_count += 1
                print("[ERROR] File", key, "Not present")
                #downloadMissingFile(key)
                
                
#print (diff_err_count , " of file(s) different with OT" )
#print (miss_err_count , " of file(s) missing from OT" )

download_checksum_file.close() 
ot_checksum_file.close() 

