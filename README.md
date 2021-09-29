# file_backup
backup files remote host

'''

$ file_backup -h 
usage: main.py [-h] [-sp SOURCE_PATH] [-dp DESTINATION_PATH] [-lobp LOCALHOST_OBJECT_TO_BACKUP_PATH] [-rbdp REMOTE_BACKUP_DIRECTORY_PATH] [-u USERNAME]
               [-hs HOSTNAME] [-mab MAX_AMOUNT_BACKUP]

Process designated for Backup PCP-CDR 2021!

optional arguments:
  -h, --help            show this help message and exit
  -sp SOURCE_PATH, --source-path SOURCE_PATH
                        Mention the source path of the file or directory which needs to be backup
  -dp DESTINATION_PATH, --destination-path DESTINATION_PATH
                        Mention the destination path of the backup
  -lobp LOCALHOST_OBJECT_TO_BACKUP_PATH, --localhost-object-to-backup-path LOCALHOST_OBJECT_TO_BACKUP_PATH
                        Mention the localhost object to be remote backup
  -rbdp REMOTE_BACKUP_DIRECTORY_PATH, --remote-backup-directory-path REMOTE_BACKUP_DIRECTORY_PATH
                        Mention the remote backup directory on the remote host
  -u USERNAME, --username USERNAME
                        Remote connection username of the backup source host
  -hs HOSTNAME, --hostname HOSTNAME
                        Backup endpoint hostname
  -mab MAX_AMOUNT_BACKUP, --max-amount-backup MAX_AMOUNT_BACKUP
                        maximum amount of backups to be kept
                        
'''
