#!/bin/bash -e

# Compiling CSS.
echo Getting dart-sass...
curl --parallel --silent --show-error --location $SASS_URL --output dart-sass.tar.gz
tar --extract --gzip --file dart-sass.tar.gz
chmod u+x dart-sass/sass
echo Compiling sass files...
dart-sass/sass --style compressed --no-source-map npysec/static/scss/styles.scss npysec/static/css/styles.css
echo Compiled successfully...

# Database setup.
echo Setting up database...
python npysec/setupdb.py

# Starting server.
echo Starting server...
uwsgi uwsgi.ini
