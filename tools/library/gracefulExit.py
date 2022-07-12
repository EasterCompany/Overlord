import signal


class GracefulExit():

  def __init__(self):
    self.state = False
    signal.signal(signal.SIGINT, self.change_state)

  def change_state(self, signum, frame):
    print("\n\nAre you sure you want to exit? (Press Ctrl+C to exit now)\n")
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    self.state = True

  def exit(self):
    return self.state
