properties([disableConcurrentBuilds()])


pipeline {
    agent {
        label 'master'
        }

    options {
        buildDiscarder(logRotator(daysToKeepStr: '5', numToKeepStr: '10'))
        timestamps()
        }

    environment {
        ENV='test'
        JENKINS_USER_ID=sh(script: "id -u jenkins", returnStdout: true).trim()
    }

    stages {

        stage("API tests") {

            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    script {
                        env.NETWORK_NAME = UUID.randomUUID().toString()
                        env.RUN_CMD='pytest -m API -s -l -v -n=2 --alluredir allure-results'
                    }
                    sh 'echo "run API tests at network $NETWORK_NAME"'

                    sh 'docker network create $NETWORK_NAME'
                    sh 'docker compose -f final/docker-compose.yaml up --abort-on-container-exit'
                }
            }

            post {
              always {
                    sh 'docker network rm $NETWORK_NAME'
                    sh 'docker compose -f final/docker-compose.yaml down || true'
                }
            }
        }

        stage("UI tests") {

            steps {
                script {
                    env.NETWORK_NAME = UUID.randomUUID().toString()
                    env.RUN_CMD='pytest -m UI -s -l -v  --selenoid -n=2 --alluredir allure-results'
                }
                sh 'echo "run UI tests at network $NETWORK_NAME"'

                sh 'docker network create $NETWORK_NAME'
                sh 'docker compose -f final/docker-compose.yaml up --abort-on-container-exit'
            }

            post {
              always {
                    sh 'docker network rm $NETWORK_NAME'
                    sh 'docker compose -f final/docker-compose.yaml down || true'
                }
            }
        }

    }

    post {
        always {
            allure([
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'final/test_app/allure-results']]
            ])
            archiveArtifacts artifacts: 'final/test_app/.tmp/', allowEmptyArchive: true
            cleanWs()
        }
    }
}
