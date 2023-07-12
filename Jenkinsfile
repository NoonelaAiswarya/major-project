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

  }
}