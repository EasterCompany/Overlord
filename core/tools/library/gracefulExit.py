'''
  gracefulExit is used to handle the CLI exit signal.
'''
import signal
from .console import col


class GracefulExit():

  def __init__(self):
    self.state = False
    signal.signal(signal.SIGINT, self.change_state)

  def change_state(self, signum, frame):
    print("\n\nAre you trying to exit the CLI? (Please use the 'exit' command instead)\n")
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    self.state = True
    print(col('./o ', 'green'))

  def exit(self):
    return self.state
