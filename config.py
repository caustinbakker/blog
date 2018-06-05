"""Config file."""
DEBUG = True
TESTING = False
TEMPLATES_AUTO_RELOAD = True
SECRET_KEY = '12341231231231223153254redsc234resdf4f34'


PROJECT_ID = 'austinbakkerblog'
DATA_BACKEND = 'Cloud SQL'
CLOUD_STORAGE_BUCKET = 'austinbakkerblog'
CLOUDSQL_IP = '35.234.157.177'
CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'nhjiZBH&**USB987adbs'
CLOUDSQL_DATABASE = 'database'
CLOUDSQL_CONNECTION_NAME = '/cloudsql/austinbakkerblog:europe-west2:mydatabase1'

GOOGLE_CLIENT_ID = '813277836621-1nf78u3rug20sned69jo39qp2qht9ujo.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '79Q3vzZYKdV5k_s7Bj1shaOt'
REDIRECT_URI = 'https://localhost:5000/gCallback'
AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
