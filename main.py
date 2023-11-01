import logging
from util import explore, explore_all, getUrlContent
import queue
import multiprocessing
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
import os, time
import redis_repository

logging.info("application is starting")

def process_task(task_id):

     next_url = redis_repository.queue_get("url_queue")

     while next_url is not None:
     
          links = explore_all(next_url)

          for link in links:
               redis_repository.queue_put("url_queue",link)

          next_url = redis_repository.queue_get("url_queue")
               
          #TODO: get the queue size 
          logging.info(f"TASK{task_id}: queue size: {1}, finished processing: {next_url}")
     logging.info(f"TASK{task_id} done")

def main():
    # Define the number of threads you want to run in parallel
     num = 4

     processes = []
     for i in range(num):
          process = multiprocessing.Process(target=process_task, args=(i,))
          processes.append(process)
          process.start()

    # Wait for all processes to complete
     for process in processes:
          process.join()

if __name__ == '__main__':
    main()