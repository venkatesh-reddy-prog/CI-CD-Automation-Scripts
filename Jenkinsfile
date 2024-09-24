pipeline {
    agent any

    parameters {
        string(name: 'UPDATES', defaultValue: '', description: 'Update values for YAML files')
    }

    environment {
        DEST_REPO_URL = credentials('dest-repo-url')
        PYTHON_PATH = 'C:\\Users\\I751676\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    }

    stages {
        stage('Clone Repositories') {
            steps {
                script {
                    // Fetch GitHub credentials inside the script block
                    def githubCredentials = credentials('github-credentials')
                    env.GITHUB_USERNAME = githubCredentials.username
                    env.GITHUB_PAT = githubCredentials.password

                    bat "${env.PYTHON_PATH} clone_repo.py"
                }
            }
        }

        stage('Update YAML Files') {
            steps {
                script {
                    env.UPDATES = "${params.UPDATES}"
                    bat "${env.PYTHON_PATH} update_yaml.py"
                }
            }
        }

        stage('Push Changes') {
            steps {
                script {
                    dir("${env.WORKSPACE}\\Clone_Repo\\Demo1-Folder") {
                        withCredentials([usernamePassword(credentialsId: 'github-credentials', usernameVariable: 'GITHUB_USERNAME', passwordVariable: 'GITHUB_PAT')]) {
                            bat "git config user.name '${env.GITHUB_USERNAME}'"
                            bat "git config user.email 'your.email@example.com'" 

                            def changes = bat(script: 'git status --porcelain', returnStdout: true).trim()
                            if (changes) {
                                bat 'git add .'
                                bat "git commit -m 'Update YAML files based on environment variables'"
                                bat "git push https://${env.GITHUB_USERNAME}:${env.GITHUB_PAT}@${DEST_REPO_URL} main"
                            } else {
                                echo 'No changes to commit.'
                            }
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
