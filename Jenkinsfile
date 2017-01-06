#!/usr/bin/env groovy

node ('master') {

    stage('build'){
        checkout scm
        sh 'source /opt/rh/python27/enable'
        sh 'export X_SCLS="`scl enable python27 'echo $X_SCLS'`"'
        sh 'virtualenv venv'
        sh 'source venv/bin/activate'
        sh 'pylint catalogclient -f parseable | tee pylint.out'
    }

}