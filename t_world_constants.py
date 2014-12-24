import math
from enum import Enum

class t_world_messages(Enum):
  receive_substance = 1
  send_substance = 2

class t_world_dissipation_constants():
  lateral_dissipation = dissipation_base = 1.0
  diagonal_dissipation = (1.0 / (math.sqrt(2.0)))
