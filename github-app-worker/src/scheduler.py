import schedule
import time
from tasks import update_all_users_data_task

# Define a job to run your task every hour
schedule.every().hour.do(update_all_users_data_task)

print("Worker starting")
update_all_users_data_task()

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(60)