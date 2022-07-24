from threading import active_count, enumerate as threads
from logger.logger import Log


def wait_and_exit():

    Log.info(f"Currently working sub-threads: {active_count()}")

    for thread in threads():

        thread_name = thread.name

        if thread_name != "MainThread":
            Log.thread_less_info(f"Waiting for {thread_name}")
            thread.join(5)
            Log.thread_less_info(f"{thread_name} has finished executing...")
