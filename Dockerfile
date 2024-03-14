FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/AltaoBE/rhs_rss_convertor .

RUN pip3 install -r requirements.txt

EXPOSE 9998

HEALTHCHECK CMD curl --fail http://localhost:9998/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=9998", "--server.address=0.0.0.0"]