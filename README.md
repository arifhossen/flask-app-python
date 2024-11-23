# Setting Up Jenkins and Docker on an Ubuntu EC2 Instance with CI/CD Pipeline

This guide provides step-by-step instructions for launching an Ubuntu EC2 instance, installing Jenkins and Docker, and setting up a Jenkins CI/CD pipeline to deploy a Python application.

## Step 1: Launch an Ubuntu EC2 Instance

### Login to AWS Management Console:
1. Navigate to the EC2 Dashboard and launch a new instance.
2. Choose an Ubuntu AMI (e.g., "Ubuntu Server 20.04 LTS").

### Instance Configuration:
1. Select an instance type (e.g., t2.small for testing purposes).
2. Configure instance details (e.g., VPC, subnet).
3. Add storage (default 8 GB is typically sufficient for Jenkins).

### Security Group Configuration:
1. Add rules to allow SSH (port 22) from your IP address.
2. Add rules to allow HTTP (port 8080 for Jenkins default port) and HTTPS (port 443).
3. Add rules to allow the Python application to run on custom port 7999.

### Launch Instance:
1. Review and launch the instance.
2. Download or select an existing key pair to SSH into your instance.

## Step 2: Connect to Your Instance

### SSH into Your Instance:
Open your terminal and connect to your instance using the key pair.
```bash
ssh -i /path/to/your-key.pem ubuntu@your-ec2-public-dns
```

## Step 3: Update Ubuntu System Packages

### Update System Packages:
Update the package list and install the latest updates.
```bash
sudo apt update
sudo apt upgrade -y
```

## Step 4: Install Java and Jenkins

### Install Java:
Jenkins requires Java to run. Install Java using the following commands:
```bash
sudo apt update
sudo apt install fontconfig openjdk-17-jre
java -version
```

### Install Jenkins:
Add the Jenkins repository and install Jenkins.
```bash
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins
```

### Start Jenkins:
Enable and start the Jenkins service.
```bash
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins
```

## Step 5: Configure Jenkins

### Access Jenkins:
Open a web browser and navigate to `http://your-ec2-public-dns:8080`.

### Unlock Jenkins:
Retrieve the initial admin password.
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
Copy the password and paste it into the "Administrator password" field.

### Customize Jenkins:
1. Install suggested plugins.
2. Create your first admin user.
3. Configure the Jenkins instance.

## Step 6: Install Docker on Ubuntu

### Install Docker:
Install Docker using the following command:
```bash
sudo apt install docker.io -y
```

### Add Docker to User Group:
Add the `ubuntu` and `jenkins` users to the Docker group and set permissions.
```bash
sudo usermod -aG docker ubuntu
sudo usermod -aG docker jenkins
groups jenkins
sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock
sudo systemctl restart jenkins
sudo systemctl start docker
sudo systemctl enable docker
```

## Step 7: Create Jenkins Pipeline CI/CD

### Create a New Item in Jenkins:
1. Create a new freestyle project in Jenkins.
2. Configure Source Code Management to use a Git repository.
3. Add a build step to run a shell script.

### Shell Script for CI/CD Pipeline:
```bash    
# Check if any container is using port 7999 and stop it
if [ "$(docker ps -q -f publish=7999)" ]; then
    echo "Stopping existing container using port 7999..."
    docker stop $(docker ps -q -f publish=7999)
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
docker run -d -p 7999:7999 flask-app:latest
echo "Image run by Docker on port 7999"
```

### Save and Build the Project:
Save your configuration and build the project. Access your application at:
```bash
http://your-ec2-public-dns:7999/
```

## Step 8: Install Nginx

### Install Nginx:
```bash
sudo apt update
sudo apt install nginx
```

### Install Certbot for SSL:
```bash
sudo apt install certbot python3-certbot-nginx
```

## Step 9: Configure Nginx for SSL and Proxy

### Obtain an SSL Certificate:
```bash
sudo certbot --nginx -d pythonapp.arifhossen.net
```

### Nginx Configuration:
Create a new configuration file for your site.
```bash
sudo nano /etc/nginx/sites-available/arifhossen.net
```

### Example Nginx Configuration:
```bash
server {
    listen 80;
    server_name pythonapp.arifhossen.net;

    location / {
        proxy_pass http://127.0.0.1:7999;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Enable the Site:
Create a symlink to the configuration file in the sites-enabled directory.
```bash
sudo ln -s /etc/nginx/sites-available/arifhossen.net /etc/nginx/sites-enabled/
```

### Test and Reload Nginx:
Test the Nginx configuration for syntax errors.
```bash
sudo nginx -t
```
Reload Nginx to apply the changes.
```bash
sudo systemctl reload nginx
```

### Disable a Site:
To disable a site, remove the symlink from the sites-enabled directory.
```bash
sudo rm /etc/nginx/sites-enabled/arifhossen.net
```
Reload Nginx to apply the changes.
```bash
sudo systemctl reload nginx
```

By following these steps, you will have set up Jenkins and Docker on an Ubuntu EC2 instance, created a CI/CD pipeline to deploy a Python application, and configured Nginx for SSL and proxy settings.