# build_files.sh
pip install -r requirements.txt
pip freeze > requirements.txt

python3.10 manage.py makemigrations --noinput
python3.10 manage.py migrate --noinput