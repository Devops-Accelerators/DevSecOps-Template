properties ([
  parameters ([
    string(name: 'appRepoURL', value: "", description: "Application's git repository"),
    string(name: 'dockerImage', value: "", description: "docker Image with tag"),
    string(name: 'targetURL', value: "", description: "Web application's URL"),
    choice(name: 'appType', choices: ['Java', 'Node', 'Angular'], description: 'Type of application'),
    string(name: 'hostMachineName', value: "", description: "Hostname of the machine"),
    string(name: 'hostMachineIP', value: "", description: "Public IP of the host machine"),
    password(name: 'hostMachinePassword', value: "", description: "Password of the target machine")
    ])
])

def repoName="";
def app_type="";
def workspace="";

node {
        stage ('Checkout SCM') 
        {
	  catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
            checkout scm
            workspace = pwd ()
	  }
        }
  
        /*stage ('pre-build setup')
        {
	  catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
	      sh """
              docker-compose -f Sonarqube/sonar.yml up -d
              docker-compose -f Anchore-Engine/docker-compose.yaml up -d
	      docker-compose -f Infection-Monkey/docker-compose.yml up -d
              """
	  }
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
	    sh """
	      rm -rf Archerysec-ZeD/zap_result/owasp_report || true
	      docker run -v `pwd`/Archerysec-ZeD/zap_result:/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py \
    	      -t ${targetURL} -J owasp_report
	    """
          }
	}*/
	
	stage ('Inspec')
	{
  	  catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
	    
	     /*
	      RUN THIS COMMAND TO INSTALL INSPEC AS A PACKAGE IN RHEL/UBUNTU/MACOS
	      curl https://omnitruck.chef.io/install.sh | sudo bash -s -- -P inspec
	      */
	    sh """
	      rm inspec_results || true
	      inspec exec Inspec/hardening-test --suppress-warnings -t ssh://${hostMachineName}@${hostMachineIP} --password=${hostMachinePassword} --reporter json:./inspec_results 
	      cat inspec_results | jq
	    """
	  }	
	}
	
	/*stage ('Breach and Attack Simulation') {
	  catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
	      echo "https://lab1.southcentralus.cloudapp.azure.com:5000"
	      sh """
	       curl -O -k https://127.0.0.1:5000/api/monkey/download/monkey-linux-64
	       chmod +x monkey-linux-64
	       ./monkey-linux-64 m0nk3y -s 127.0.0.1:5000
	      """
	  }
	}*/
	
        stage ('Clean up')
        {
	  catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
            sh """
	      rm -r ${repoName} || true
	      mkdir -p reports/trufflehog
	      mkdir -p reports/snyk
	      mkdir -p reports/Anchore-Engine
	      mkdir -p reports/OWASP
	      mkdir -p reports/Inspec
              mv trufflehog reports/trufflehog
	      mv *.json *.html reports/snyk || true
	      cp -r /var/lib/jenkins/jobs/${JOB_NAME}/builds/${BUILD_NUMBER}/archive/Anchore*/*.json ./reports/Anchore-Engine ||  true
	      mv inspec_results reports/Inspec
            """
	   // cp Archerysec-ZeD/zap_result/owasp_report reports/OWASP/
		  
	    sh """
	    docker system prune -f
	    docker-compose -f Sonarqube/sonar.yml down
            docker-compose -f Anchore-Engine/docker-compose.yaml down -v
	    """
	  }
        }
}
       
