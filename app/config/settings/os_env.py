import os

SECRET_KEY = os.environ.get('SECRET_KEY')
DB_NAME=os.environ.get('DB_DATABASE_NAME')
DB_USER=os.environ.get('DB_USER')
DB_PASS=os.environ.get('DB_PASS')
DB_PORT=os.environ.get('DB_DESTINATION_PORT')
DB_HOST=os.environ.get('DB_HOST')
AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME=os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_LOCATION=os.environ.get('AWS_LOCATION')