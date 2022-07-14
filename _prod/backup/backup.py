#!/usr/bin/python3

""""
Backup data to google drive
"""

import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import sys
from dotenv import load_dotenv

load_dotenv()


def ensure_drive(path_to_credentials=os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_PATH')):
    """
    Ensure that the drive exists
    """
    gauth = GoogleAuth()
    scope = ["https://www.googleapis.com/auth/drive"]
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(path_to_credentials, scope)
    return GoogleDrive(gauth)


def create_folder(folder_name):
    """
    Create folder in google drive
    """
    drive = ensure_drive()

    # Create a folder if it doesn't exist
    folder_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for folder1 in folder_list:
        if folder1['title'] == folder_name:
            # print('Folder %s already exists' % folder_name)
            return folder1
    folder = drive.CreateFile({'title': folder_name, "mimeType": "application/vnd.google-apps.folder"})
    folder.Upload()
    print('Created folder: %s' % folder['title'])
    return folder


def upload_file(file_path, file_name):
    """
    Upload file to google drive
    """
    drive = ensure_drive()
    folder = create_folder("backup")
    # Upload a file to folder
    file1 = drive.CreateFile({'title': file_name, "parents": [{"kind": "drive#fileLink", "id": folder['id']}]})
    file1.SetContentFile(file_path)
    file1.Upload()
    print('Uploaded file: %s' % file1['title'])
    return file1


def delete_file(file_name):
    """
    Delete file from google drive
    """
    drive = ensure_drive()
    folder = create_folder("backup")

    # Delete a file in folder
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % folder['id']}).GetList()
    for file1 in file_list:
        if file1['title'] == file_name:
            file1.Delete()
            print('Deleted file: %s' % file1['title'])
            return file1


def list_all_files(in_folder: bool = False):
    """
    List all files in google drive
    """
    drive = ensure_drive()
    folder = create_folder("backup")
    if in_folder:
        # List all files in folder
        file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % folder['id']}).GetList()
        for file1 in file_list:
            print('Title: %s, ID: %s' % (file1['title'], file1['id']))
        return file_list

    # List all files in folder
    file_list = drive.ListFile({'q': "trashed=false"}).GetList()
    for file1 in file_list:
        print('Title: %s, ID: %s' % (file1['title'], file1['id']))
    return file_list


def cleanup():
    """
    Cleanup function
    """
    # if files in our folder is more than 10, delete the oldest one
    drive = ensure_drive()
    folder = create_folder("backup")

    # List all files in folder
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % folder['id']}).GetList()
    if len(file_list) > 10:
        file_list.sort(key=lambda x: x['modifiedDate'])
        file1 = file_list[0]
        file1.Delete()
        print('Deleted file: %s' % file1['title'])
        return file1


def reset():
    """
    Reset function
    """
    drive = ensure_drive()
    folder = create_folder("backup")
    # Delete all files in folder
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % folder['id']}).GetList()
    for file1 in file_list:
        file1.Delete()
        print('Deleted file: %s' % file1['title'])
    # Delete everything in the root folder
    file_list = drive.ListFile({'q': "trashed=false"}).GetList()
    for file1 in file_list:
        file1.Delete()
        print('Deleted file: %s' % file1['title'])


def download_file(file_name, path_to_save):
    """
    Download file from google drive
    """
    drive = ensure_drive()
    folder = create_folder("backup")
    # Download a file in folder and save it locally
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % folder['id']}).GetList()
    for file1 in file_list:
        if file1['title'] == file_name:
            file1.GetContentFile(path_to_save)
            print('Downloaded file: %s' % file1['title'])
            return file1


def share_folder_with_email(email):
    """
    Share folder with specific email
    """
    drive = ensure_drive()
    folder = create_folder("backup")
    # Share folder with specific email
    folder.InsertPermission(
        {
            'type': 'user',
            'value': email,
            'role': 'reader'
        }
    )


def main():
    """
    Main function
    """

    if len(sys.argv) < 2:
        print("Usage: backup.py <file_path> <file_name>")
        sys.exit(1)

    file_path = sys.argv[1]
    file_name = sys.argv[2]

    upload_file(file_path, file_name)
    cleanup()
    print("In the backup folder:")
    list_all_files(in_folder=True)

    # Download the file (Debugging)
    # download_file(file_name, "/tmp/%s" % file_name)
    print("Done")


if __name__ == '__main__':
    main()
    sys.exit(0)
