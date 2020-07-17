# dash-flask-docker
Serving multiple Dash apps with Flask and Docker

### 1. Docker build
build your image with:
```docker build -t dashflaskdocker .```

### 2. Edit flask_app.py according to your needs

### 3. Launh stack with docker-compose 
```docker-compose up -d```

### 4. Nginx
By default, docker-compose.yml listen to localhost.
You can proxy a local port to your public ip, although it's not recommended in production.
Follow step-by-step this awesome guide to proxy your container to your domain with Nginx webserver:
[Host docker container with Nginx](https://www.digitalocean.com/community/questions/how-to-host-multiple-docker-containers-on-a-single-droplet-with-nginx-reverse-proxy)

