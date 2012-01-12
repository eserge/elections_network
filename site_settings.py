import os

# Settings in this file must be edited before deployment

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',                # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_PATH, 'database.sqlite'), # Or path to database file if using sqlite3.
        'USER': '',                                            # Not used with sqlite3.
        'PASSWORD': '',                                        # Not used with sqlite3.
        'HOST': '',                                            # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                            # Set to empty string for default. Not used with sqlite3.
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'uu$m8_^m%69-z&$s=2q#&s9b%6y0_4$v)zk!h1v&q6d6@3+4g6'