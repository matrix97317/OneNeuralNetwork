
# Developer Manual

Hi, I'm glad you want to become a developer. The following tutorial will quickly guide you on how to develop.


### STEP 0. Build Docker

The following operations are based on your proficiency in using Docker. If you don't know how to do so, you can take a look here.
https://docs.docker.com/get-started/

If you have a docker image, you can skip this step. If you not, you can do the following commands one by one.

```
$ git clone https://github.com/matrix97317/OneNeuralNetwork.git
$ cd OneNeuralNetwork
$ cd dockers
$ docker buildx build --platform=linux/amd64 -t ONN:v1.0.0 -f .
$ docker images //you can look `ONN:v1.0.0`
```

### STEP 1. Clone Repo
If you have clone repo,you can skip it.

```
$ git clone https://github.com/matrix97317/OneNeuralNetwork.git
$ cd OneNeuralNetwork
$ git checkout -b <your_name>/<feature_name>
```

### STEP 2. Build Development Environment

```
$ cd OneNeuralNetwork
$ make dev
$ make pre-commit
```

### STEP 3. Develop Project

Now,you can develop this project.

### STEP 4. Add your unit test.

To ensure the robustness of the project, you must write unit tests.

### STEP 5. Upload your commit to your branch

Congratulations！

```
$ make test       // Verify Unit Test
$ make pre-commit // Verify Code Style & auto format your code.

$ git checkout -b <your_name>/<feature_name>
$ git add <modified_file_names> # Add the intended files to commit.
$ git commit -m "commit message"
$ git checkout main
$ git pull
$ git checkout -b <your_name>/<feature_name>
$ git merge main
$ git push
```
