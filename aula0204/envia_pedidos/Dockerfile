FROM python
RUN apt-get update && apt-get install python3-pip -y
WORKDIR /envia_pedidos
COPY . /envia_pedidos/
RUN pip install -r requirements.txt 

CMD ["python","envia_pedidos.py"] 
