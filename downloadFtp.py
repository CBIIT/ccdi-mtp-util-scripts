import ftplib
import io
import os
FTP_HOST = "ftp.ebi.ac.uk"
FTP_USER = "anonymous"
FTP_PASS = "anonymous@domain.com"
# connect to the FTP server
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
# force UTF-8 encoding


subdirect = input.split("/")[0]
filename = input.split("/")[1]
#ftp.encoding = "utf-8"
ftpPath ="/pub/databases/opentargets/platform/latest/output/etl/json/diseases/"+subdirect+"/"
ftp.cwd(ftpPath)
print(ftp.pwd())

downloadPath = "/Users/wangx51/Documents/OpenTargetFile/etl_json/"+input

#file= open(downloadPath)
print(ftp.dir())
with open(downloadPath, "wb") as file:
    # Command for Downloading the file "RETR filename"
    ftp.retrbinary(f"RETR {filename}", file.write)
 
# Read file in binary mode


