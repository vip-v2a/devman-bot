# Devman's checking telegrambot

The bot notifies you about checking your homework on the [devman](https://devman.org) website

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need create environment variables:
- `BOT_TOKEN` from @Bot_father
- `DEVMAN_TOKEN` from [devman.org](https://devman.org)
- `TELEGRAM_CHAT_ID` from @userinfobot (type command: "/start")

You need install `requirements.txt`
```    
pip install -r requirements.txt
```

## Features

- Repository has `.Procfile` to deploy on Heroku
- Logs are printed into chat with bot

## Running the tests

To test bot you need to submit your homework on devman website for review and then return it from the review.
For example, you show next message from bot:
![](https://github.com/vip-v2a/devman-bot/blob/1a6fcefe5e4b6d95b49381ca7b3f4674679a0363/ext/fast_test.png)

## Deployment

To deploy on [Heroku](https://heroku.com/): 
- create a new app on European server
- create Reveal Config Vars from 'Settings' tab:`BOT_TOKEN`, `DEVMAN_TOKEN`, `TELEGRAM_CHAT_ID` 
- open 'Deploy' tab on the top menu
- connect to your github profile
- select your bot repository
- choose a branch to deploy 'master' 
- press 'Deploy Branch'
- waiting 'Your app was successfully deployed'
- go to 'Recources' tab
- check worker is ON (if need, edit dino formation -> then switch ON dino app -> confirm)
- drink a cup of tea
