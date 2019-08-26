# ArcherySec-Zed
  This guide helps you set up archerysec, a tool that helps developers and pentesters to perform scans and manage vulnerabilities, and run a OWASP-**Z**ed **A**ttack **P**roxy (**ZAP**) scan to detect security vulnerabilities in your application. ZAP is run on the target url where our application is running and Archerysec will import the scanned results from ZAP and display the detected vulnerabilities in our application.
  
# Pre-requisites
- Must have docker and docker-compose installed.
  
# Getting Started
-  Run the docker-compose file to set up the environment on your system.
  ```
  git clone https://github.com/Devops-Accelerators/DevSecOps-Template.git && cd Archerysec-ZeD
  
  docker-compose up -d
  ```
- Once the containers are up and running check if they are accessible by accessing the below urls
  ```
  ArcherySec: http://your_system_ip_address:8000
  OWASP ZAP: http://your_system_ip_address:8090
  ```
- Open the ArcherySec portal, go to the settings page <http://your_system_ip_address:8000/webscanners/setting>, edit the ZAP settings by providing ZAP API Host & ZAP API Port.

- Next step is to install archerysec-cli tool on the jenkins server.
  ```
  pip install archerysec-cli
  Or 
  git clone https://github.com/archerysec/archerysec-cli.git
  cd archerysec-cli
  pip install -r requirements.txt

  # Install jq tool
  sudo apt-get install jq
  ```

  
