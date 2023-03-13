from core.configs import settings
from core.aws import get_s3_client


def upload_bucket_s3(file_location, file_path):
    # obtem o cliente S3
    s3 = get_s3_client()

    # abre o arquivo em modo de leitura binária ("rb")
    with open(file_location, "rb") as f:
        # faz o upload do arquivo usando o cliente S3
        s3.upload_fileobj(f, settings.AWS_BUCKET_NAME, file_path)
    
    # retorna a URL pública do arquivo armazenado no bucket S3
    return f"{settings.AWS_CDN_URL}/{file_path}"