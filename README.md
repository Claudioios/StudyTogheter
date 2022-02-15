Entrare nella cartella contenente i files scaricati da GitHUB e creare un virtual environment per Python:

python3 -m venv venv

attivare il virtual environment:

source venv/bin/activate

installare Flask:

pip install Flask

installare le librerie richieste:

pip install -r requirements.txt

avviare Flask e far partire il web-server:

flask run --host 0.0.0.0

per farlo partire solo su localhost:

flask run
