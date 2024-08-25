FROM python

WORKDIR /app

RUN pip install beautifulsoup4
RUN pip install requests
RUN pip install "fastapi[standard]"

COPY ./app /app

CMD ["fastapi", "run", "main.py", "--port", "80"]