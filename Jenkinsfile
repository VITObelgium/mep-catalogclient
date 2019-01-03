#!/usr/bin/env groovy

def deployable_branches = ["master"]

node("jenkinsslave1.vgt.vito.be"){

    stage("build-test"){
        checkout scm

        sh '''
          source /opt/rh/python27/enable
          export X_SCLS="`scl enable python27 'echo $X_SCLS'`"
          virtualenv venv
          source venv/bin/activate
          pip install -I --upgrade pip setuptools wheel==0.30.0
          pip install --upgrade pytest pylint
          pip install nose2 requests
          venv/bin/pylint catalogclient -f parseable | tee pylint.out
          python setup.py install
          venv/bin/nose2 --plugin nose2.plugins.junitxml --junit-xml
        '''
        sh '''
          source /opt/rh/rh-python35/enable
          source /etc/profile.d/pyspark.sh          
          virtualenv venv35
          source venv35/bin/activate
          pip install -I --upgrade pip setuptools wheel==0.30.0
          pip install nose2 requests          
          python setup.py install
          venv35/bin/nose2 --plugin nose2.plugins.junitxml --junit-xml
        '''
        // publish unit test results
        junit '**/nose2-junit.xml'
        // publish pylint warnings
        step([$class: 'WarningsPublisher', consoleParsers: [[parserName: 'PyLint']]])
    }

    if(deployable_branches.contains(env.BRANCH_NAME)){

        stage("deploy"){
          // ask confirmation before deployment to PyPi
          input 'Deploy to PyPi?'
          sh("python setup.py sdist upload -r public")
          // retrieve version from setup.py file
          version = sh(
            script: "python setup.py --version",
            returnStdout: true
          ).trim()
          // tag the release in Git
          // make sure ssh agent is running
          sshagent(['3b18ac8a-ef5a-44d7-81d0-71e51b9d0d5b']) {
            sh("git tag -a v${version} -m 'version ${version}'")
            sh("git push origin v${version}")
          }
        }

    }

}
