pipeline {
    agent any

    parameters {
        string(name: 'DEST_REPO_URL', defaultValue: '', description: 'Destination Repository URL')
        string(name: 'UPDATES', defaultValue: '', description: 'Updates as key=value pairs (comma-separated)')
    }

    environment {
        GITHUB_PAT = credentials('github-pat') 
        GITHUB_USERNAME = 'venkatesh-reddy-prog' 
        GITHUB_EMAIL = 'bvenkateshreddy87@gmail.com' 
    }

    stages {
        stage('Clone Repositories') {
            steps {
                script {
                    bat 'python clone_repo.py'
                }
            }
        }

        stage('Update YAML Files') {
            steps {
                script {
                    env.UPDATES = params.UPDATES
                    bat 'python update_yaml.py'
                }
            }
        }

        stage('Commit Changes') {
            steps {
                script {
                    dir("${env.WORKSPACE}\\Clone_Repo\\Demo1-Folder") {
                        bat '''
                        git config user.name "%GITHUB_USERNAME%"
                        git config user.email "%GITHUB_EMAIL%"
                        git add .
                        git diff --cached --quiet || git commit -m "Update YAML files with modifications"
                        '''
                    }
                }
            }
        }

        stage('Push Changes') {
            steps {
                script {
                    dir("${env.WORKSPACE}\\Clone_Repo\\Demo1-Folder") {
                        bat '''
                        git remote set-url origin https://github.com/%GITHUB_USERNAME%:%GITHUB_PAT%@${params.DEST_REPO_URL}
                        git push origin main
                        '''
                    }
                }
            }
        }
    }
}
