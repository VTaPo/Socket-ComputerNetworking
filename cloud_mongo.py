from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
#Others libraries
from time import localtime, strftime
import requests
import ast
import schedule

def API():
  data=requests.get("https://api.apify.com/v2/key-value-stores/EaCBL1JNntjR3EakU/records/LATEST?disableRedirect=true").text
  data=ast.literal_eval(data)
  for item in data["overview"]:
    date=item["date"]
  return data,date
def uploadData(data,date,db):
  tm=strftime( "%H:%M:%S", localtime())
  # date=strftime("(%d-1)-%m-%Y", localtime())
  realDate=date+'-'+strftime("%Y", localtime())
  res=db.covids.find_one({"date":realDate})
  if(res):
      db.covids.update_one({'date':realDate},{"$set":{"data":data,"time":tm,"date":realDate}})
  else:
      db.covids.insert_one({"data":data,"time":tm,"date":realDate})
  print('done')
def crawling_data(minutes,db):
  data,date=API()
  uploadData(data,date,db)
  schedule.every(minutes).minutes.do(uploadData,data,date,db)
  while True:
      schedule.run_pending()


