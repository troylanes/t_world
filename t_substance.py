
class t_substance():

  def __init__(self, identifier, initial_value, min_value, max_value, dissipation_rate):
    self.identifier = identifier
    self.min_value = min_value
    self.max_value = max_value
    self.dissipation_rate = dissipation_rate

    self.value = initial_value
