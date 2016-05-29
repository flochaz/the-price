# How Much ?
[![Build Status](https://travis-ci.org/flochaz/the-price.svg?branch=master)](https://travis-ci.org/flochaz/the-price)
[![Coverage Status](https://coveralls.io/repos/github/flochaz/the-price/badge.svg?branch=master)](https://coveralls.io/github/flochaz/the-price?branch=master)


## Alexa Skills aspects

### Synopsis

An Alexa skill to finally get the answer to the simple question : How much it costs ?
Introduction of the skill enabling Alexa to let you know the price of anything you think about.

### Motivation

This project has been started through the live contest "Hey Alexa!" (The Amazon Alexa Skill Contest on [Hackster.io](https://www.hackster.io)).

Amazon is the leader of online retailing but the Alexa has not the ability yet to answer any question how much cost things (except the Amazon echo device itself).
The idea was as well to not only limits this search to product that you can find on Amazon but any kind of stuff a user may have in mind such as Tesla model S, Kobe Bryant newport beach house, travel to space, etc. by combining Amazon and Google Search.

### How to use

1. Enable the skill in the Amazon Skills Section at alexa.amazon.com.
2. Say "Alexa, How much is the tesla model 3" to your Amazon device that supports Alexa (Echo, FireOS, FireTV, etc.)
3. Alexa will prompt you the price found by my skill by first checking on Amazon and if nothing have been found it will then try other search engine (Google custom search for now).

Reading advice: [Getting started guide for the Alexa Skills Kit](https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/getting-started-guide)

### API: Examples of utterances to play with the skill:
```
  Alexa, How much is a kindle fire HD7
  Alexa, ask How much is a travel to space
```

### Command Line version
To facilitate testing and interaction, a really simple command line is as well available.
To install it you can simply:
```
git clone https://github.com/flochaz/the-price/
cd the-price
pip install .
(python2.7-venv)florians-MacBook-Air:the-price flochaz$ ask-the-price --help
Usage: ask-the-price [OPTIONS] ITEM

  Main function to get the price of an item from a specific shop. If no shop
  provided, default strategy will apply

Options:
  --shop TEXT  Narrow done the search to a specific shop
  --help       Show this message and exit.
```

## Technical apsects

### Current supported Search engine
* Amazon Productizing API
* Google Custom Search API

### Feedbacks
* I ran into some troubles mainly due to the fact that Amazon Produtizing API does not support IAM and Amazon Lambda does not support environment variables. These limitations forced me to leverage Amazon KMS Service to encrypt/decrypt credentials (for the good at the end).
* Packaging python for AWS Lambda was kind of a pain as well since I was relying on a lib called lxml which needs specific .so files compiled for Lambda runtime. So I had to spin up an AIM similar to amazon lambda to compile and extract lxml .so (that is the reason why you have this lxml folder into the repo).
* The lack of Alexa testing API complexify automated integration testing

### Unit Tests

Simply run tox in the project folder:
```
tox
```

### Acceptance Tests

WORK IN PROGRESS : Leveraging the hack proposed by Sam Machin (https://github.com/sammachin/AlexaPi) I am developing a Lib for Robot Framework to automate Acceptance tests

### Contribution

Pull requests are more than welcome!
Once merged, project is automatically build, packaged, and uploaded to the AWS Lambda.
Which will end up updating the Alexa Skill people play with in one click!

## License

MIT
