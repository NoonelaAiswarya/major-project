pipeline {
  agent any
  stages {
    stage('Checkout code') {
      steps {
        git(url: 'https://github.com/NoonelaAiswarya/major-project', branch: 'main')
      }
    }

    stage('Installing dependencies') {
      steps {
        sh 'cd app && pip3 install -r requirements.txt'
      }
    }

    stage('Build') {
      steps {
        sh 'docker build -t aishyadav/project:latest /var/lib/jenkins/workspace/major-project_main/app'
      }
    }

  }
}