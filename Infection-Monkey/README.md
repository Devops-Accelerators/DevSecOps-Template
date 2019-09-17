# Infection Monkey

The Infection Monkey is an open source Breach and Attack Simulation (BAS) tool that assesses the resiliency of private and public cloud environments to post-breach attacks and lateral movement.

# Pre-requisites
 - Need docker and docker-compose installed since we are running infection monkey in a container for this project.
 - Download the [infection monkey file](https://www.guardicore.com/infectionmonkey/index.html#download) (.tgz)
 - Load the docker image, once you've extracted it from the .tgz
 ```
 docker load -i dk.monkeyisland.latest.tar
 ```

# Getting Started

 - Run the docker-compose file and navigate to https://\<server-ip\>:5000.
 - To get the Infection Monkey running as fast as possible, click Run Monkey.
 - It can be run on any machine of your choice. Follow the instructions provided once you've reached the infection monkey page and you'll be able to run your scans successfully.
 
