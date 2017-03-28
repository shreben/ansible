node("${env.SLAVE}") {
  withEnv(["PATH+MAVEN=${tool 'Maven_3.3.9'}/bin"]) {
  stage("Build"){
    /*
        Update file src/main/resources/build-info.txt with following details:
        - Build time
        - Build Machine Name
        - Build User Name
        - GIT URL: ${GIT_URL}
        - GIT Commit: ${GIT_COMMIT}
        - GIT Branch: ${GIT_BRANCH}

        Simple command to perform build is as follows:
        $ mvn clean package -DbuildNumber=$BUILD_NUMBER
    */
    checkout scm
    sh "echo build artefact"
    sh """echo "Build time: \$(date)\nBuild Machine Name: \$(hostname)\nBuild User Name: \$(whoami)\nGIT URL: \$(git config --get remote.origin.url)\nGIT Commit: \$(git log -1 --pretty=%B)\nGIT Branch: shreben" > src/main/resources/build-info.txt"""
    sh "mvn clean package -DbuildNumber=${BUILD_NUMBER}"
  }

  stage("Package"){
    /*
        use tar tool to package built war file into *.tar.gz package
    */
    sh "echo package artefact"
    sh """cd target
    tar -czf mnt-exam-${BUILD_NUMBER}.tar.gz mnt-exam.war"""

  }

  stage("Roll out Dev VM"){
    /*
        use ansible to create VM (with developed vagrant module)
    */
    /* env.ANSIBLE_CONFIG = '../playbooks/ansible.cfg' */
    sh "echo ansible-playbook createvm.yml ..."
    sh '''cd ansible/playbooks
        ansible-playbook createvm.yml'''
  }

  stage("Provision VM"){
    /*
        use ansible to provision VM
        Tomcat and nginx should be installed
    */
    sh "echo ansible-playbook provisionvm.yml ..."
    sh '''cd ansible/playbooks
        ansible-playbook provisionvm.yml'''
  }

  stage("Deploy Artefact"){
    /*
        use ansible to deploy artefact on VM (Tomcat)
        During the deployment you should create file: /var/lib/tomcat/webapps/deploy-info.txt
        Put following details into this file:
        - Deployment time
        - Deploy User
        - Deployment Job
    */
    sh "echo ansible-playbook deploy.yml -e artefact=... ..."
    sh '''cd ansible/playbooks
    tar -zxf ../../target/mnt-exam-${BUILD_NUMBER}.tar.gz
    ansible-playbook deploy.yml -e artefact=mnt-exam.war'''
  }

  stage("Test Artefact is deployed successfully"){
    /*
        use ansible to artefact on VM (Tomcat)
        During the deployment you should create file: /var/lib/tomcat/webapps/deploy-info.txt
        Put following details into this file:
        - Deployment time
        - Deploy User
        - Deployment Job
    */
    sh "echo ansible-playbook application_tests.yml -e artefact=... ..."
    sh '''
    cd ansible/playbooks
    ansible-playbook application_tests.yml
    '''

  }
  }
}

