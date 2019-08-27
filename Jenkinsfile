properties ([
  parameters([
    [$class: 'GlobalVariableStringParameterDefenition', defaultValue: '', description: "git url of the application's repo", name: 'appRepoURL'],
    [$class: 'GlobalVariableStringParameterDefinition', defaultValue: '', description: "name of the image", name: 'dockerImage'],
    [$class: 'GlobalVariableStringParameterDefinition', defaultValue: '', description: "web application's url", name: 'targetURL']
  ])
])

node {

        stage ('Checkout SCM') 
        {
          checkout scm
          workspace = pwd ()
          sh "ls -al" 
        }
        
        stage ('Check secrets')
        {
          sh "rm trufflehog || true"
          sh "docker run gesellix/trufflehog --json --regex ${appRepoURL} > trufflehog"
          sh "cat trufflehog"
        }
        
        stage ('Source Composition Analysis')
        {
          snykSecurity projectName: '${projectName}', severity: 'high', snykInstallation: 'SnykSec', snykTokenId: 'snyk-personal', targetFile: 'pom.xml'
        }
        
        stage ('SAST')
        {
          // sonarqube
        }
        
        stage ('Container Image Scan')
        {
          sh "rm anchore_images || true"
          sh """ echo "$dockerImage" > anchore_images"""
          anchore 'anchore_images'
        }
        
        stage ('DAST')
        {
          sh """
                  export ARCHERY_HOST='http://ipaddr:port'
                  export TARGET_URL=$targetURL
                  bash `pwd`/Archerysec-Zed/zapscan.sh || true
             """
        }
}
       
