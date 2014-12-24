try:
  import queue
except:
  import Queue
from t_world_constants import *

class t_square():
  
  def __init__(self, x, y, parent_queue, debug = False):
    self.substances = dict()
    self.x = x
    self.y = y

    self.incoming = None
    try:
      self.incoming = queue.Queue()
    except:
      self.incoming = Queue.Queue()
    self.parent_queue = parent_queue

    self.debug = debug


  def run_dissipation(self):
    
    dregs = []

    for substance in self.substances.keys():

      lateral_value = self.substances[substance].value * (self.substances[substance].dissipation_rate / 4.0) * (t_world_dissipation_constants.lateral_dissipation)
      diagonal_value = self.substances[substance].value * (self.substances[substance].dissipation_rate / 4.0) * (t_world_dissipation_constants.diagonal_dissipation)

      self.substances[substance].value -= (4.0 * lateral_value) + (4.0 * diagonal_value)
      #don't track to miniscule values
      #if self.substances[substance].value < self.substances[substance].min_value:
      #  dregs.append(substance)
      #  lateral_value += self.substances[substance].value / 4.0 #send diagonally, too, some time
      #send substance dissipation to adjacent squares
      lateral_substance = t_substance(self.substances[substance].identifier, lateral_value, self.substances[substance].min_value, self.substances[substance].max_value, self.substances[substance].dissipation_rate)
      diagonal_substance = t_substance(self.substances[substance].identifier, diagonal_value, self.substances[substance].min_value, self.substances[substance].max_value, self.substances[substance].dissipation_rate)
      self.parent_queue.put((t_world_messages.send_substance, self.y + 1, self.x, lateral_substance))
      self.parent_queue.put((t_world_messages.send_substance, self.y + 1, self.x + 1, diagonal_substance))
      self.parent_queue.put((t_world_messages.send_substance, self.y, self.x + 1, lateral_substance))
      self.parent_queue.put((t_world_messages.send_substance, self.y - 1, self.x + 1, diagonal_substance))
      self.parent_queue.put((t_world_messages.send_substance, self.y - 1, self.x, lateral_substance))
      self.parent_queue.put((t_world_messages.send_substance, self.y - 1, self.x - 1, diagonal_substance))
      self.parent_queue.put((t_world_messages.send_substance, self.y, self.x - 1, lateral_substance))
      self.parent_queue.put((t_world_messages.send_substance, self.y + 1, self.x - 1, diagonal_substance))

    for d in dregs:
      del self.substances[d]

  def receive_substance(self, substance):
    if not substance.identifier in self.substances:
      self.substances[substance.identifier] = substance
    else:
      self.substances[substance.identifier].value += substance.value
    

  
        

      
if "__main__" == __name__:
  
  from t_substance import *
  import random
  import numpy
  import matplotlib
  matplotlib.use('TkAgg')
  import matplotlib.pyplot as plt
  import matplotlib.animation as animation
  import time
  import sys

  world_width = int(sys.argv[1])
  world_height = int(sys.argv[2])

  squares = numpy.empty((world_width, world_height), dtype=numpy.object)

  mailbox = None
  try:
    mailbox = queue.Queue()
  except:
    mailbox = Queue.Queue()

  for x in range(world_width):
    for y in range(world_height):
      s1 = t_substance("calcium", random.randint(0, 100), 1, 30000, 0.1)
      t = t_square(x, y, mailbox, debug=True)
      t.receive_substance(s1)
      squares[x][y] = t

  ims = []
  fig = plt.figure()

  for i in range(int(sys.argv[3])):
    for t in squares.flat:
      t.run_dissipation()
    while not mailbox.empty():
      message = mailbox.get()
      if (len(message) > 3) and (t_world_messages.send_substance == message[0]):
        x = message[1]
        y = message[2]
        if x >= world_width:
          x -= world_width
        if y >= world_height:
          y -= world_height
        try:
          squares[x][y].receive_substance(message[3])
        except:
          print(message)

    grid = [[0 for x in range(world_width)] for y in range(world_height)]#numpy.empty((world_width, world_height))
    for t in squares.flat:
      for s in t.substances:
        grid[t.x][t.y] = float(t.substances[s].value)

    im = plt.imshow(grid, interpolation='sinc')
    ims.append([im])

  ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
  ani.save("%d.mp4" % int(time.time()))
  plt.show()

