# Dockerfile
FROM python:3.8-slim
ADD ./ /app
WORKDIR /app

# Instalamos dependencias
RUN pip3 install -r requirements.txt

# Abrimos puerto http
EXPOSE 8080

RUN chmod +x entrypoint.sh
ENTRYPOINT ["bash", "entrypoint.sh"]