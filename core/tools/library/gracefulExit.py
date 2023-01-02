'''
  gracefulExit is used to handle the CLI exit signal.

  Author(s): Owen Easter & StackOverflow
'''
import signal
from core.library import console


class GracefulExit():

  def __init__(self):
    self.state = False
    signal.signal(signal.SIGINT, self.change_state)

  def change_state(self, signum, frame):
    warning = console.out(
      "\n\nAre you trying to exit the CLI? (Please use the 'exit' command instead)\n\n",
      "yellow",
      False,
      end=""
    )
    cursor = console.out(
      './o ',
      'green',
      False
    )
    return print(warning + cursor, end="")
    # signal.signal(signal.SIGINT, signal.SIG_DFL)
    # self.state = True

  def exit(self):
    return self.state
