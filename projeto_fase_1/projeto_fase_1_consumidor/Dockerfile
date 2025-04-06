FROM python
RUN apt-get update && apt-get install python3-pip -y
WORKDIR /projeto
COPY projeto /projeto/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 
EXPOSE 8000
CMD ["python", "./processamento_paralelo/consumer_pedidos.py", "&", "uvicorn","main:app", "--host", "0.0.0.0", "--port", "8000"] 
# CMD sh -c "python ./processamento_paralelo/consumer_pedidos.py & uvicorn main:app --host 0.0.0.0 --port 8000"


