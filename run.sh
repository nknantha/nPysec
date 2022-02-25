#!/bin/bash

set -e

# Compiling CSS.
echo
echo Getting dart-sass...
curl --parallel --silent --show-error --location $SASS_URL --output dart-sass.tar.gz
tar --extract --gzip --file dart-sass.tar.gz
chmod u+x dart-sass/sass
echo Compiling sass files...
dart-sass/sass --style compressed --no-source-map scss/styles.scss css/styles.css
echo Compiled successfully...
echo

# Starting server.
echo Starting server...
uwsgi uwsgi.ini
