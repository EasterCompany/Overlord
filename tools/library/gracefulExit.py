import signal
from . import console


class GracefulExit():

  def __init__(self):
    self.state = False
    signal.signal(signal.SIGINT, self.change_state)

  def change_state(self, signum, frame):
    print("\n\n" +
      "Are you sure you want to exit? (Press Ctrl+C to confirm)\n" +
      "You can also use the 'exit' command\n"
    )
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    self.state = True

  def exit(self):
    return self.state
