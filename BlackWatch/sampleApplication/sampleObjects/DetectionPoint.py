class DetectionPoint(object):
    dpName = "unknown"
    description = "no description"

    def __init__(self, dpName, description):
        self.dpName = dpName
        self.description = description

    def makeDetectionPoint(dpName, description):
        detectionPoint = DetectionPoint(dpName, description)
        return detectionPoint
