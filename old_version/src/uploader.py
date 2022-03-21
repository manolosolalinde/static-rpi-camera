
from google.oauth2 import service_account
from google.cloud import storage
import os

''' Project objective
Upload files in folder 
    -- instantiate object: RPUploader rpu(outputfolder)
    -- all files: RPUploader rpu.upload_all()
    -- specific timeframe: rpu.upload_timeframe(initialtime,finaltime)
Uploaded files are renamed to 

'''

class RPUploader():
    def __init__(self, output_directory,auth_key = None):
        if (auth_key == None):
            service_account_info = {'type': 'service_account',
                            'project_id': 'brave-airship-247719', 
                            'private_key_id': 'bc2a9a6c6f926fc9cb0d141eecc1394d68743a06', 
                            'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDK6jrOzTG0GblH\ncKoR3Zor0oPEBTvu+QDO7owOzjTcNbhO2PRwW5BHcW/QTEVvGjos+sa2XU2WLdnp\n3m+YTZiuGK6OsHHQp9SASSu8QAOOlpLKXXrjpRG8pwlG+eOANXAkaSUgkiC8EvaY\nNQfAC9pUX0JLIsRtVFeyyGEWnMMVTu8rmrBwGVF5oqpse0QVOLz6K4ChsEFFAXQP\n1xmgAkv3KuQwdSqB7c26nleK+MeGOxni9ToE6MDTVRU5vvNq57ogs/Bc0vVNToOQ\n/dplxt8JFi4KgowmB0VXip7Be01drwecXLZLIZqAK3Bkf4bw3sjnnhsR16ESM/3G\nh1Y+A/wVAgMBAAECggEAAJVNN2xm1IiYk14r5MiGRUcQhvqc303fLxYqnfp1YkEC\nXSYyfDSM/CeVITwihX/0V/Edq0cPMU0gb5Ok0WBWQ6QEVpp4UIwfTg2h96N0jbUW\n5usWl1VFwq/1Tt4wRZGzNHM46kcM4QkkMKpZQ1qW0mufTpxXVaS+9fbEvzbM26Zz\nqbzuzhBA8sl3q5lg4h2xPUXsFYIhwTm8AQD+0jTULwnNejQho2SV86r+uQ084RKN\n5UJ0b+qwF8m4l5cz6ggQ+lnVKbawnWXXo+9wWNvOOv2+ReX0i8O9hTO9oPRgnVqB\nUBZJIvvMxMSKLvIZNKUe5i0kFRx8UoL4UQaP6bPBYQKBgQDvLGyq6pG6We1kn2C7\neaUJylNMh0uGlSlKLsv+G8Jz+oXPU8VYWxBudDhuZ2Xw3nZkvixvX2VrgLD2UDso\n6Nl3PzcrE6vNFm3skV0QDkzHS64DDskWFrxRiLxqX7HQgJccNMR1kRmqvCQj5q0E\nDhX0fXtNSZVHNarhb3KisDEOFwKBgQDZMMd6CUeynuVUqRVuHQTC7MiFbttaM4D+\nnvGlf0nwYjkjL4EWArrtQyJqEFpYdSQCfkEMnNFntAGA9aeNhoezPYtE6fiAjvdl\nI3ldNihNwuEDcIqmIa8DVIE25Xw8PawEi7kvL9zIcjBCz/jalfxaT+Nwxn+pTypV\nLhpYQqkuswKBgEHdeg+XiYpIOZf8TCdU2J5ZmZb5q1LkwPos6QCRpHtMAo2WBELQ\n0TWZy/CbiPdMTE5yEMqa+tMgHZu3fJNHjJvKTOcQA7/27U64uWgyh/JaZRFygO4U\nVMgfX8PrloxU3UhnP7MgwnDCXzGD1SHIv0MVS199ZB64KNbsWiVzYA8BAoGAcv4z\nr3Z4YqdkjsWTViDBI5+Qr605MHHyi12GXfSeJksrK2j8dLXvWK3h67xKyWkELtnA\nATiKWtjgrvHhy7n94TXlphAnBZIshH0axfJltn5G+rY8gqd07VNxsqogdBjHGgUM\ngGJcCDkFOmq4vKsK2JpRtqUydGc4566oPjDVOKcCgYBRLPJmopNSo42x5gdBO6lf\nZU7zOagzRfCYVlTaIm6oVoShxtsNliMpoBm3ZdniTwsqfkZtR88z3Ttq4TqvsPmN\nUZxup6HDUH78mMj7nndbOoK2f/hAkwXfY226b+w/vubUpkh9DqF50/YC8VRnl11Y\n5jDAEvWOPf36czodEtQMSA==\n-----END PRIVATE KEY-----\n', 
                            'client_email': 'replaybox-uploader@brave-airship-247719.iam.gserviceaccount.com', 
                            'client_id': '114678146513649799044', 
                            'auth_uri': 'https://accounts.google.com/o/oauth2/auth', 
                            'token_uri': 'https://oauth2.googleapis.com/token', 
                            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs', 
                            'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/replaybox-uploader%40brave-airship-247719.iam.gserviceaccount.com'}
            self._credentials = service_account.Credentials.from_service_account_info(service_account_info)
        else:
            self._credentials = service_account.Credentials.from_service_account_file(auth_key)
        self._storage_client = storage.Client(project='brave-airship-247719',credentials=self._credentials)
        self._bucket_name = 'replaybox-bucket'
        self._bucket_folder = 'bucket01_input'
        self._output_directory = output_directory

    def list_blobs(self):
        """Lists all the blobs in the bucket."""
        bucket_name = self._bucket_name
        bucket = self._storage_client.get_bucket(bucket_name)
        blobs = bucket.list_blobs()
        for blob in blobs:
            print(blob.name)

    def upload_output(self,initialtime = None,finaltime = None):
        """ Upload all the files in _output_directory """
        bucket = self._storage_client.get_bucket(self._bucket_name)
        # self.list_blobs()
        directory = os.fsencode(self._output_directory)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".h264") or filename.endswith(".aac") or filename.endswith(".txt"): 
                source_file_name = os.path.join(directory.decode("utf-8"), filename)
                destination_blob_name = self._bucket_folder + "/" + filename
                print("Copying from {} to {} ".format(source_file_name,destination_blob_name))
                blob = bucket.blob(destination_blob_name)
                try:
                    blob.upload_from_filename(source_file_name)
                except Exception as e:
                    errorstr = e.__str__()
                    if (errorstr.find("403")!=-1):
                        print("Erro 403: Acceso prohibido (file exist?)")
                    else:
                        print("Unknown error: {}, file not uploaded".format(errorstr))


if __name__ == '__main__':
    # run_quickstart()
    # upload_blob('replaybox-bucket','acl_test.py','bucket01_input/acl_test.py')
    # myuploader = RPUploader(output_directory='../output',auth_key='replaybox-uploader-auth.json')
    myuploader = RPUploader(output_directory='../output')
    myuploader.upload_output_folder()



