#!/usr/bin/env groovy

node ('master') {

    stage('build'){
        checkout scm
        sh '''
          source /opt/rh/python27/enable
          export X_SCLS="`scl enable python27 'echo $X_SCLS'`"
          virtualenv venv
          source venv/bin/activate
          pylint catalogclient -f parseable | tee pylint.out
        '''
    }

}