# Chef Inspec
Chef InSpec is a free and open-source framework for testing and auditing your applications and infrastructure. Chef InSpec works by comparing the actual state of your system with the desired state that you express in easy-to-read and easy-to-write Chef InSpec code. Chef InSpec detects violations and displays findings in the form of a report, but puts you in control of remediation.

# Pre-requisites

 - Need to have Chef Inspec on the host machine to run the test.
 - The Chef InSpec package is available for MacOS, RedHat, Ubuntu and Windows.
 ```
 curl https://omnitruck.chef.io/install.sh | sudo bash -s -- -P inspec
 ```
 
 # Getting started
 
  - Run the inspec profile on any target machine.
  -
  ```
  stage ('Inspec')
	{
	    sh """
	      inspec exec Inspec/hardening-test -t ssh://${hostMachineName}@${hostMachineIP} --password=${hostMachinePassword} --reporter         json:./inspec_results 
	    """
	}
  
  ```
