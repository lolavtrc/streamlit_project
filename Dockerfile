# app/Dockerfile

# Utilisez l'image Python 3.9-slim comme base
FROM python:3.9-slim

# Définissez le répertoire de travail dans /app
WORKDIR /app

# Installez les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clonez le code de votre projet (ne pas oublier le point à la fin)
RUN git clone https://github.com/lolavtrc/streamlit_project.git .

# Copiez le fichier requirements.txt depuis le répertoire local vers /app dans le conteneur
COPY ./app/requirements.txt /app/requirements.txt
COPY ./app/app_python.py /app/app_python.py
COPY ./app/data/tmdb_5000_movies.csv /app/data/tmdb_5000_movies.csv

# Installez les dépendances Python depuis requirements.txt
RUN pip install -r /app/requirements.txt

# Exposez le port 8504 (si nécessaire)
EXPOSE 8504

# Commande de vérification de l'état de santé (healthcheck)
HEALTHCHECK CMD curl --fail http://localhost:8504/_stcore/health

# Commande d'entrée pour exécuter Streamlit
ENTRYPOINT ["streamlit", "run", "app_python.py", "--server.port=8501", "--server.address=0.0.0.0"]