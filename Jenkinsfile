pipeline {
    agent any

    parameters {
        string(name: 'UPDATES', defaultValue: '', description: 'Pass environment variables in key=value format, separated by commas (e.g., key1=value1,key2=value2)')
        string(name: 'DEST_REPO_URL', defaultValue: '', description: 'Destination repository URL')
    }

    environment {
        // Fetch GitHub username and PAT using 'github-credentials'
        GITHUB_CREDENTIALS = credentials('github-credentials')
        GITHUB_USERNAME = credentails('github-username')
        GITHUB_PAT = credentials('github-pat)
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                // Cloning the Jenkins workspace to ensure the Python scripts are available
                checkout scm
            }
        }

        stage('Clone Repositories') {
            steps {
                script {
                    bat """
                        set GITHUB_USERNAME=${env.GITHUB_USERNAME}
                        set GITHUB_PAT=${env.GITHUB_PAT}
                        set DEST_REPO_URL=${params.DEST_REPO_URL}
                        python clone_repo.py
                    """
                }
            }
        }

        stage('Update YAML Files') {
            steps {
                script {
                    bat "set UPDATES=${params.UPDATES} && python update_yaml.py"
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
            cleanWs() 
        }
        failure {
            echo "Build failed!"
        }
    }
}
