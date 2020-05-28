import logging
import logging.config
import argparse

parser = argparse.ArgumentParser(description='Run LSL R value processing')
parser.add_argument('--discard-timestamps', dest='discard_timestamps', default=True, action='store_false', help='Use local timestamps instead of LSL packet timestamps')
parser.add_argument('--correct-timestamps', dest='correct_timestamps', default=False, action='store_true', help='Enable stream processing and correction (proc_ALL)')
args = parser.parse_args()

from acquisition import Discovery
from analysis import Analysis
from ui import Application

def main():
  logging.config.fileConfig('logging.conf')

  discovery = Discovery(
    discard_timestamps=args.discard_timestamps,
    correct_timestamps=args.correct_timestamps
  )

  analysis = Analysis(discovery)
  ui = Application(discovery)

  discovery.start()
  analysis.start()
  analysis._update()
  ui.start()

if '__main__' == __name__:
  try:
    main()
  except KeyboardInterrupt:
    pass
