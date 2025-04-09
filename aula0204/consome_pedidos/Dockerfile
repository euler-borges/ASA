FROM python
RUN apt-get update && apt-get install python3-pip -y
WORKDIR /consome_pedidos
COPY . /consome_pedidos/
RUN pip install -r requirements.txt 

CMD ["python","consome_pedidos.py"] 