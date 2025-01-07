from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables desde el archivo .env

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@127.0.0.1/sistema_tickets"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "tu_clave_secreta_super_segura"
"""     MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'uri21199@gmail.com'
    MAIL_PASSWORD = 'apuz ocmu tcge qbyz'  
    MAIL_DEFAULT_SENDER = 'uri21199@gmail.com' """