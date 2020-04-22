# Emotion Recognizer
Web based Flask &amp; Tensorflow application to identify emotions from webcam pictures.
Transfer learning is used to rapidly train and customize the model to this task. 



### Instructions
To get a copy of the project running on your local machine.

###  Prerequisites
- [Python 3.6+](https://www.python.org/)
- [Node.js](https://nodejs.org/) version 8.9 or above
- [Vue cli](https://cli.vuejs.org/guide/installation.html)
- [tensorflow.js](https://www.tensorflow.org/js)

### Setting up the project
First, clone this repository to your local machine:

```sh
$ git clone https://github.com/Onroe/emotion-classifier.git
```

### Running the App

####Extract the files 

- Using your python terminal, navigate into the - server folder:

```
$ pip install -r requirements.txt

```

- Finally run the app:
```
$ flask run

```

####Run the front end
-Open a new nodejs terminal window, then navigate to the client folder:

Install dependencies:
```
$npm install

```

Then run the app:

```
$ npm run serve

```

-Check the URL where app is running - http://localhost:8080/index.

![Screenshot](screenshot.png)

