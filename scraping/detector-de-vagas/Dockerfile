FROM leommiranda/pyautogui:latest

RUN apt-get update && apt-get install --no-install-recommends -y \
    # psycopg2 related
    build-essential \
    libpq-dev \
    # clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY scraping/detector-de-vagas/requirements.txt /tmp/
RUN pip install --default-timeout=15000 --no-cache-dir -r /tmp/requirements.txt

COPY scraping/detector-de-vagas/elementos_das_telas elementos_das_telas
COPY scraping/detector-de-vagas/detector_de_vagas.py .
COPY scraping/detector-de-vagas/utils utils

COPY database/database.py .

RUN mkdir arquivos_html

CMD ["python3", "/app/detector_de_vagas.py"]
