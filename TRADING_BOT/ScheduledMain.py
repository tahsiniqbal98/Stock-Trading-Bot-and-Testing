import MainStockScreener
import schedule
import time

print("PROGRAM RUNNING")
def runSchedule():
    MainStockScreener.main()


schedule.every().monday.at("08:31").do(runSchedule)
schedule.every().monday.at("09:31").do(runSchedule)
schedule.every().monday.at("10:31").do(runSchedule)

schedule.every().tuesday.at("08:31").do(runSchedule)
schedule.every().tuesday.at("09:31").do(runSchedule)
schedule.every().tuesday.at("10:31").do(runSchedule)

schedule.every().wednesday.at("08:31").do(runSchedule)
schedule.every().wednesday.at("09:31").do(runSchedule)
schedule.every().wednesday.at("10:31").do(runSchedule)

schedule.every().thursday.at("08:31").do(runSchedule)
schedule.every().thursday.at("09:31").do(runSchedule)
schedule.every().thursday.at("10:31").do(runSchedule)

schedule.every().friday.at("08:31").do(runSchedule)
schedule.every().friday.at("09:31").do(runSchedule)
schedule.every().friday.at("10:31").do(runSchedule)

while True:
    schedule.run_pending()
    time.sleep(0.001)