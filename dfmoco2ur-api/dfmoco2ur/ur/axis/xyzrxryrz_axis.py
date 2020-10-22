import logging
import numpy as np

logger = logging.getLogger(__name__)


class XYZRxRyRzAxis():
    def __init__(self, config):
        self.config = config
        self.num_axes = 6
        self.scale = self.config.get('ur.axes.xyzrxryrz.scale')
        self.inch_acc = self.config.get('ur.axes.xyzrxryrz.inch_acc')
        self.jog_acc = self.config.get('ur.axes.xyzrxryrz.jog_acc')
    
    def set_scale(self, scale):
        self.scale = scale

    def get_inch_acc(self):
        return self.inch_acc

    def get_jog_acc(self):
        return self.jog_acc

    def scale_pos(self, pos, origin):
        scaled_pos = np.multiply(np.array(pos), self.scale)
        scaled_origin = np.multiply(origin, self.scale)
        return (scaled_pos - scaled_origin).astype(int)

    def unscale_pos(self, pos, origin):
        return (pos/self.scale)+ origin
        