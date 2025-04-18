import time
import psutil
import os 
from uptime import uptime
import smtplib
from humanfriendly import format_timespan
import logging
import asyncio
from dotenv import dotenv_values
 
"""
cpu usage
memory usage
disk usage
battery level
system uptime
"""

def checkCpu():
    return psutil.cpu_percent()

def checkMemory():
    memory =  psutil.virtual_memory()
     
    
    return memory.percent

def checkDiskUsage():

    return psutil.disk_usage("/").percent
    
def checkBatteryLevel():

    return psutil.sensors_battery().percent

def checkUptime():
    seconds=uptime()
    return format_timespan(seconds)


async def sendMail(message):
    try:
        my_secrets = dotenv_values(".env")
         
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email=my_secrets["email"]
        password=my_secrets["password"]
        s.login(email,password)
        reciever=my_secrets["reciever"]
        s.sendmail(email,reciever,message)
        s.quit()
    except Exception as e:
        print(f"Error Sending email:{e}")    






   


 

     




async def main():
   
    logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG) 
    while True:
        cpu=checkCpu()
        memory=checkMemory()
        disk=checkDiskUsage()
        battery=checkBatteryLevel()
        uptime=checkUptime()

        logging.info(f"cpu usage:{cpu}, memory usage:{memory}, disk usage:{disk}, battery percent:{battery}, uptime :{uptime}")
        if cpu>90:
            await sendMail("Cpu threshold reached please check it")
        
        if memory>95:
            await sendMail("Memory threshold reached please check it")
        
        if disk>95:
            await sendMail("disk threshold reached please check it")

        if battery<20:
            await sendMail("low power please plugg into power")   
        time.sleep(20)
         






if __name__=="__main__":
      asyncio.run(main())