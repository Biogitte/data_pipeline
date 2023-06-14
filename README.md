# Running the Airflow Docker container
1. Create the Docker image 

        docker build -t my_airflow:latest .

2. Initialize the Airflow Docker container by running database migrations and create the first user account. The created user account has the login `airflow` and the password `airflow`.

        docker-compose up airflow-init

3. Clean up the environment.

        docker-compose down --volumes --remove-orphans

4. Start the Docker container. The -d flag starts the Docker container in detached mode, allowing it to run in the background.

        docker-compose up -d

5. Check that the container is running (optional: Docker desktop)

        docker-compose ps

6. Now you can explore the Airflow DAGs on [http://0.0.0.0:8080](http://0.0.0.0:8080)

7. Optional: clean up the build cache if experiencing cache issues
      docker builder prune --filter type=exec.cachemount

# Changes

## Changes to the Docker image
        
        # Make changes in Dockerfile
        # Build Docker image
        docker build -t my_airflow:latest .
        # Re-build and run the Container
        docker-compose up --build

## Changes to docker-compose.yaml

        # Stop the container and clean the environment
        docker-compose down --volumes --remove-orphans
        # Make changes in docker-compose.yaml
        # Re-build and run the Container
        docker-compose up --build

Alternatively, you can restart the Airflow Docker container to apply the changes (without cleaning and re-building):

        # check container id
        docker ps
        # restart the container
        docker restart <container id>

## Changes to the code in /dags
Make changes in the code, and wait. The changes will be automatically deployed in the Docker container without the need to rebuild or restart the container.

# Working in the container

## Finding and review downloaded, preprocessed, or result data

1. Access the Docker container.

        # check Container ID
        docker ps
        # access the Docker container
        docker exec -it <container id> /bin/bash

3. Once inside the container, you can check the value of the `RAW_DIR`, `PROC_DIR`or `RESULTS_DIR` environment variable by running:
      
      echo $RAW_DIR

4. The output will display the path to the directory where the files were downloaded. You can navigate to that directory using the cd command and view the files using ls:
      cd $RAW_DIR
      ls

# Other useful snippets

* Check the dependencies installed in the Docker container: `docker exec <containerid> pip list`

