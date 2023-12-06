# cultural-rationalization
This repository stores the code used in the experiments for the cultural evolution and rationalization project. The project is primarily written in Python and Javascript, and uses the Flask framework to run the experiments.

## Setup
To run this experiment, please start by installing the ```requirements.txt``` file. This can be done by running the following command in the terminal:

```pip install -r requirements.txt```

## Running the experiment
This experiment is built using Flask. In order to run it, please use the following commands:

1. Set the ```FLASK_APP``` environment variable to ```main.py```. This can be done by running the following command in the terminal:

```export FLASK_APP=app.py```

2. Additionally, if you are running this application locally for testing purposes, please set the ```FLASK_ENV``` environment variable to ```development```. This can be done by running the following command in the terminal:

```export FLASK_ENV=development ```

3. Launch the Flask application. This can be done by running the following command in the terminal:

```flask run```

4. In the command line, you will now see a URL where the application is running. To access the application, please copy and paste the URL and **importantly, specify which generation you would like to play the game as by adding /gen_number at the end of the URL** Each generation has a separate URL, so that the experiment could be run sequentially. 

For example, to run the experiment for a participant in generation 1:
http://sever:port/1

For generation 2:
http://sever:port/2

And so on for generations 3-8. 

## Notes on potential errors
1. If you are running this application locally, we recommend you use a private session on your browser to avoid cookies, and launch each new session on a new broswer window. 

2. If you are facing any issues with data storage or saving, please see the ```db.py``` script. 

