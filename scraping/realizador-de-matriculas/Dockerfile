FROM leommiranda/pyautogui:latest

RUN apt-get update && apt-get install --no-install-recommends -y \
    # psycopg2 related
    build-essential \
    libpq-dev \
    # clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY scraping/realizador-de-matriculas/requirements.txt /tmp/
RUN pip install --default-timeout=15000 --no-cache-dir -r /tmp/requirements.txt

COPY scraping/realizador-de-matriculas/elementos_das_telas elementos_das_telas
COPY scraping/realizador-de-matriculas/realiza_uma_matricula.py .
COPY scraping/realizador-de-matriculas/realizador_de_matriculas.py .

COPY scraping/utils utils
COPY database/database.py .

CMD ["python3", "/app/realizador_de_matriculas.py"]
