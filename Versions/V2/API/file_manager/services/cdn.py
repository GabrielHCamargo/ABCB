from services.aws import upload_bucket_s3


async def upload_cdn(file_location, file_path):

    try:
        # faz o upload do arquivo para o bucket S3
        response = upload_bucket_s3(file_location, file_path)
        return response
    except:
        # em caso de erro, retorna uma mensagem de erro
        return "upload error in bucket s3"