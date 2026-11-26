pipeline {
    agent { label 'linux-python' }
    options { skipDefaultCheckout(); disableConcurrentBuilds() }
    triggers { pollSCM('H/2 * * * *') }
    environment { DEPLOY_HOST = '192.168.56.104' }
    stages {
        stage('Checkout') { steps { deleteDir(); checkout scm } }
        stage('Dependencies') { steps { sh 'python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt' } }
        stage('Tests') {
            steps { sh '.venv/bin/python -m pytest -q --junitxml=results.xml' }
            post { always { junit 'results.xml' } }
        }
        stage('Package') {
            steps {
                sh 'mkdir -p dist && tar -czf dist/lifedays.tar.gz app.py calculator.py VERSION requirements.txt templates static'
                archiveArtifacts artifacts: 'dist/lifedays.tar.gz', fingerprint: true
            }
        }
        stage('Deploy') {
            steps {
                sshagent(credentials: ['deploy-ssh']) {
                    sh '''
                        scp -o BatchMode=yes dist/lifedays.tar.gz deploy@$DEPLOY_HOST:/opt/lifedays/incoming/$BUILD_NUMBER.tar.gz
                        ssh -o BatchMode=yes deploy@$DEPLOY_HOST bash -s -- "$BUILD_NUMBER" < scripts/deploy.sh
                    '''
                }
            }
        }
        stage('Smoke test') {
            steps { sh 'curl -fsS http://$DEPLOY_HOST/health && curl -fsS http://$DEPLOY_HOST/ | grep -q LifeDays' }
        }
    }
}
