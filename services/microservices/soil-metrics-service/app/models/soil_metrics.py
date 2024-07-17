class SoilMetric:
    def __init__(self, metric_id, farmer_id, ph, moisture, temperature, timestamp):
        self.metric_id = metric_id
        self.farmer_id = farmer_id
        self.ph = ph
        self.moisture = moisture
        self.temperature = temperature
        self.timestamp = timestamp
