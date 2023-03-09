# change root and directory name
cd D:/venvs/
mkdir my_directory
cd my_directory
py -3.10 -m virtualenv env
env/Scripts/activate
mkdir static
mkdir media
python -m pip install pip-tools
git clone https://github.com/andywar65/dj-hx-patterns
cd dj-hx-patterns
python -m pip install -r requirements.txt
pre-commit install
python generate_env_file.py
python manage.py migrate
python manage.py create_super_user
python manage.py seed_items
.\run
