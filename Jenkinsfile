pipeline {
  agent any
  stages {
    stage('检出') {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[name: env.GIT_BUILD_REF]],
          userRemoteConfigs: [[url: env.GIT_REPO_URL, credentialsId: env.CREDENTIALS_ID]]
        ])
      }
    }
    stage('部署到腾讯云存储') {
      steps {
        sh 'coscmd config -a $TENCENT_SECRET_ID -s $TENCENT_SECRET_KEY -b $TENCENT_COS_BUCKET -r $TENCENT_COS_REGION'
        sh 'rm -rf .git'
        sh 'ls -la'
        //sh 'tree'
        sh 'coscmd upload -r ./ /'
      }
    }
  }
}