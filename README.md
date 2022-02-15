Enter the folder containing the files downloaded from GitHub and create a virtual environment for Python:

python3 -m venv venv

activate the virtual environment:

source venv/bin/activate

install Flask:

pip install Flask

install the required libraries:

pip install -r requirements.txt

start Flask and start the web server:

flask run --host 0.0.0.0

to run it only on localhost:

flask run
