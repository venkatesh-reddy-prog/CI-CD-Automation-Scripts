pipeline {
    agent any

    parameters {
        string(name: 'dest_repo_url', defaultValue: 'https://github.com/venkatesh-reddy-prog/Demo1-Folder', description: 'Destination repository URL')
        string(name: 'updates', defaultValue: 'tokenurl=Nithin', description: 'Environment variables in key=value format')
    }
    stages {
        stage('Checkout Source Code') {
            steps {
                checkout scm
            }
        }

        stage('Clone Repositories') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-credentials', usernameVariable: 'GITHUB_USERNAME', passwordVariable: 'GITHUB_PAT')]) {
                    bat """
                        set GITHUB_USERNAME=%GITHUB_USERNAME%
                        set GITHUB_PAT=%GITHUB_PAT%
                        set DEST_REPO_URL=${params.dest_repo_url}
                        python clone_repo.py
                    """
                }
            }
        }

        stage('Update YAML Files') {
            steps {
                script {
                    bat "set UPDATES=${params.updates} && python update_yaml.py"
                }
            }
        }

        stage('Push Changes') {
            steps {
                script {
                    dir("${env.WORKSPACE}\\Clone_Repo\\Demo1-Folder") {
                        bat """
                        git config user.email "bvenkateshreddy87@gmail.com"
                        git config user.name "venkatesh-reddy-prog"
                        git checkout -b main || git checkout main
                        git add -A  // Ensures all untracked files are included
                        git commit -m "Automated YAML updates" || echo "Nothing to commit"
                        git push origin main
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()  
        }
        failure {
            echo "Build failed!"
        }
    }
}
