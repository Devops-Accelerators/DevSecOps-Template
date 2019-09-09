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
	  mkdir -p Archerysec-Zed/zap_result
	  chmod 1000 Archerysec-Zed/zap_result
          """
	
        }
        
        stage ('Check secrets')
        {
	  catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
            sh """
            rm trufflehog || true
            docker run gesellix/trufflehog --json --regex ${appRepoURL} > trufflehog
            cat trufflehog
            """
	  
	    def truffle = readFile "trufflehog"
		   
	    if (truffle.length() == 0){
              echo "Good to go" 
            }
            else {
              echo "Warning! Secrets are committed into your git repository."
	      throw new Exception("Secrets might be committed into your git repo")
            }
	  }
        } 
        
	stage ('Source Composition Analysis')
        {
	   catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
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
		   
	    def snykFile = readFile "snyk_report.html"
	    if (snykFile.exists()) {
		throw new Exception("Vulnerable dependencies found!")    
	    }
	    else {
		echo "Please enter the app repo URL"
	    	currentBuild.Result = "FAILURE"
	    }
   	    
	  }
	}

        
        stage ('SAST')
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
	  }
        
        stage ('Container Image Scan')
        {
          catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
	    sh "rm anchore_images || true"
            sh """ echo "$dockerImage" > anchore_images"""
            anchore 'anchore_images'
	  }
        }
        
        stage ('DAST')
        {
          catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
	    /*sh """
              export ARCHERY_HOST='http://127.0.0.1:8000'
              export TARGET_URL=$targetURL
              bash `pwd`/Archerysec-ZeD/zapscan.sh || true
            """*/
	    sh """
	      
	      docker run -d -v $(pwd)/zap_result:/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py \
    	      -t http://www.dvwa.co.uk -J report_json
	    """
          }
	}
  
        stage ('Clean up')
        {
          sh """
	    rm -r ${repoName}
	    mkdir -p reports/trufflehog
            mv trufflehog reports/trufflehog
	    mkdir -p reports/snyk
	    mv *.json *.html reports/snyk
	    cp -r /var/lib/jenkins/jobs/${JOB_NAME}/builds/${BUILD_NUMBER}/archive/Anchore* ./reports/ ||  true
	    cp -r Archerysec-Zed/zap_result/ reports/
	    docker system prune -f
          """
	    //docker-compose -f Archerysec-ZeD/docker-compose.yml down
	    //docker-compose -f Sonarqube/sonar.yml down
            //docker-compose -f Anchore-Engine/docker-compose.yaml down
        }
}
       
