# cultural-rationalization
This repository stores the code used in the experiments for the cultural evolution and rationalization project. The project is primarily written in Python, Javascript, and HTML, and uses the Flask library to run the experiments. The main authors of this project are: Fiery Cushman, Danish Bajwa, and Linas Nasvytis.

## Experiment overview
The folder ```experiment1``` contains all the code needed to run the experiment that is specified in our preregistration form. Later versions of the experiment will be added to this repository as they are completed.

## Setup
To run this experiment, please start by installing the ```requirements.txt``` file. This can be done by running the following command in the command line terminal:

```pip install -r requirements.txt```

## Running the experiment
This experiment is built using Flask. In order to run it, please first navigate into the relevant folder (i.e. ```experiment1```), and use the following commands:

1. Set the ```FLASK_APP``` environment variable to ```main.py```. This can be done by running the following command in the terminal:

```export FLASK_APP=app.py```

2. Additionally, if you are running this application locally for testing purposes, please set the ```FLASK_ENV``` environment variable to ```development```. This can be done by running the following command in the terminal:

```export FLASK_ENV=development ```

3. Launch the Flask application. This can be done by running the following command in the terminal:

```flask run```

4. In the command line, you will now see a URL where the application is running. To access the application, please copy and paste the URL and **importantly, specify which generation you would like to play the game as by adding "/gen_number" at the end of the URL** Each generation has a separate URL, so that the experiment could be run sequentially. Generations are numbered from 0-7, with 0 being the initial generation. 

For example, to run the experiment for participants in generation 0, you would use the following URL:
http://sever_number:port_number/0

To run the experiment for participants in generation 1, you would use the following URL:
http://sever_number:port_number/1

Similar logic appplies for generations 2-7. 

As an example, if you are running the experiment locally, the URL for generation 1 could look like this: http://127.0.0.1:5000/1

Once there is sufficient player data from one generation (e.g. generation 0), participants in the subsequent generation (e.g. generation 1) will be automatically shown the tutorials of the 3 players with the highest scores from the previous generation. 

## Notes on potential errors
1. If you are running this application locally, we recommend you use a private session on your browser to avoid cookies, and launch each new session on a new broswer window. 

2. If you are facing any issues with data storage or saving, please see the ```db.py``` script. 