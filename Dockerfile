# aqui você vai colocar a versão do python que tu ta usando
FROM python:3.9-slim 

# aqui você vai colocar o diretório onde o app vai ficar
WORKDIR /app

# aqui você vai copiar o app para o diretório
COPY app/ /app

# aqui você vai instalar o flask
RUN pip install flask

# aqui você vai expor a porta 5000 da maquina virtual para o seu pc
EXPOSE 5000

# aqui você vai rodar o app
CMD ["python", "main.py"] 

# no lugar de main.py você vai colocar o nome do arquivo que você quer rodar
