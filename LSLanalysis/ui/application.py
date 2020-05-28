import urwid
import logging
from .streams import Stream

class Application:
  palette = [
    ('stream.progress', 'black', 'light red', 'bold'),
    ('stream.bar', 'white', 'dark gray', 'bold'),
    ('stream.title', 'white', 'dark blue', 'bold'),
    ('stream.box', 'black', 'white'),
  ]

  def __init__(self, discovery):
    self.logger = logging.getLogger(__name__)
    self.discovery = discovery
    self.listing = urwid.SimpleListWalker([])
    self.view = urwid.ListBox(self.listing)

  def start(self):
    self.loop = urwid.MainLoop(self.view, self.palette, unhandled_input=self.on_input)
    self.loop.set_alarm_in(0.1, self.update)
    self.loop.run()

  def update(self, loop, user_data):
    try:
      self.perform_update()
    except Exception as e:
      self.logger.exception(e, exc_info=True)
    finally:
      self.loop.set_alarm_in(1.0 / 30.0, self.update)
      self.loop.screen.clear()

  def perform_update(self):
    self.refresh()
    self.touch()

  def touch(self):
    for stream in self.listing:
      stream.update()

  def refresh(self):
    self.logger.debug("Refreshing device list")

    streams_visible = [stream.uid for stream in self.listing]
    streams_active = []
    streams_new = []

    for uid, stream in self.discovery.streams_by_uid.items():
      streams_active.append(uid)

      if not uid in streams_visible:
        streams_new.append(Stream(stream))

    # Double loops, but hey it works
    for uid in list(set(streams_visible) - set(streams_active)):
      for stream in self.listing:
        if stream.uid == uid:
          self.listing.remove(stream)

    for stream in streams_new:
      self.listing.append(stream)

  def on_input(self, key):
    if key in ('esc', 'q'):
      raise urwid.ExitMainLoop()
