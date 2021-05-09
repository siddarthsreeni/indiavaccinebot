
import requests
from datetime import date,timedelta,datetime
import os
import time


ageLimits=[18, 45] # for current age limits.    
pincodeList=[k for k in range(682011,682039)] #edit here for your own pincode, a list duh!

root_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="
headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

phone_number = "+9194xxxxxxxx" #your phone where you want the info of available centre in the pincode
api_key = "xxxxxx" #key obtained from callmebot.api 


def send_notification(message):
    try:
        requests.get("https://api.callmebot.com/whatsapp.php?phone="+phone_number+"&text="+message+"&apikey="+apikey+)
    except Exception as e:
        print("failed for ", message)

def parse_op(result,ageLimits,pincode,url):
    centers = result['centers']
    output=[]
    for center in centers:
        sessions=center['sessions']
        if len(sessions)==0:
            continue
        for session in sessions:
            if(session['min_age_limit'] in ageLimits):
                print("Surprise: 18+ slot detected in pincode: Please add to list: " + str(pincode))

            if session['available_capacity'] > 0:   
                res = {'name':center['name'],'block_name':center['address'],'age_limit':session['min_age_limit'],'vaccine_type':session['vaccine'],'date':session['date'],'available_capacity':session['available_capacity']}
                if res['age_limit'] in ageLimits:
                    output.append(res)
                    send_notification(pincode + "+has+capacity")
                    if(res['vaccine_type']=="COVAXIN"):
                        print("=============================================> COVAXIN availability found", res)
    return output




def call_api(url,headers,date,ageLimits,pincode):
    response={}
    try:
        response = requests.get(url, headers = headers)
        print("Checking ",pincode,"for ", date, " for groups ",ageLimits, response.status_code, response.json())
    except:
        print("No internet")
    if response.status_code == 200:
        result = response.json()
        output = parse_op(result,ageLimits,pincode,url) 
        if(len(output)>0):
            print("==>API call success: date"+date+ " OP:" ,output )


if __name__ == '__main__':
    count = 0
    try:
        send_notification("started+script")
    except:
        print("failed to send restart")
    while True:
        count += 1
        if count % 30 == 0:
            send_notification("heartbeat..sorry") #sends a heartbeat indicating script is runnign for your mental satisfaction ever ~2.5 hours
        try:
            for pincode in pincodeList:
                today = date.today()
                for i in range(0,2):
                    datt=str(today + timedelta(days=i))
                    datt=datt[8:] + "-" + datt[5:7] + "-" + datt[:4]
                    url = root_url + str(pincode) + "&date=" + datt
                    call_api(url,headers,datt,ageLimits,pincode)
                    time.sleep(5)
            time.sleep(30)
        except Exception as e:  
            try:
                send_notification(e)
            except:
                print("failed")
