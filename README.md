# DevSecOps-Template
This DevSecOps utility includes various open-source security tools that can scan and report vulnerabilities within application code. We have created a parameterize Jenkinsfile, where application repository url, docker image name with tag (Publicly accessible), Server url where application running, and the project type (Java, Node) need to be define as a parameters. the job runs through various different stages as described below:

-	Stage 1 (Checkout SCM): This is the stage where our code is checked out.
-	Stage 2 (pre-build setup): This stage spins up all the necessary security tools in containers so that they are ready to be used.
-	Stage 3 (Check-secrets): Checks if any secrets are committed into your application repository.
-	Stage 4 (Source Composition Analysis): Identifies open source security risks and vulnerabilities of third-party components that was used in application code.
-	Stage 5 (SAST): Inspect the source code of your application and will pinpoint possible security flaws.
-	Stage 6 (Container Image Scan): Performs a thorough scan on the container images and the vulnerabilities are listed out in a json file.
-	Stage 7 (DAST): Test for security flaws once the application is up and running.
- Stage 8 (Inspec): Tests your infrastructure with a inspec profile in the repo.

