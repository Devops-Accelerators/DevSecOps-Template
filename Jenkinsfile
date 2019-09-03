/*properties ([
  parameters([
    [$class: 'GlobalStringParameterDefinition', defaultValue: '', description: "git url of the application's repo", name: 'appRepoURL'],
    [$class: 'GlobalStringParameterDefinition', defaultValue: '', description: "name of the image", name: 'dockerImage'],
    [$class: 'GlobalStringParameterDefinition', defaultValue: '', description: "web application's url", name: 'targetURL']
  ])
])*/

def repoName="";
def app_type="";
def workspace="";

node {
        stage ('Checkout SCM') 
        {
          checkout scm
          workspace = pwd ()
          sh "ls -al" 
        }
  
        stage ('pre-build setup')
        {
          sh """
          docker-compose -f Sonarqube/sonar.yml up -d
          mkdir -p Anchore-Engine/db
          docker-compose -f Anchore-Engine/docker-compose.yaml up -d
          docker-compose -f Archerysec-ZeD/docker-compose.yml up -d
          """
        }
        
        stage ('Check secrets')
        {
	  catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
            sh """
            rm trufflehog || true
            docker run gesellix/trufflehog --json --regex ${appRepoURL} > trufflehog
            cat trufflehog
            mkdir -p reports/trufflehog
            mv trufflehog reports/trufflehog
            """
	  
	    def truffle = readFile "reports/trufflehog/trufflehog"
		   
	    if (truffle.length() == 0){
              echo "Good to go" 
            }
            else {
              echo "Warning! Secrets are committed into your git repository." 
            }
	  }
        } 
        
	stage ('Source Composition Analysis')
        {
	  catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
	    sh "git clone ${appRepoURL} || true" 
            repoName = sh(returnStdout: true, script: """echo \$(basename ${appRepoURL.trim()})""").trim()
            repoName=sh(returnStdout: true, script: """echo ${repoName} | sed 's/.git//g'""").trim()
	  
	    if (appType.equalsIgnoreCase("Java")) {
	      app_type = "pom.xml"	
	    }
	    else {
	      app_type = "package.json"
	      dir ("${repoName}") {
	        sh "npm install"
              }
	    }
	  
            snykSecurity failOnIssues: false, projectName: '$BUILD_NUMBER', severity: 'high', snykInstallation: 'SnykSec', snykTokenId: 'snyk-token', targetFile: "${repoName}/${app_type}" 
            sh "mkdir -p reports/snyk"
            sh "mv *.json *.html reports/snyk"
	  }
	}

        
        /*stage ('SAST')
        {
	  catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
	    if (appType.equalsIgnoreCase("Java")) {
	      withSonarQubeEnv('sonarqube') {
	        dir("${repoName}"){
	          sh "mvn clean package sonar:sonar"
	        }
	      }
	    
	    timeout(time: 1, unit: 'HOURS') {   
	      def qg = waitForQualityGate() 
	      if (qg.status != 'OK') {     
	        error "Pipeline aborted due to quality gate failure: ${qg.status}"    
	        }	
	      }
	     }
            }
	  }*/
        
        stage ('Container Image Scan')
        {
          catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
	    sh "rm anchore_images || true"
            sh """ echo "$dockerImage" > anchore_images"""
            anchore 'anchore_images'
	  }
        }
        
        /*stage ('DAST')
        {
          catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
	    sh """
              export ARCHERY_HOST='http://127.0.0.1:8000'
              export TARGET_URL=$targetURL
              bash `pwd`/Archerysec-ZeD/zapscan.sh || true
            """
          }
	}*/
  
        stage ('Clean up')
        {
          sh """
	    mkdir -p reports/Anchore-Engine
	    cp -r /var/lib/jenkins/jobs/${JOB_NAME}/builds/${BUILD_NUMBER}/archive/Anchore* ./reports/Anchore_engine ||  true
	    docker system prune -f
            docker-compose -f Sonarqube/sonar.yml down
            docker-compose -f Anchore-Engine/docker-compose.yaml down
            docker-compose -f Archerysec-ZeD/docker-compose.yml down
          """
        }
}
       
