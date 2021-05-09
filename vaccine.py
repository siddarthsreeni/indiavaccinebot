
import requests
from datetime import date,timedelta,datetime
import os
import time
import sys

ageLimits=[18, 45] # for current age limits.    
district_id=str(sys.argv[1])

root_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+district_id
headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

phone_number = str(sys.argv[2]) #your phone where you want the info of available centre in the pincode
api_key = str(sys.argv[3]) #key obtained from callmebot.api 


def send_notification(message):
	try:
		requests.get("https://api.callmebot.com/whatsapp.php?phone="+phone_number+"&text="+message+"&apikey="+api_key)
	except Exception as e:
		print("failed for ", e)

def parse_op(result,ageLimits,url):
	centers = result['centers']
	output=[]
	for center in centers:
		sessions=center['sessions']
		if len(sessions)==0:
			continue
		for session in sessions:
			if session['available_capacity'] > 0:   
				res = {'name':center['name'],'block_name':center['address'],'age_limit':session['min_age_limit'],'vaccine_type':session['vaccine'],'date':session['date'],'available_capacity':session['available_capacity']}
				if res['age_limit'] in ageLimits:
					output.append(res)
					send_notification("Found+capacity")
					print("=============================================> availability found", res)
	return output




def call_api(url,headers,date,ageLimits):
	response={}
	try:
		response = requests.get(url, headers = headers)
		if response.status_code == 200:
			result = response.json()
			try:
				output = parse_op(result,ageLimits,url) 
			except:
				send("something+broke+could+be+vaccine+for+"+district_id)
			if(len(output)>0):
				print("==>API call success: date"+ date+ " OP:" ,output )
			else:
				print("Checking for district ", district_id ,"for ", date, " for groups ",ageLimits, " found: ", output, "availability")
		else:
			print("error .. in response")
			send_notification("error+from+api")	
	except:
		print("No internet")

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
			today = date.today()
			for i in range(1,8):
				datt=str(today + timedelta(days=i))
				datt=datt[8:] + "-" + datt[5:7] + "-" + datt[:4]
				url = root_url + "&date=" + datt
				call_api(url,headers,datt,ageLimits)
				time.sleep(10)   
		except Exception as e:  
			try:
				send_notification(e)
			except:
				print("failed")
