pipeline {
    agent any

    parameters {
        string(name: 'dest_repo_url', defaultValue: 'https://github.com/venkatesh-reddy-prog/Demo1-Folder', description: 'Destination repository URL')
        string(name: 'updates_str', defaultValue: 'tokenurl=Nithin', description: 'key=value format')
    }

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
                withCredentials([usernamePassword(credentialsId: 'github-credentials', usernameVariable: 'GITHUB_USERNAME', passwordVariable: 'GITHUB_PAT')]) {
                    script {
                        bat """
                            set DEST_REPO_URL=${params.dest_repo_url}
                            python clone_repo.py
                        """
                    }
                }
            }
        }

        stage('Update YAML Files') {
            steps {
                script {
                    bat """
                        set UPDATES=${params.updates_str}
                        python update_yaml.py
                    """
                }
            }
        }

        stage('Push Changes') {
            steps {
                script {
                    bat """
                        git config --global user.email "bvenkateshreddy87@gmail.com"
                        git config --global user.name "venkatesh-reddy-prog"
                        git checkout main || git checkout -b main
                        git pull origin main --rebase || echo "No changes to pull"
                        git add .
                        git commit -m "Automated YAML updates" || echo "Nothing to commit"
                        git push origin main
                    """
                }
            }
        }
    }
}
