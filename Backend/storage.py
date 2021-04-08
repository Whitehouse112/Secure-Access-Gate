from google.cloud import storage

BUCKET_NAME = 'secure-access-photos'

class Storage:
    def __init__(self):
        self.client = storage.Client()

    def upload_image(self, file, blob_name):
        bucket = self.client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        #blob.make_public()
        try:
            blob.upload_from_string(file)
        except Exception as e:
            print(e)
            return 500
        return 'Success'

    def get_image(self, blob_name):
        bucket = self.client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        if blob.exists():
            return blob.download_to_filename() #TODO: the other one is deprecated, we need to supply a filename
        else:
            return None

    def delete_image(self, blob_name):
        bucket = self.client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        if blob.exists():
            blob.delete

    def check_image(self, blob_name):
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        return blob.exists()