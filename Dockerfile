FROM python:3.8-slim-buster
COPY . .
RUN pip install -e .
CMD streamlit run streets_of_helsinki/app.py --server.port $PORT