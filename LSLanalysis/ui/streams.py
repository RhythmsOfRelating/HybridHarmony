import urwid
import logging

class Stream(urwid.WidgetWrap):
  def __init__(self, stream):
    self.logger = logging.getLogger(__name__)
    self.uid = stream.uid
    self.stream = stream
    self.setup()

    urwid.WidgetWrap.__init__(self, self.view)

  def setup(self):
    self.title = urwid.Text(self.stream.uid, 'center')
    self.created_at = urwid.Text("Started at: N/A")
    self.updated_at = urwid.Text("Last updated at: N/A")
    self.buffer = urwid.ProgressBar('stream.bar', 'stream.progress', 0.0)
    self.view = urwid.Pile([
      urwid.AttrWrap(self.title, 'stream.title'),
      urwid.AttrWrap(
        urwid.Padding(
          urwid.Pile([
            urwid.Divider(),
            self.created_at,
            self.updated_at,
            urwid.Divider(),
            urwid.Text("Buffer Size"),
            self.buffer,
            urwid.Divider(),
          ]),
          left=2, right=2
        ),
        'stream.box'
      )
    ])

  def update(self):
    self.title.set_text(self.stream.uid)
    self.created_at.set_text("Started at: {}".format(self.stream.created_at))
    self.updated_at.set_text("Last updated at: {}".format(self.stream.updated_at))
    self.buffer.set_completion((len(self.stream.buffer) / self.stream.buffer.size) * 100)
