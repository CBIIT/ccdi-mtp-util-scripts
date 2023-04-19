import ftplib
# Step3's output, updated OT's checksum
OT_UPDATED_CHECKSUM_ADDR = "/Users/wangx51/Documents/OpenTargetFile/etl_json/updated_release_data_integrity.sha1"
# step2's output, downloaded files' checksum
DOWNLOAD_FILE_CHECKSUM_ADDR = "/Users/wangx51/Documents/OpenTargetFile/etl_json/openssldownloaded.sha1"
FTP_HOST = "ftp.ebi.ac.uk"
FTP_USER = "anonymous"
FTP_PASS = "anonymous@domain.com"
# connect to the FTP server
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)

def downloadMissingFile(input):
# force UTF-8 encoding
    subdirect = input.split("/")[0]
    filename = input.split("/")[1]
#ftp.encoding = "utf-8"
    ftpPath ="/pub/databases/opentargets/platform/latest/output/etl/json/"+subdirect+"/"
    ftp.cwd(ftpPath)
    downloadPath = "/Users/wangx51/Documents/OpenTargetFile/etl_json/"+input
    with open(downloadPath, "wb") as file:
        ftp.retrbinary(f"RETR {filename}", file.write)

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
                downloadMissingFile(key)
        else:
                miss_err_count += 1
                print("[ERROR] File", key, "Not present")
                #downloadMissingFile(key)
                
                
print (diff_err_count , " of file(s) different with OT" )
print (miss_err_count , " of file(s) missing from OT" )

download_checksum_file.close() 
ot_checksum_file.close() 

ftp.quit()

