import hashlib
import sqlite3
from sqlite3 import Error
import os


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
def sha256sum(filename):
    h  = hashlib.sha1()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_record(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO file2(file_name,ot_checksum,downloaded_checksum,lines, is_downloaded)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid



conn = create_connection("file.db")
ot_checksum_file = open("release_data_integrity.sha1", 'r')
ot_checksum_file_lines = ot_checksum_file.readlines()
for line in ot_checksum_file_lines:
    if "/etl/json/" in line and ".json" in line and "error" not in line:
        line = line.strip()
        array = line.split("  ./")
        sha1 = array[0].strip()
        if "sourceId=" in line or "/fda/" in line or "/parquet/" in line:
            key = str("/".join(array[1].split("/")[-3:]))
        else:
            key = str("/".join(array[1].split("/")[-2:]))
        downloadPath = "/Users/wangx51/Documents/OpenTargetFile/etl_json/"+key
        print(os.path.isfile(downloadPath))
        if os.path.isfile(downloadPath):
            num_lines = sum(1 for line in open(downloadPath))
            downloaded_sum =sha256sum(downloadPath)
            record= (key, sha1, downloaded_sum, num_lines, "true")
            create_record(conn, record)
        else:
            record= (key, sha1, None, None, "false")
            create_record(conn, record)
            #downloadMissingFile(key)



