import os
import boto3

# Проверяем переменные окружения
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")

print("AWS_ACCESS_KEY_ID:", AWS_ACCESS_KEY_ID)
print("AWS_SECRET_ACCESS_KEY:", "*****" if AWS_SECRET_ACCESS_KEY else None)
print("AWS_STORAGE_BUCKET_NAME:", AWS_STORAGE_BUCKET_NAME)
print("AWS_S3_REGION_NAME:", AWS_S3_REGION_NAME)

# Инициализация клиента
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION_NAME,
)

# Локальный файл для теста
local_file_path = "7.jpg"  # создай любой файл рядом с этим скриптом
s3_key = "products/test_upload.jpg"  # путь в бакете

# Загрузка файла
try:
    with open(local_file_path, "rb") as f:
        s3.put_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_key, Body=f)
    print(f"Файл успешно загружен в S3: {s3_key}")
    print(f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/{s3_key}")
except Exception as e:
    print("Ошибка при загрузке в S3:", e)
