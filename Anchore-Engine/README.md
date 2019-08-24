# Setting up Anchore Engine

This guide helps set up anchore engine container so that it can be integrated with the jenkins using anchore engine plugin.

# Pre-requisite

- Must have docker and docker-compose installed on the host.

# Getting Started

  - Clone this repository and move to the Anchore-Engine directory.
    ```
    git clone https://github.com/Devops-Accelerators/DevSecOps.git && cd DevSecOps/Anchore-Engine
    ```
  - Create a directory to persist db data.
    ```
    mkdir -p db
    ```
  - Finally, run the docker image.
    ```
    docker-compose up -d
    ```
