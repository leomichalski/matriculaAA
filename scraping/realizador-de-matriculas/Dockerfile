FROM leommiranda/pyautogui:latest

RUN apt-get update && apt-get install --no-install-recommends -y \
    # psycopg2 related
    build-essential \
    libpq-dev \
    # clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /scraping

COPY realizador-de-matriculas/requirements.txt /tmp/
RUN pip install --default-timeout=15000 --no-cache-dir -r /tmp/requirements.txt

COPY realizador-de-matriculas/elementos_das_telas elementos_das_telas
COPY realizador-de-matriculas/realiza_uma_matricula.py .
COPY realizador-de-matriculas/realizador_de_matriculas.py .

COPY utils utils

CMD ["python3", "realizador_de_matriculas.py"]
