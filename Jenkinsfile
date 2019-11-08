#!/usr/bin/env groovy

/*
    This Jenkinsfile uses the Jenkins shared library. (ssh://git@git.vito.local:7999/biggeo/jenkinslib.git)
    Information about the pythonPipeline method can be found in pythonPipeline.groovy
*/

@Library('lib')_

pythonPipeline {
  package_name = 'catalogclient'
  wipeout_workspace = true
  wheel_repo = 'python-packages-public'
  python_version = ['2.7','3.5','3.6']
}
