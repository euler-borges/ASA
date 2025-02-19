FROM python
RUN apt-get update && apt-get install python3-pip -y
WORKDIR /projeto_fast_api_teste
COPY projeto_fast_api_teste /projeto_fast_api_teste/
RUN pip install -r requirements.txt 
EXPOSE 8000
CMD ["uvicorn","main:app", "--host", "0.0.0.0", "--port", "8000"] 
