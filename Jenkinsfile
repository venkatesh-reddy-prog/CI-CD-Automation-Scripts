pipeline {
    agent any

    environment {
        GITHUB_USERNAME = credentials('github-username') 
        GITHUB_PAT = credentials('github-pat')
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                checkout scm
            }
        }

        stage('Clone Repositories') {
            steps {
                script {
                    bat """
                        set GITHUB_USERNAME=${env.GITHUB_USERNAME}
                        set GITHUB_PAT=${env.GITHUB_PAT}
                        set DEST_REPO_URL=https://github.com/venkatesh-reddy-prog/Demo1-Folder
                        python clone_repo.py
                    """
                }
            }
        }

        stage('Update YAML Files') {
            steps {
                script {
                    bat "set UPDATES=tokenurl=Meghana && python update_yaml.py"
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
                        git add .
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
            cleanWs()  // No need for 'node' block here
        }
        failure {
            echo "Build failed!"
        }
    }
}
