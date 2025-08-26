# 引入模块
from obs import ObsClient, PutObjectHeader
import os

# 创建ObsClient实例
obsClient = ObsClient(
    access_key_id='UXC42LP5RRWVWSCHBWRT',     # 替换成你的Access Key ID
    secret_access_key='W80HelKVRo4Gdpc93rWLPbnPnJGdT00Eb6MOtgg7',  # 替换成你的Secret Access Key
    server='obs.cn-north-4.myhuaweicloud.com'   # 替换成你的服务器地址
)




# 定义上传文件的函数
def upload_file(client, bucket_name, local_path, obs_path, headers=None):
    try:
        resp = client.putFile(
            bucket_name,
            obs_path,
            local_path,
            headers=headers
        )
        if resp.status < 300:
            print('Upload successful for:', obs_path)
            print('objectUrl:', resp.body.objectUrl)
            print('requestId:', resp.requestId)
            print('etag:', resp.body.etag)
            print('versionId:', resp.body.versionId)
            print('storageClass:', resp.body.storageClass)
        else:
            print('Failed to upload:', obs_path)
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
    except Exception as e:
        print('Error uploading', obs_path, 'with exception:', e)




def uploadtoday(tian):
    files_to_upload = []

    def find_2024(path):
        if not os.path.exists(path):
            print(f"The path {path} does not exist.")
            return

        for root, dirs, files in os.walk(path):
            for dir_name in dirs:
                if dir_name.startswith(tian):
                    directory = os.path.join(root, dir_name)
                    for entry in os.listdir(directory):
                        file_path = os.path.join(directory, entry)
                        # Create dictionary for each file with local_path and obs_path
                        obs_path = f"test_{entry}"  # Example: Constructing obs_path
                        file_info = {
                            'local_path': file_path,
                            'obs_path': obs_path
                        }
                        files_to_upload.append(file_info)
                        # Optionally, print the file info for verification
                        #print(file_info)

        # If you want to return the list of dictionaries
        return files_to_upload

    # Example usage:
    files_to_upload = find_2024(os.path.dirname(os.path.abspath(__file__)))

    for file_info in files_to_upload:
        upload_file(
            obsClient,
            'obs1111112',  # 替换成你的桶名
            file_info['local_path'],
            file_info['obs_path'],
            headers=PutObjectHeader()  # 可以设置headers，例如 contentType
        )

    # 关闭obsClient
    obsClient.close()
#uploadtoday('2024-07-18')