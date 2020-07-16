"""Example of the workflow with gridded anuga output data"""

import numpy as np
import particlerouting.particle_track as pt
from particlerouting.particle_track import params
from particlerouting.routines import get_state
import matplotlib.pyplot as plt

# load some variables from a deltarcm output so stage is varied
data = np.load('ex_anuga_data.npz')

# pull depth and stage from that data
depth = data['depth']
qx = data['qx']
qy = data['qy']

# create params and then assign the parameters
params = params()

# define the params variables
params.depth = depth
params.stage = depth  # using depth as standin for stage parameter
params.qx = qx
params.qy = qy

params.seed_xloc = list(range(20, 30))
params.seed_yloc = list(range(48, 53))
params.Np_tracer = 50
# smaller cell size than the other examples to tighten the range of
# travel time values that are obtained (aka increase travel time resolution)
params.dx = 10.
params.theta = 1.0
params.model = 'Anuga'

### Apply the parameters to run the particle routing model
particle = pt.Particle(params)
np.random.seed(0)
# run model until all particles have travelled for about 1.5 hours
walk_data = particle.run_iteration(target_time=2100)

x0, y0, t0 = get_state(walk_data, 0)
xi, yi, finaltimes = get_state(walk_data)

# print target travel time and list of the particle travel times
print('Prescribed target travel time: 2100 seconds')
print('List of particle travel times for final particle locations: ' +
      str(np.round(finaltimes)))

# make plot of initial and final particle locations
plt.figure(figsize=(4, 4), dpi=200)
plt.scatter(y0, x0, c='b', s=0.75)
plt.scatter(yi, xi, c='r', s=0.75)
plt.imshow(params.depth)
plt.title('Depth')
plt.colorbar()
plt.show()
