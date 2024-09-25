pipeline {
    agent any

    parameters {
        string(name: 'UPDATES', defaultValue: '', description: 'Pass environment variables in key=value format, separated by commas (e.g., key1=value1,key2=value2)')
        string(name: 'DEST_REPO_URL', defaultValue: '', description: 'Destination repository URL')
    }

    environment {
        // Use Jenkins' `usernamePassword` credentials to store both GitHub username and PAT
        GITHUB_CREDENTIALS = credentials('github-credentials') // This will store both username and password
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
                    // Pass the GitHub credentials (username and PAT) and DEST_REPO_URL to the clone_repo.py script
                    bat """
                        set GITHUB_USERNAME=${env.GITHUB_CREDENTIALS_USR}
                        set GITHUB_PAT=${env.GITHUB_CREDENTIALS_PSW}
                        set DEST_REPO_URL=${params.DEST_REPO_URL}
                        python clone_repo.py
                    """
                }
            }
        }

        stage('Update YAML Files') {
            steps {
                script {
                    // Pass the UPDATES parameter to the update_yaml.py script
                    bat "set UPDATES=${params.UPDATES} && python update_yaml.py"
                }
            }
        }

        stage('Push Changes') {
            steps {
                script {
                    dir("${env.WORKSPACE}\\Clone_Repo\\Demo1-Folder") {
                        // Configure Git credentials and commit changes on Windows
                        bat """
                        git config user.email "bvenkateshreddy87@gmail.com"
                        git config user.name "venkatesh-reddy-prog"
                        git add .
                        git commit -m "Automated YAML updates"
                        git push origin main
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up the workspace after the job execution
            bat 'rmdir /S /Q %WORKSPACE%' // Clean workspace on Windows
        }
        failure {
            // Notify in case of failure
            echo "Build failed!"
        }
    }
}
