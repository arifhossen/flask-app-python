sudo usermod -aG docker ubtunu
sudo usermod -aG docker jenkins
groups jenkins
sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock

sudo systemctl restart jenkins

groups jenkins

sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock

sudo systemctl start docker
sudo systemctl enable docker


sudo docker build . -t flask-app:latest
sudo docker run -d -p 7000:7000 flask-app:latest


sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock

sudo apt update
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d app1.aseemcloudtech.com




server {
    listen 80;
    server_name app1.aseemcloudtech.com;

    location / {
        proxy_pass http://127.0.0.1:7000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}


ln -s /etc/nginx/sites-available/a /etc/nginx/sites-enabled/


sudo systemctl restart nginx
# flask-app-python
# flask-app-python



# Shell Scirpt for CICD Item freestyle : write this code in shell script command

# Check if any container is using port 7000 and stop it
if [ "$(docker ps -q -f publish=7000)" ]; then
  echo "Stopping existing container using port 7000..."
  docker stop $(docker ps -q -f publish=7000)
fi

# Check if the image already exists and remove it
if docker image inspect flask-app:latest > /dev/null 2>&1; then
  echo "Removing existing image..."
  docker image rm -f flask-app:latest
fi

# Build the new image
docker build . -t flask-app:latest
echo "Image created"

# Run the new image
docker run -d -p 7000:7000 flask-app:latest
echo "Image run by Docker on port 7000"
