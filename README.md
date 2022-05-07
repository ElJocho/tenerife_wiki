# Tenerife Wiki

Here code for a geo-wiki is emerging. It is done as a part of a university field trip to tenerife.

For users the website is available under: tbd

# Installation
## For Linux (Ubuntu 18.04)

### Prerequisites:

- git, docker und docker-compose
- python >= 3.8 und venv

```
sudo apt install git-all
curl -sSL https://get.docker.com | sh
sudo apt-get install -y libffi-dev libssl-dev
sudo apt-get install -y python3 python3-pip
sudo apt-get remove python-configparser
# für dockersetup:
sudo pip3 -v install docker-compose
# für cmd setup:
sudo pip3 install virtualenv
```

## Installation for Developers:

In new folder:
```
git clone https://github.com/ElJocho/tenerife_wiki.git
# für dockersetup:
docker-compose -f docker-compose.dev.yaml up -d --build --force-recreate
# rest für commandline setup
cd web_master
```
In web_master:
```
virtualenv .venv
source ./venv/bin/activate
pip install -r requirements.txt
cd ..
export $(cat .env | xargs)
cd web_master
python main.py
```

## For Windows

*Dockersetup:*

http://git-scm.com/download/win -> download and install git

https://docs.docker.com/docker-for-windows/install/ -> download and install docker-desktop.

Wsl2 for windows could need an update. If that is the case:

https://docs.microsoft.com/de-de/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package --> Do steps 4 and 5.

In new folder:

```git clone https://github.com/ElJocho/tenerife_wiki.git```  

Delete from web_master/Dockerfile the following part:
```
# get pg to check for database status
RUN apt-get update && \
    apt-get install --yes --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/*

```
Please do not commit and upload this change so it stays local ;)!

Then open the console and type:

```docker-compose -f docker-compose.dev.yaml up -d --build --force-recreate``` ausführen,

With 

```docker ps```

you can check if all dockers are running, if not, execute

```docker-compose -f docker-compose.dev.yaml up -d```.

Now a db with a flask background should be running on your computer.