# Step 1: Launch an Ubuntu EC2 Instance
Login to AWS Management Console:

Go to the EC2 Dashboard and launch a new instance.
Choose an Ubuntu AMI (Amazon Machine Image), such as "Ubuntu Server 20.04 LTS".
Instance Configuration:

Select instance type (e.g., t2.small for testing purposes).
Configure instance details (e.g., VPC, subnet).
Add storage (default 8 GB is typically sufficient for Jenkins).
Security Group Configuration:

Add rules to allow SSH (port 22) from your IP address.
Add rules to allow HTTP (port 8080 for Jenkins default port) and HTTPS (port 443).
Add rules to allow Python Application run custom port on 7000

Launch Instance:

Review and launch the instance.
Download or select an existing key pair to SSH into your instance.


# Step 2: Connect to Your Instance
SSH into Your Instance:
Open your terminal and connect to your instance using the key pair.
```bash
ssh -i /path/to/your-key.pem ubuntu@your-ec2-public-dns
```

# Step 3: Update Ubuntu System Packages

Update System Packages: Update the package list and install the latest updates.

```bash
sudo apt update
sudo apt upgrade -y
```

## Install Java and Jenkins on Ubuntu
Below the reference site for installation
https://www.jenkins.io/doc/book/installing/linux/#debianubuntu

### Installation of Java
Jenkins requires Java to run, yet not all Linux distributions include Java by default. Additionally, not all Java versions are compatible with Jenkins.

```bash
sudo apt update
sudo apt install fontconfig openjdk-17-jre
java -version
```


### Install Jenkins:
On Debian and Debian-based distributions like Ubuntu you can install Jenkins through apt.
```bash
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins
```

### Start Jenkins
You can enable the Jenkins service to start at boot with the command:
```bash
sudo systemctl enable jenkins
```
You can start the Jenkins service with the command:

```bash
sudo systemctl start jenkins
```
You can check the status of the Jenkins service using the command:

```bash
sudo systemctl status jenkins
```

If everything has been set up correctly, you should see an output like this:

Loaded: loaded (/lib/systemd/system/jenkins.service; enabled; vendor preset: enabled)
Active: active (running) since Tue 2018-11-13 16:19:01 +03; 4min 57s ago



###  Step 4: Configure Jenkins
Access Jenkins:

Open a web browser and navigate to http://your-ec2-public-dns:8080.

Unlock Jenkins:
Retrieve the initial admin password.

sudo cat /var/lib/jenkins/secrets/initialAdminPassword

Copy the password and paste it into the "Administrator password" field.

### Customize Jenkins:

    Install suggested plugins.

    Create your first admin user.

    Configure Jenkins instance.


## Create New Item and source code setup and scirpt command
Create a new freestyle project in Jenkins.

Configure Source Code Management to use a Git repository.

Add a build step to run a shell script.


```Bash    
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
```

 Save and build the project.



## Install docker on Ubuntu
```Bash
apt install docker.io -y
```

## Docker add to user group
```Bash
sudo usermod -aG docker ubtunu
sudo usermod -aG docker jenkins
groups jenkins
sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock
sudo systemctl restart jenkins
sudo systemctl start docker
sudo systemctl enable docker
```

## nginx install
```bash
nginx -v
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

## SSL Certificate add by nginx for Subdomain
```bash
sudo certbot --nginx -d pythonapp.arifhossen.net
```

## nginx (for configuration files)
```bash
cd /etc/nginx/
```

## nginx sites-available
```bash
cd /etc/nginx/sites-available/
```

## sites-enabled: This directory contains symlinks to the configuration files in sites-available that are enabled.
```bash
/etc/nginx/sites-enabled/
```


##  Managing Virtual Hosts

## Managing Virtual Hosts
Create a Virtual Host Configuration:  Create a new configuration file in the sites-available directory.
```bash
sudo nano /etc/nginx/sites-available/arifhossen.net
```

Example content for example.com: 
```bash
server {
    listen 80;
    server_name pythonapp.arifhossen.net;

    location / {
        proxy_pass http://127.0.0.1:7000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Enable the Site:
Create a symlink from the sites-available configuration file to the sites-enabled directory.
```bash
sudo ln -s /etc/nginx/sites-available/arifhossen.net /etc/nginx/sites-enabled/
```

## Test Nginx Configuration:
Test the Nginx configuration for syntax errors.
```bash
sudo nginx -t
```

If the test is successful, you should see: 
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

## Reload Nginx:

Reload Nginx to apply the changes.
```bash
sudo systemctl reload nginx
```

##  Additional Information
### Disabling a Site:

To disable a site, remove the symlink from the sites-enabled directory.
```bash
sudo rm /etc/nginx/sites-enabled/arifhossen.net
```

Then reload Nginx to apply the changes:
```bash
sudo systemctl reload nginx
```
