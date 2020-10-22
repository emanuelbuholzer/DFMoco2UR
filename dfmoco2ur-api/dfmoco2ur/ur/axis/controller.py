import logging
from dfmoco2ur.ur.axis.xyzrxryrz_axis import XYZRxRyRzAxis


logger = logging.getLogger(__name__)


class AxisController():

    def __init__(self, config):
        self.config = config
        self.virtual_axis = {
            "xyzrxryrz": XYZRxRyRzAxis(config)
        }

    def get_num_axes(self):
        return self.axis.num_axes

    def set_axis(self, name = None):
        axis_name = name
        if name == None:
            axis_name = self.config.get("ur.axis")
        
        self.axis = self.virtual_axis.get(axis_name, False)
        
        if not self.axis:
            raise Exception(f"Unknown axis {axis_name}")

    def set_scale(self, scale):
        self.axis.set_scale(scale)

    def get_step_acc(self, kind, axis):
        if kind == "inch":
            return self.axis.get_inch_acc()[axis]
        elif kind == "jog":
            return self.axis.get_jog_acc()[axis]

    def scale_pos(self, pos, origin):
        return self.axis.scale_pos(pos, origin)

    def unscale_pos(self, pos, origin):
        return self.axis.unscale_pos(pos, origin)
    
