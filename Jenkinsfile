pipeline {
    agent any
    parameters {
        string(name: 'UPDATES', defaultValue: ' ', description: 'Update values for YAML files')
    }

    environment {
        DEST_REPO_URL = credentials('dest-repo-url')
        PYTHON_PATH = 'C:\\Users\\I751676\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    }

    stages {
        stage('Clone Repositories') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'github-credentials', usernameVariable: 'GITHUB_USERNAME', passwordVariable: 'GITHUB_PAT')]) {
                        env.GITHUB_USERNAME = GITHUB_USERNAME
                        env.GITHUB_PAT = GITHUB_PAT
                        bat "${env.PYTHON_PATH} clone_repo.py"
                    }
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
                            bat "git config user.name ${GITHUB_USERNAME}"
                            bat "git config user.email 'bvenkateshreddy87@gmail.com'"

                            // Checkout the correct branch
                            bat "git checkout main"

                            // Print untracked files for debugging
                            def untrackedFiles = bat(script: 'git ls-files --others --exclude-standard', returnStdout: true).trim()
                            echo "Untracked files: ${untrackedFiles}"

                            // Check for changes
                            def changes = bat(script: 'git status --porcelain', returnStdout: true).trim()
                            if (changes) {
                                bat 'git add .'
                                bat 'git commit -m "Update YAML files based on environment variables"'
                                bat "git push https://${GITHUB_USERNAME}:${GITHUB_PAT}@${DEST_REPO_URL} main"
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
