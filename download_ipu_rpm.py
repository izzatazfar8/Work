"""
=========================================================================================================================
Description:    To download latest IPU ingredients from artifactory
-------------------------------------------------------------------------------------------------------------------------
Dependencies/Maintainence:
 hardcoded artifactory url --> https://ubit-artifactory-ba.intel.com/artifactory/ped-bxtn-ipu-local/
 hardcoded latest ipu keyword --> ipu6_adl_dev
 hardcoded foldernames that contains rpms --> 'AIQB','iCameraSrc','IPUFW','LibCamHal','LibIAAIQ','LibIACSS'
 need to use personal username and password to access artifactory. WIP to have faceless account access to remove this dependency
-------------------------------------------------------------------------------------------------------------------------
Sample Command:
python3 download_ipu_rpms.py --username <username> --password <passwd>
=========================================================================================================================
"""

import os
import sys
import argparse
import logging
import requests
import re
import paramiko
import time

from lxml import html
from tqdm import tqdm
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
from requests.compat import urljoin

url = "https://ubit-artifactory-ba.intel.com/artifactory/ped-bxtn-ipu-local/"
keyword = "ipu6_adl_dev"
rpm_directories = ['AIQB','iCameraSrc','IPUFW','LibCamHal','LibIAAIQ','LibIACSS']
sut_path = "/home/root"
def parse_cli(argv):
    parser = argparse.ArgumentParser(
        prog=argv[0],
        description="Download xlink and hddl deb")

    parser.add_argument(
        '--username',
        type=str,
        default="sys_ipu",
        help='username for artifactory')

    parser.add_argument(
        '--password',
        type=str,
        default="image_processing_unit@321",
        help='password for artifactory')

    parser.add_argument(
        '--sut_ip',
        type=str,
        default="",
        help='SUT IP')
    
    args = parser.parse_args(argv[1:])

    return args
    
    

def create_logger(debug):
    logger = logging.getLogger(__name__)
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Stream handler
    stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(stream_formatter)
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)

    return logger

def get_url_content(url, user, pswd):
    try:
        response = requests.get(url, auth = HTTPBasicAuth(user, pswd))
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        main_logger.error(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        main_logger.error(f'Other error occurred: {err}')  # Python 3.6
    else:
        tree = html.fromstring(response.content)

        return(tree)

def download_url_content(url, file_name, user, pswd):
    main_logger.info("Downloading {}".format(url))

    req = requests.get(url, stream=True, auth = HTTPBasicAuth(user, pswd))

    # create download progress bar
    total_size = int(req.headers.get('content-length', 0))
    block_size = 1024
    status_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

    # download file
    with open(file_name, 'wb') as file_handler:
        for data in req.iter_content(block_size):
            status_bar.update(len(data))
            file_handler.write(data)

    status_bar.close()

    if total_size != 0 and status_bar.n != total_size:
        main_logger.error("Download {} incomplete".format(url))
        return(False)

    return(True)

def download_ipu_rpms(url, args):
    target_user = 'root'
    target_pass = ''
    sut = paramiko.SSHClient()
    sut.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sut.connect(hostname=args.sut_ip,port=22,username=target_user,password=target_pass,allow_agent=False,look_for_keys=False)
    host,port = args.sut_ip,22
    
    

    # get latest ipu ingredieents
    tree = get_url_content(url, args.username, args.password).xpath('//a/@href')
    matching_contentname = []
    [matching_contentname.append(contentname) for contentname in tree if keyword in contentname]
    matching_contentname.sort()
    latest_ipu = matching_contentname[-1]
    
    # download latest ipu rpms based on list of folder name
    for rpm_directory in rpm_directories:
        rpmname = get_url_content(url + latest_ipu + rpm_directory, args.username, args.password).xpath('//a/@href')[1]
        download_url_content(url + latest_ipu + rpm_directory + "/" + rpmname, rpmname, args.username, args.password)
            
        print(rpmname)
        
        sftp = sut.open_sftp()
        sftp.put(rpmname , os.path.join(sut_path, rpmname))

        stdin, stdout, stderr = sut.exec_command("rpm -ivh --nodeps " + rpmname)
        time.sleep(3)
        output = stdout.readlines()
        print ("\nSUT output:\n")
        print (output)        
if __name__ == "__main__":
    args = parse_cli(sys.argv)
    sut = parse_cli(sys.argv)
    main_logger = create_logger(False)
    download_ipu_rpms(url, args)
    
    

