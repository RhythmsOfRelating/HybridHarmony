from threading import current_thread, Thread
from collections import deque
import numpy as np
import logging

class OutputAnalysis:
    def __init__(self, analysis):
        self.logger = logging.getLogger(__name__)
        self.analysis = analysis
        self.buffer = analysis.output_buffer
        self.thread = None
        self.running = False

    def start(self):
        if self.thread:
            return False

        self.thread = Thread(target=self._update, daemon=True, name="Buffering")
        self.running = True
        self.thread.start()

        return True

    def stop(self):
        if not self.thread:
            return True

        self.running = False
        if current_thread() is not self.thread:
            self.thread.join()
        self.thread = None

        return True

    def _update(self):
        while self.running:
            try:
                data = self.buffer.process(0.3)
                self._calculate(data)
            except Exception as e:
                self.logger.warning("Error during analysis, skipped frame")
                self.logger.exception(e)

    def _calculate(self, data):
        # Make sure we have buffers to analyze
        sample = deque(data, maxlen=int(self.analysis.output_size*self.analysis.window_lag*6))  # 6 is estimated sampling rate for rvalues #TODO needs better code
        sample.reverse()
        sample = np.array(sample).reshape((-1, int(self.analysis.output_size)))
        trailing_timestamp = sample[0, int(self.analysis.output_size-1)]
        ind = next(x[0] for x in enumerate(sample[:,int(self.analysis.output_size-1)]) if x[1] < trailing_timestamp-3)
        # print('relative', trailing_timestamp)



