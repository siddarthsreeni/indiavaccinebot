# India's Covid Whatsapp Bot Script


#Continuously run's every 50 seconds to check if there is a new center & capacity available for the pincodes you set.
This script only checks today & tomorrow for slots. Ofcourse you can read the script & change that to a week too.

## To get info in your whatsapp!

You need to get the apikey form the bot before using the API:

Add the phone number +34644204756 into your Phone Contacts. (Name it it as you wish, I say covid_bot)
Send this message "I allow callmebot to send me messages" to the new Contact created (using WhatsApp of course). Mind the spelling

Wait until you receive the message "API Activated for your phone number. Your APIKEY is 123123" from the bot. As this is still in beta testing, the activation can take up to 2 minutes.

Once you are done. replace it in the script!


## how to run?

Find your district id from the districts.json file & use the command below. The api_key can be retreived by following steps above

```
python3 vaccine.py <disctict_id> <phone_number_with_std> <api_key>
```

## Requirements?

Oh, ofcourse ensure you install requests

```
pip3 install requests
```

@credits to https://www.callmebot.com/ for their free usage of API's for the countries benefits & making our lives easier!
