/*properties ([
  parameters([
    [$class: 'GlobalStringParameterDefinition', defaultValue: '', description: "git url of the application's repo", name: 'appRepoURL'],
    [$class: 'GlobalStringParameterDefinition', defaultValue: '', description: "name of the image", name: 'dockerImage'],
    [$class: 'GlobalStringParameterDefinition', defaultValue: '', description: "web application's url", name: 'targetURL']
  ])
])*/

def repoName;
node {
  
        stage ('Checkout SCM') 
        {
          checkout scm
          workspace = pwd ()
          sh "ls -al" 
        }
  
        stage ('pre-build setup')
        {
         sh"""
         docker-compose -f Sonarqube/sonar.yml up -d
         docker-compose -f Anchore-Engine/docker-compose.yaml up -d
         docker-compose -f Archerysec-ZeD/docker-compose.yml up -d
         """
        }
        
        /*stage ('Check secrets')
        {
           sh """
            rm trufflehog || true
            docker run gesellix/trufflehog --json --regex ${appRepoURL} > trufflehog
            cat trufflehog
            mkdir -p reports/trufflehog
            mv trufflehog reports/trufflehog
            """
        } 
        
        stage ('Source Composition Analysis')
        {
          sh "git clone ${appRepoURL}"
          repoName = sh(returnStdout: true, script: """echo \$(basename ${appRepoURL.trim()})""").trim()
          repoName=sh(returnStdout: true, script: """echo ${repoName} | sed 's/.git//g'""").trim()
          snykSecurity failOnIssues: false, projectName: '$BUILD_NUMBER', severity: 'high', snykInstallation: 'SnykSec', snykTokenId: 'snyk-token', targetFile: "${repoName}/pom.xml" 
          sh "rm -rf ${repoName}"
          sh "mkdir -p reports/snyk"
          sh "mv *.json *.html reports/snyk"
        }*/
        
        stage ('SAST')
        {
          // sonarqube
          environment {
             scannerHome = tool 'SonarQubeScanner' 
          }
          
          withSonarQubeEnv('sonarqube') {
            sh """${scannerHome}/bin/sonar-scanner -Dsonar.host.url=http://lab1.southcentralus.cloudapp.azure.com:9000 -Dsonar.login=admin -Dsonar.password=admin"""
          }
        }
        
        /*stage ('Container Image Scan')
        {
          try { 
              sh "mkdir -p Anchore-Engine/db"
              sh "sleep 20"
              sh "rm anchore_images || true"
              sh """ echo "$dockerImage" > anchore_images"""
              anchore 'anchore_images'
          }
          catch(error){
                   currentBuild.result = 'SUCCESS'
          }
        }
        
        stage ('DAST')
        {
          sh """
                  
                  export ARCHERY_HOST='http://127.0.0.1:8000'
                  export TARGET_URL=$targetURL
                  bash `pwd`/Archerysec-ZeD/zapscan.sh || true
             """
        }*/
}
       
