#!/usr/bin/env groovy

def deployable_branches = ["master"]

node("master"){

    stage("build-test"){
        checkout scm
        sh '''
          source /opt/rh/python27/enable
          export X_SCLS="`scl enable python27 'echo $X_SCLS'`"
          virtualenv venv
          source venv/bin/activate
          pylint catalogclient -f parseable
          python setup.py install
          pip install nose2 requests
          venv/bin/nose2 --plugin nose2.plugins.junitxml --junit-xml
        '''
        // publish unit test results
        junit '**/nose2-junit.xml'
        // publish pylint warnings
        step([$class: 'WarningsPublisher', consoleParsers: [[parserName: 'PyLint']]])
    }

    if(deployable_branches.contains(env.BRANCH_NAME)) {

        stage("deploy"){
          input 'Deploy to PyPi?'
          sh '''
            python setup.py sdist upload -r local
          '''
        }

    }

}