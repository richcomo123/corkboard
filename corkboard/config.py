import os

class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BCRYPT_LOG_ROUNDS = 12

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'richcomo123@gmail.com'
    MAIL_PASSWORD = 'ttka qvas cldz ltvg'

    UPLOAD_FOLDER = 'static/uploads'


