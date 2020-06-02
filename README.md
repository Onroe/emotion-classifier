# Emotion Recognizer
Real time Facial Emotion classification using Tensorflow js. The model is trained on fer2013 dataset using keras.
For each picture a chart is ploted showing scores of the different emotions and the dorminant emotion is the class emotion.
-PICTURE :- A pretrained keras model is loaded into the browser and used to detect faces and classify emotions.
-WEBCAM :-  Transfer learning is used to rapidly train and customize the model to this task for webcam pictures. 



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

####NOTE
- Make sure saved model is accessible over http as a json file:


-Check the URL where app is running - http://localhost:8080/picture.

![Screenshot](emotion.jpg)

-Check the URL where app is running - http://localhost:8080/index.

![Screenshot](screenshot.png)

