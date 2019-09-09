properties ([
  parameters ([
    string(name: 'appRepoURL', value: "", description: "Application's git repository"),
    string(name: 'dockerImage', value: "", description: "docker Image with tag"),
    string(name: 'targetURL', value: '', description: "Web application's URL"),
    choice(name: 'appType', choices: ['Java', 'Node', 'Angular'], description: 'Type of appliation')
    ])
])


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
	    /*removing archerysec
	      sh """
              export ARCHERY_HOST='http://127.0.0.1:8000'
              export TARGET_URL=$targetURL
              bash `pwd`/Archerysec-ZeD/zapscan.sh || true
            """*/
	    sh """
	      rm -rf Archerysec-ZeD/zap_result/owasp_report || true
	      docker run -v `pwd`/Archerysec-ZeD/zap_result:/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py \
    	      -t ${targetURL} -J owasp_report
	    """
          }
	}
  
        stage ('Clean up')
        {
	  catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
            sh """
	      rm -r ${repoName}
	      mkdir -p reports/trufflehog
              mv trufflehog reports/trufflehog
	      mkdir -p reports/snyk
	      mv *.json *.html reports/snyk
	      mkdir -p reports/Anchore-Engine
	      cp -r /var/lib/jenkins/jobs/${JOB_NAME}/builds/${BUILD_NUMBER}/archive/Anchore* ./reports/Anchore-Engine ||  true
	      mkdir -p reports/OWASP
	      cp  Archerysec-ZeD/zap_result/owasp_report reports/OWASP/
	      cp Archerysec-ZeD/zap_result/owasp_report reports/OWASP/
	      docker system prune -f
            """
	    //docker-compose -f Archerysec-ZeD/docker-compose.yml down
	    //docker-compose -f Sonarqube/sonar.yml down
            //docker-compose -f Anchore-Engine/docker-compose.yaml down
	  }
        }
}
       
