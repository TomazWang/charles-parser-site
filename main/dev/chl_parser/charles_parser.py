import json
import os
from datetime import datetime
import zipfile

import requests
from flask import url_for, current_app

from main.dev.chl_parser import json_parser

TEMP_FILE_FOLDER = 'temp/charles_parser'
DOWNLAOD_DIR = 'download'


class Result:
    """
    The container of the result of parsing.
    """
    RC_SUCCESS = 0

    RC_ERR_FILE_EXT = -100      # 檔案類型錯誤（副檔名錯誤）
    RC_ERR_FILE_TYPE = -101     # 檔案解析錯誤（應該是正確的類型，但是卻無法解析）

    RC_ERR_CONTENT_CANN = -201  # 無法取得檔案

    RC_ERR_UNKNOWN = -999

    def __init__(self, rc, error='') -> None:
        super().__init__()
        self.file_name = ''
        self._rc = -999
        self.rm = ''
        self.error = error
        self.rc = rc

    @property
    def rc(self):
        return self._rc

    @rc.setter
    def rc(self, rc):
        self._rc = rc
        if rc == Result.RC_SUCCESS:
            self.rm = '處理成功'
        elif rc == Result.RC_ERR_FILE_EXT:
            self.rm = '檔案類型錯誤'
        elif rc == Result.RC_ERR_FILE_TYPE:
            self.rm = '解析失敗，解析檔案時發生錯誤'
        elif rc == Result.RC_ERR_CONTENT_CANN:
            self.rm = '無法取得原始檔案'
        elif rc == Result.RC_ERR_UNKNOWN:
            self.rm = '解析檔案時發生錯誤，去罵 @tomaz ({})'.format(self.error)


def zipdir(dir_path, dest="") -> str:
    """
    input : Folder path and name
    output: using zipfile to ZIP folder
    """
    if dest == "":
        zf = zipfile.ZipFile(dir_path + '.zip', zipfile.ZIP_DEFLATED)
    else:
        zf = zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED)

    current_path = os.getcwd()
    os.chdir(dir_path)

    for root, dirs, files in os.walk("./"):
        for f in files:
            zf.write(os.path.join(root, f))

    zf.close()
    os.chdir(current_path)
    return dest


def from_url(url: str) -> Result:
    """
    Parse charles session file with json format from a url.

    1. Create a temp file for results.
    2. Download the file from url.

    :param url: a link to charles session file with .chlsj extension
    :type url: str
    
    :return: a Result obj.
    :rtype: Result
    """

    if not url.endswith('.chlsj'):
        return Result(Result.RC_ERR_FILE_EXT)

    # temp file name
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    temp_file_name = './{}/temp_{}.json'.format(TEMP_FILE_FOLDER, timestamp)

    print(os.curdir)

    # check if temp folder exists
    if not os.path.exists('./{}'.format(TEMP_FILE_FOLDER)):
        os.makedirs('./{}'.format(TEMP_FILE_FOLDER))

    # download file from url
    r = requests.get(url)
    content = r.content.decode('utf-8')
    json_content = json.loads(content)

    if json_content is not None:
        folder, output_file_arr = json_parser.parse(temp_file_name,
                                                    suffix=timestamp,
                                                    json_content=json_content)
    else:
        return Result(Result.RC_ERR_CONTENT_CANN)

    folder_path = './{}/{}'.format(TEMP_FILE_FOLDER, folder)

    # zipfile

    # Check if the download folder exists
    if not os.path.exists('./{}'.format(DOWNLAOD_DIR)):
        os.mkdir('./{}'.format(DOWNLAOD_DIR))

    # Create an output file located at download dir.
    zipf_path = './{}/{}.zip'.format(DOWNLAOD_DIR, folder)
    zipdir(folder_path, dest=zipf_path)

    # Get public url for this file
    result = Result(Result.RC_SUCCESS)
    result.file_name = '{}.zip'.format(folder)

    return result
