"""Used to time long processes

!!! Example
    Use the context manager as follows

    ``` py
    with Timer(task_string):
        Do long process
    ```
"""

import time

class Timer:
    """Create a timer as a context manager

    Args:
        taskString (str): String describing the process
    """
    def __init__(self, taskString: str) -> None:
        # Create a Timer with a task name
        self.taskString = taskString

    def __enter__(self):
        # Start the timer running and print that this is a long running process
        print(f'{self.taskString}...')
        self.startTime = time.time()

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Get the time elapsed
        timeElapsed = time.time() - self.startTime

        # Output the time elapsed
        print(f'{self.taskString} took {timeElapsed:.2f} seconds')

if __name__ == '__main__':
    # Test the timer
    with Timer('Waiting'):
        time.sleep(2.449)
