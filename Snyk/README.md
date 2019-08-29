# Snyk
  Snyk enables you to find, and more importantly fix known vulnerabilities in your open source.This guide helps you intergrate snyk with     jenkins so that you can scan vunerabilities in your application before you deploy it to production.
  
# Prerequisites
  - You must sign up for an account with Snyk before you begin.
  - Install the [snyk plugin](https://snyk.io/docs/install-the-snyk-plugin/) in the jenkins server.
  
# Getting started
  - Go to the pipeline script generator in jenkins, find snykSecurity in the drop-down, fill in the required fields and generate the        pipeline script.
  - Copy the generated pipe syntax and run it in a stage you want to.
  - Refer to this [link](https://snyk.io/docs/snyk-for-your-pipeline/) for further details.
  

