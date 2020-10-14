from pymongo import MongoClient
import datetime
import qrcode
client=MongoClient()

def connection():
	
	client = MongoClient('')
	return client

def login(userid,password):
	
	conn = connection()
	mydatabase = conn['digigreen_hackathon']
	mycollection = mydatabase['users']
	cur=mycollection.find({'userid':userid,'password':password})
	if cur.count()==0:
		response={'status':False}
	else:
		response={'status':True,'username':cur[0]['username'],'usertype':cur[0]['usertype'],'key':cur[0]['key']}

	return response	

def addBatch(farmerId,cropdetails):

    conn = connection()
    mydatabase = conn['digigreen_hackathon']
    mycollection = mydatabase['Batch Details']
    dateString=datetime.datetime.now()
    cur=mycollection.find()
    len=cur.count()
    batchnumber=0
    print("---")
    for i in range(0,len):
        currentBatch=cur[i]['Batch_number']
        currentBatch=currentBatch.split("_")[1]
        currentBatch=int(currentBatch)
        if (currentBatch>batchnumber):
            batchnumber=currentBatch
    batchnumber=batchnumber+1
    batchString="BAT_"+str(batchnumber)
    print(batchString)
    find1={"Batch_number":batchString,"Farmer_id":farmerId,"Vegdetails":cropdetails,"date":dateString}
    cur=mycollection.insert_one(find1)
    qrString="Farmer :"+farmerId
    for each_crop in cropdetails:
        print(each_crop,each_crop.split(':')[0],each_crop.split(':')[1])
        qrString=qrString+"\n"+each_crop.split(':')[0]+" : "+each_crop.split(':')[1]
    print (qrString)
    img=qrcode.make(qrString)
    filename="static/agp_qrcodes/"+batchString+".png"
    img.save(filename)
    return {'batchNumber':batchString,'qrPath':'http://127.0.0.1:5000/'+filename}

def getFarmers():

    conn = connection()
    mydatabase = conn['digigreen_hackathon']
    mycollection = mydatabase['users']
    cur=mycollection.find({'usertype':'Farmer'})
    #if cur.count()==0:
    #   response={'status':False}
    #lse:
    len=cur.count()
    farmerlist=[]
    for i in range(0,len):
        #print({'farmerid':cur[i]['userid']})
        farmerlist.append(cur[i]['userid']) 
    return farmerlist


def gettestdetails(farmerid):

    conn = connection()
    mydatabase = conn['digigreen_hackathon']
    mycollection = mydatabase['soil_test']
    cur=mycollection.find({'farmerid':farmerid})
    if cur.count()==0:
        response={'status':False}
    else:
        response={'carbon':cur[0]['carbon'],'nitrogen':cur[0]['nitrogen'],'potassium':cur[0]['potassium'],'phosphorous':cur[0]['phosphorous'],'magnessium':cur[0]['magnessium']}    
    return response

def entertestdetails(farmerid,carbon,nitrogen,potassium,phosphorous,magnessium):

    conn = connection()
    mydatabase = conn['digigreen_hackathon']
    mycollection = mydatabase['soil_test']
    cur=mycollection.find({'farmerid':farmerid})
    if cur.count()==0:
        find={"farmerid":farmerid,"carbon":carbon,"nitrogen":nitrogen,"potassium":potassium,"phosphorous":phosphorous,"magnessium":magnessium}
        cur=mycollection.insert_one(find)
    else:
        find = {"farmerid":farmerid}
        change = {"$set": { "carbon":carbon,"nitrogen":nitrogen,"potassium":potassium,"phosphorous":phosphorous,"magnessium":magnessium}}
        cur=mycollection.update_one(find,change)
#login('RC_001','admin')
#cursor = mycollection.find()
#for i in cursor:
#	print(i)

def getBatchCrops(batchId):

    conn = connection()
    mydatabase = conn['digigreen_hackathon']
    mycollection = mydatabase['Batch Details']
    cur=mycollection.find({"Batch_number":batchId})
    vegDetails=cur[0]['Vegdetails']
    vegList=[]
    for each_detail in vegDetails:
        vegList.append(each_detail.split(':')[0])
    return vegList

def updateBatch(batchId,crop,farmerdamage):

    conn = connection()
    mydatabase = conn['digigreen_hackathon']
    mycollection = mydatabase['Batch Details']
    cur=mycollection.find({"Batch_number":batchId})
    vegDetails=cur[0]['Vegdetails']
    #print(vegDetails)
    for i in range(0,len(vegDetails)):
        if(vegDetails[i].split(':')[0]==crop):
            actualWeight=int(vegDetails[i].split(':')[1])
            farmerdamage=int(farmerdamage)
            finalWeight=actualWeight-farmerdamage
            vegDetails[i]=vegDetails[i].split(':')[0]+":"+vegDetails[i].split(':')[1]+":"+str(farmerdamage)+":"+str(finalWeight)
            break
    find=({"Batch_number":batchId})
    change={"$set": {"Vegdetails":vegDetails}}
    mycollection.update_one(find,change)
    qrstring="https://digitalgreen.herokuapp.com?fname=Tom&vname="+crop
    print(qrstring)
    img=qrcode.make(qrstring)
    filename="static/consumer_qrcodes/"+batchId+"_"+crop+".png"
    img.save(filename)
    return {'qrPath':'http://127.0.0.1:5000/'+filename}
    return 'ok'

def listAllBatch():

    conn = connection()
    mydatabase = conn['digigreen_hackathon']
    mycollection = mydatabase['Batch Details']
    cur=mycollection.find()
    len=cur.count()
    #if(len==0):
        #response={'status':False}
    #else:
    batchList=[]
    for i in range(0,len):
        #print({'Batch_number':cur[i]['Batch_number']})
        batchList.append(cur[i]['Batch_number'])
        #print(batchList)
    batchList=batchList[::-1]
    return batchList

def getBatchDetails(batchId):

    conn = connection()
    mydatabase = conn['digigreen_hackathon']
    mycollection = mydatabase['Batch Details']  
    cur=mycollection.find({"Batch_number":batchId})
    if cur.count()==0:
        response={"status":False}
    else:
        response={"status":True,"Batch_number":cur[0]["Batch_number"],"Farmer_id":cur[0]["Farmer_id"],"Vegdetails":cur[0]["Vegdetails"],"date":cur[0]["date"]}
    return response



def getBatchDate(farmerid):

    conn = connection()
    mydatabase = conn['digigreen_hackathon']
    mycollection = mydatabase['Batch Details']  
    cur=mycollection.find({"Farmer_id":farmerid})
    batchDateList=[]
    len=cur.count()
    for i in range(0,len):
        saleDate=cur[i]['date']
        saleDate=saleDate.strftime("%d-%b-%Y (%H:%M:%S)")
        batchDateList.append(saleDate)
    batchDateList=batchDateList[::-1]
    return batchDateList

def getDateBatchDetails(findDate):

    conn = connection()
    mydatabase = conn['digigreen_hackathon']
    mycollection = mydatabase['Batch Details']  
    mycollection1=mydatabase['users']
    cur=mycollection.find()
    length=cur.count()
    for i in range(0,length):
        saleDate=cur[i]["date"].strftime("%d-%b-%Y (%H:%M:%S)")
        if (saleDate==findDate):
            farmerid=cur[i]["Farmer_id"]
            cur1=mycollection1.find({"userid":farmerid})
            response={"status":True,"Batch_number":cur[i]["Batch_number"],"Farmer_Name":cur1[0]["username"],"Vegdetails":cur[i]["Vegdetails"],"date":cur[i]["date"]}
    return response