from robomation import *
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)


color_detection = ColorDetection(0)
color_detection.device('MJPEG')
color_detection.display(True)


