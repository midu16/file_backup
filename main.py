"""
This is the file_backup main.
The purpose of this is to backup the CallDetailRecord files to a remote site.
"""
__author__ = 'Mihai IDU'
__version__ = '0.0.1'

# importing the python libraries for further Use
import argparse
from datetime import datetime
from pathlib import Path
import zipfile
import os
from os import listdir
from os.path import isfile, join
import pysftp
import time


def SendBackup(remote_backup_directory_path, localhost_object_to_backup_path, server, username):
    srv = pysftp.Connection(host=server, username=username,log=".pysftp.log")
    with srv.cd(remote_backup_directory_path):
        x = [os.path.abspath(os.path.join(localhost_object_to_backup_path, p)) for p in os.listdir(localhost_object_to_backup_path) if p.endswith(('zip'))]
        for index in x:
            print(index)
            srv.put(index)
    # Closes the connection
    srv.close()


def ManagementBackup(object_to_backup_path, backup_directory_path, max_amount_backup):
    # Validate the backup directory exists and create if required
    backup_directory_path.mkdir(parents=True, exist_ok=True)
    # Get the amount of past backup zips in the backup directory already
    existing_backups = [
        x for x in backup_directory_path.iterdir()
        if x.is_file() and x.suffix == '.zip' and x.name.startswith('backup-')
    ]

    # Enforce max backups and delete oldest if there will be too many after the new backup
    oldest_to_newest_backup_by_name = list(sorted(existing_backups, key=lambda f: f.name))
    while len(oldest_to_newest_backup_by_name) >= max_amount_backup:  # >= because we will have another soon
        backup_to_delete = oldest_to_newest_backup_by_name.pop(0)
        backup_to_delete.unlink()

    # Create zip file (for both file and folder options)
    backup_file_name = f'backup-{datetime.now().strftime("%Y%m%d%H%M%S")}-{object_to_backup_path.name}.zip'
    zip_file = zipfile.ZipFile(str(backup_directory_path / backup_file_name), mode='w')
    if object_to_backup_path.is_file():
        # If the object to write is a file, write the file
        zip_file.write(
            object_to_backup_path.absolute(),
            arcname=object_to_backup_path.name,
            compress_type=zipfile.ZIP_DEFLATED
        )
    elif object_to_backup_path.is_dir():
        # If the object to write is a directory, write all the files
        for file in object_to_backup_path.glob('**/*'):
            if file.is_file():
                zip_file.write(
                    file.absolute(),
                    arcname=str(file.relative_to(object_to_backup_path)),
                    compress_type=zipfile.ZIP_DEFLATED
                )
    # Close the created zip file
    zip_file.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    global USERNAME
    global HOSTNAME
    global BACKUP_DIRECTORY
    global OBJECT_TO_BACKUP
    global MAX_BACKUP_AMOUNT
    global LOCALHOST_OBJECT_TO_BACKUP_PATH
    global REMOTE_BACKUP_DIRECTORY_PATH

    parser = argparse.ArgumentParser(description="Process designated for Backup PCP-CDR 2021!")
    parser.add_argument("-sp", "--source-path", type=str, help="Mention the source path of the file or directory which needs to be backup")
    parser.add_argument("-dp","--destination-path", type=str, help="Mention the destination path of the backup")
    parser.add_argument("-lobp","--localhost-object-to-backup-path", type=str, help="Mention the localhost object to be remote backup")
    parser.add_argument("-rbdp","--remote-backup-directory-path", type=str, help="Mention the remote backup directory on the remote host")
    parser.add_argument("-u","--username", type=str, help="Remote connection username of the backup source host")
    parser.add_argument("-hs","--hostname", type=str, help="Backup endpoint hostname")
    parser.add_argument("-mab","--max-amount-backup", type=int, help="maximum amount of backups to be kept", default=180)
    args = parser.parse_args()
    OBJECT_TO_BACKUP = args.source_path
    BACKUP_DIRECTORY = args.destination_path
    USERNAME = args.username
    HOSTNAME = args.hostname
    MAX_BACKUP_AMOUNT = args.max_amount_backup
    LOCALHOST_OBJECT_TO_BACKUP_PATH = args.localhost_object_to_backup_path
    REMOTE_BACKUP_DIRECTORY_PATH = args.remote_backup_directory_path
    max_amount_backup = 2
    object_to_backup_path = Path(OBJECT_TO_BACKUP)
    backup_directory_path = Path(BACKUP_DIRECTORY)
    assert object_to_backup_path.exists()
    ManagementBackup(object_to_backup_path, backup_directory_path, max_amount_backup)
    time.sleep(5)
    SendBackup(REMOTE_BACKUP_DIRECTORY_PATH,LOCALHOST_OBJECT_TO_BACKUP_PATH,HOSTNAME,USERNAME)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
