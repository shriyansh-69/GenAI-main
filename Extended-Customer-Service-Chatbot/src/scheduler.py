# This File Is Created For Automatically Updating The Data Of The Database 

# Importing Function
from apscheduler.schedulers.background import BackgroundScheduler
from src.lang_chain_helper import create_vector_db

scheduler = BackgroundScheduler()


def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(create_vector_db,"interval", hours = 1 )
        scheduler.start()
        print("Scheduler Started. Knowledge will update automatically. ")
    
    










