library 'reference-pipeline'
library 'AppServiceAccount'



pipeline{
    agent any
    
    /**  JOB JENKINS INPUT PARAMETERS  **/
    
	
	options {
        buildDiscarder(logRotator(numToKeepStr: '20'))
		// since the build is based on the branch the below variable should be set to true to avoid default checkout from master branch
		//  this causes GIT_* environment variable to be 'lost' and breaks the pcf deploy step -  skipDefaultCheckout true
    }
	
	
	/** Setting up the tools **/
    tools {
        jdk 'JAVA_8'
        maven 'Maven 3.3.9'
    }
	environment {
		/* SETUP PARAM*/
		IS_BOOLEAN = true
		PATH_TO_DEPLOY = "/opt/fedex/kycapp"
		GIT_BRANCH = ""
		//GIT_REPO_URL = ""
		GIT_REPO_URL = "git@gitlab.prod.fedex.com:APP3531572/india_kyc_microsite.git"
		
		HOST_URL1 = ''
        HOST_URL2 = ''
        
		// Eureka Server URL.
		EUREKA_SERVER_URL= ''
		
		DEV_URL1= "byculla.emea.fedex.com"
		DEV_URL2= "NA"
		ANGULAR_DEV= "dev"
		DEV_EUREKA_SERVER= "NA"
		
		TEST_URL1= "byculla.emea.fedex.com"
		TEST_URL2= "NA"
		//ANGULAR_DEV= "dev"
		TEST_EUREKA_SERVER= ""
		
		PREPROD_URL1= "byculla.emea.fedex.com"
		PREPROD_URL2= "NA"
		ANGULAR_PREPROD= "dev"
		PREPROD_EUREKA_SERVER= ""
		
		PROD_URL1= "byculla.emea.fedex.com"
		PROD_URL2= "NA"
		ANGULAR_PROD= "dev"
		PROD_EUREKA_SERVER= ""
		
		/*AUDIT_JAR_NAME = "kyc-audit-1.1.11-SNAPSHOT.jar"
		CONSIGNEE_JAR_NAME ="kyc-consignee-1.1.10-SNAPSHOT.jar"
		DMS_JAR_NAME = "kyc-dms-0.0.1-SNAPSHOT.jar"*/
		
		AUDIT_APP_GROUP =''
		AUDIT_APP_NAME =''//'kyc-audit'
		AUDIT_APP_VERSION =''
		
		CONSIGNEE_APP_GROUP =''
		CONSIGNEE_APP_NAME =''
		CONSIGNEE_APP_VERSION =''
		
		DMS_APP_GROUP =''
		DMS_APP_NAME =''
		DMS_APP_VERSION =''
		
		NEXUS_REPO = 'SNAPSHOT'
		APP_VERSION = ''
		APP_GROUP = ''
		
		AUDIT_JAR_PATH = "kyc_api/kyc-audit/target"
		CONSIGNEE_JAR_PATH ="kyc_api/kyc-consignee/target"
		DMS_JAR_PATH = "kyc_api/kyc-dms/target"
		
		AUDIT_PROFILE_PORT = "6741"
		CONSIGNEE_PROFILE_PORT ="6701"
		DMS_PROFILE_PORT = "6781"
		
		JAR_NAME = ""
		JAR_PATH = ""
		PROFILE =""
		PROFILE_PORT =""
		APP_NAME =''
		
		audit_pom =''
		consignee_pom=''
		dms_pom= ''
		
		EAI_NUMBER = "3531572"
		NEXUS_CREDS_ID = "3531572_Nexus_cred"
	}
	
	
	stages{
	
		stage('Environment'){
           steps{
                script {
					echo "Begining the environment"
					
					def audit_pom = readMavenPom file: "${WORKSPACE}/kyc_api/kyc-audit/pom.xml"		
					AUDIT_APP_GROUP = audit_pom.getGroupId()                
					AUDIT_APP_NAME = audit_pom.getArtifactId()	
					AUDIT_APP_VERSION = audit_pom.getVersion() 
					
					echo "Audit pom read done"
					
					def consignee_pom = readMavenPom file: "${WORKSPACE}/kyc_api/kyc-consignee/pom.xml"		
					CONSIGNEE_APP_GROUP = consignee_pom.getGroupId()                
					CONSIGNEE_APP_NAME = consignee_pom.getArtifactId()	
					CONSIGNEE_APP_VERSION = consignee_pom.getVersion() 
					
					def dms_pom = readMavenPom file: "${WORKSPACE}/kyc_api/kyc-dms/pom.xml"		
					DMS_APP_GROUP = dms_pom.getGroupId()                
					DMS_APP_NAME = dms_pom.getArtifactId()	
					DMS_APP_VERSION = dms_pom.getVersion() 
                    echo "DMS pom read done"
					
					RELEASE_TAG = "DEV_BUILD_OCT2020_KYC_DMS"
					
					
							JAR_PATH = DMS_JAR_PATH
							JAR_NAME = "${DMS_APP_NAME}-${DMS_APP_VERSION}.jar"
							PROFILE_PORT = DMS_PROFILE_PORT
							APP_VERSION= DMS_APP_VERSION
							APP_GROUP = DMS_APP_GROUP
							APP_NAME =DMS_APP_NAME
					
					
					

					echo "ASSIGNMENT DONE done"
					echo "JAR_NAME :: ${JAR_NAME}"
					
					GIT_BRANCH="*/${RELEASE_TAG}"
					HOST_URL1 = DEV_URL1
					HOST_URL2 = DEV_URL2
					EUREKA_SERVER_URL = DEV_EUREKA_SERVER
					PROFILE ="dev"
					DEPLOY_SERVICE ="KYC-AUDIT"
					DEPLOY_ENV = "DEV"
					
					echo "ENV :: ${DEPLOY_ENV}"
					echo "GIT_BRANCH :: ${GIT_BRANCH}"
					echo "SERVICE :: ${DEPLOY_SERVICE}"
                }
            }
        }
	
	
		stage('Checkout'){
				steps{
					checkout([$class: 'GitSCM', 
						branches: [[name: GIT_BRANCH]],
						doGenerateSubmoduleConfigurations: false,
						//extensions: [[$class:'WipeWorkspace'], [$class: 'SparseCheckoutPaths', sparseCheckoutPaths:[[$class:'SparseCheckoutPath', path:DEPLOY_SERVICE]]]],
						extensions: [[$class: 'CheckoutOption', timeout: 100],[$class: 'WipeWorkspace']],
						submoduleCfg: [],
						userRemoteConfigs: [[credentialsId: 'kycuser', url: GIT_REPO_URL]]])
				}
			}
			
		stage('Build'){
            steps {
				//mavenBuild("mvn clean install -s ${WORKSPACE}/CI/MavenSettings.xml -U -N -f ${WORKSPACE}/pom.xml -DskipTests");
				mavenBuild("mvn -s ${WORKSPACE}/kyc_api/kyc-audit/CI/MavenSettings.xml -f ${WORKSPACE}/kyc_api/pom.xml -Dmaven.test.skip=true -U clean install")
				//sh "cd ${WORKSPACE}}; pwd; ls";
				//sh "cd ${WORKSPACE}}; cd target; ls";
            }
        }
		
		stage('SonarQube analysis') {
            steps {
				echo "APP_NAME :: ${APP_NAME}"
				withSonarQubeEnv('SonarQube') {
					//configFileProvider([configFile(fileId: 'a6f6c28f-fbf4-4811-b4c7-a422d2691feb', variable: 'MAVEN_SETTINGS')]) {
                    sh 'mvn -s ${WORKSPACE}/kyc_api/kyc-audit/CI/MavenSettings.xml -f ${WORKSPACE}/kyc_api/pom.xml sonar:sonar'
					//}
				}
			}
        }
        /*stage('Quality Gate'){
		    steps {
				sonarQualityGate timeoutMinutes : 5
		    }
		}
		*/
		
		/*stage('nexus Upload') {
            steps {
                echo "Artifact Uploading..."
				nexusArtifactUploader artifacts: [[artifactId: "${APP_NAME}", classifier: '', file:"${WORKSPACE}/kyc_api/${APP_NAME}/target/${APP_NAME}-${APP_VERSION}-${NEXUS_REPO}.jar", type: 'jar']],
				credentialsId: "${NEXUS_CREDS_ID}",
				groupId: "eai${EAI_NUMBER}.${APP_GROUP}",
				nexusUrl: 'nexus.prod.cloud.fedex.com:8443/nexus',
				nexusVersion: 'nexus3',
				protocol: 'https',
				repository: "${NEXUS_REPO}",
				version: "${APP_VERSION}-${NEXUS_REPO}"
            }
        }*/
		
		stage('nexus Upload') {
            steps {
                echo "Artifact Uploading..."
				nexusStaging artifactId: "${APP_NAME}", tool: "maven", mavenSettings : "${WORKSPACE}/kyc_api/kyc-audit/CI/MavenSettings.xml -f ${WORKSPACE}/kyc_api/${APP_NAME}/pom.xml -N -U -DskipTests -DrepositoryId=snapshot", credentialsId: "${NEXUS_CREDS_ID}"
            }
        }
		
		
		stage('Kill Service'){
            steps {
			  script{
               sshagent(['kycuser']) {
                    sh "ssh -o StrictHostKeyChecking=no  kycuser@${HOST_URL1} uptime"
                    sh 'set +e'
                    //sh "ssh kycuser@${HOST_URL1} \"pkill -f ${DEPLOY_SERVICE}-${APP_VERSION}.jar\" || \"true\" "
					sh "ssh kycuser@${HOST_URL1} \"pkill -f ${JAR_NAME}\" || \"true\" "
                   
                }
                   if(HOST_URL2 == 'NA'){
                        echo 'Skipping deploy for instance 2 as URL is NA'
                    }
                    else{
                       sshagent(['kycuser']) {
                            sh "ssh -o StrictHostKeyChecking=no  kycuser@${HOST_URL2} uptime"
                            sh 'set +e'
                            sh "ssh kycuser@${HOST_URL2} \"pkill -f ${JAR_NAME}\" || \"true\" "
                        }
					}
				}
            }
        }
		
		/*stage('nexus Download') {
            steps {
                echo "Artifact Downloading..."
				downloadNexusArtifact groupId: "eai${EAI_NUMBER}.${APP_GROUP}",
				artifactId: "${AUDIT_APP_NAME}",
				repo: "${NEXUS_REPO}",
				release: true,
				extension: 'jar',
				version: "${APP_VERSION}-${NEXUS_REPO}",
				downloadFileName: "${AUDIT_APP_NAME}-${APP_VERSION}-${NEXUS_REPO}.jar"
            }
        }*/
		stage('nexus Download') {
            steps {
                echo "Artifact Downloading..."
				downloadNexusArtifact groupId:"${APP_GROUP}", artifactId:"${APP_NAME}", version:"${APP_VERSION}", release:false, repo:"snapshot", extension:"jar"
            }
        }
		
        stage('Deploy Artifact'){
            steps {
                sshagent(['kycuser']) {
                    sh "ssh -o StrictHostKeyChecking=no  kycuser@${HOST_URL1} uptime"
					//sh "scp -r ${WORKSPACE}/${DEPLOY_SERVICE}/target/kyc-audit-1.1.10-SNAPSHOT.jar kycuser@${HOST_URL1}:/opt/fedex/kycapp/"
					sh "scp -r ${JAR_PATH}/${JAR_NAME} kycuser@${HOST_URL1}:${PATH_TO_DEPLOY}/CICD/"
					sh "scp -r ${JAR_PATH}/${JAR_NAME} kycuser@${HOST_URL1}:${PATH_TO_DEPLOY}/"
                }
				script{
                    if(HOST_URL2 == 'NA'){
                        echo 'Skipping deploy for instance 2 as URL is NA'
                    }
                    else{
                        sshagent(['kycuser']) {
                            sh "ssh -o StrictHostKeyChecking=no  kycuser@${HOST_URL2} uptime"
                            //sh "scp -r ${WORKSPACE}/${DEPLOY_SERVICE}/target/kyc-audit-1.1.10-SNAPSHOT.jar kycuser@${HOST_URL2}:/opt/fedex/kycapp/"
							sh "scp -r ${JAR_PATH}/${JAR_NAME} kycuser@${HOST_URL2}:${PATH_TO_DEPLOY}/CICD/"
							sh "scp -r ${JAR_PATH}/${JAR_NAME} kycuser@${HOST_URL1}:${PATH_TO_DEPLOY}/"
                        }
                    }
                }
            }
        }
		stage('Start Instance'){
            steps {
			  script{
               sshagent(['kycuser']) {
                    sh "ssh -o StrictHostKeyChecking=no  kycuser@${HOST_URL1} uptime"
                    sh "set +e"
					//sh "ssh kycuser@${HOST_URL1} \"nohup /opt/java/hotspot/8/latest/bin/java ${JAVA_OPTS} -jar ${APPD_JAVA_OPTS} ${APPD_JAVA_MIN_OPTS} -Dspring.profiles.active=${DEPLOY_ENV} -Dvcap.application.instance_id=${DEPLOY_ENV.toUpperCase()}-1 -Deureka.server.uri=${EUREKA_SERVER_URL} /opt/fedex/rmsappuser/${DEPLOY_SERVICE}-${APP_VERSION}.jar > /dev/null  2>&1 &\" "
					sh "ssh kycuser@${HOST_URL1} \"nohup /opt/java/hotspot/8/64_bit/jdk1.8.0_261/bin/java -jar -Dspring.profiles.active=${PROFILE} -Dserverport=${PROFILE_PORT} ${PATH_TO_DEPLOY}/${JAR_NAME}> /${PROFILE}/null 2>&1 &\" "
					//sh "ssh kycuser@${HOST_URL1} \"nohup /opt/java/hotspot/8/64_bit/jdk1.8.0_261/bin/java -jar -Dlogging.config=http://acme-dev-config.emea.fedex.com:8888/kyc-audit/env/master/kyc-audit-logback.xml -Dserverport=6741 -Dspring.profiles.active=dev -Dspring.cloud.config.label=master -Dspring.cloud.config.uri=http://acme-dev-config.emea.fedex.com:8888/ -Dspring.cloud.config.username=acmeconfigserver -Dspring.cloud.config.password='AcmE!CoNfig'  kyc-audit-0.0.1-SNAPSHOT.jar> /dev/null 2>&1 &\" " 
				  }
				  
                   if(HOST_URL2 == 'NA'){
                        echo 'Skipping deploy for instance 2 as URL is NA'
                    }
                    else{
                       sshagent(['kycuser']) {
                            sh "ssh -o StrictHostKeyChecking=no  kycuser@${HOST_URL2} uptime"
                            sh 'set +e'
							//sh "ssh kycuser@${HOST_URL2} \"nohup /opt/java/hotspot/8/latest/bin/java ${JAVA_OPTS} -jar ${APPD_JAVA_OPTS} ${APPD_JAVA_MIN_OPTS} -Dspring.profiles.active=${DEPLOY_ENV} -Dvcap.application.instance_id=${DEPLOY_ENV.toUpperCase()}-2 -Deureka.server.uri=${EUREKA_SERVER_URL}   /opt/fedex/rmsappuser/${DEPLOY_SERVICE}-${APP_VERSION}.jar > /dev/null  2>&1 &\""
							//sh "ssh kycuser@${HOST_URL2} \"nohup /opt/java/hotspot/8/64_bit/jdk1.8.0_261/bin/java -jar -Dspring.profiles.active=dev -Dserverport=6741 kyc-audit-0.0.1-SNAPSHOT.jar> /dev/null 2>&1 &\" "
							sh "ssh kycuser@${HOST_URL2} \"nohup /opt/java/hotspot/8/64_bit/jdk1.8.0_261/bin/java -jar -Dspring.profiles.active=${PROFILE} -Dserverport=${PROFILE_PORT} ${JAR_NAME}> /${PROFILE}/null 2>&1 &\" "
						}
					}
				}
            }
        }
		
		
	}
}