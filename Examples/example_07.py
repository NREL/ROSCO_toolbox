'''
----------- Example_07 --------------
Load saved turbine, tune controller, plot minimum pitch schedule
-------------------------------------

In this example:
  - Load a yaml file
  - Load a turbine from openfast
  - Tune a controller
  - Plot minimum pitch schedule
'''

# Python modules
import matplotlib.pyplot as plt 
import yaml, os
# ROSCO toolbox modules 
from ROSCO_toolbox import controller as ROSCO_controller
from ROSCO_toolbox import turbine as ROSCO_turbine
from ROSCO_toolbox import sim as ROSCO_sim

this_dir = os.path.dirname(__file__)
example_out_dir = os.path.join(this_dir,'examples_out')
if not os.path.isdir(example_out_dir):
  os.makedirs(example_out_dir)

# Load yaml file 
parameter_filename = os.path.join(this_dir,'NREL5MW_example.yaml')
inps = yaml.safe_load(open(parameter_filename))
path_params         = inps['path_params']
turbine_params      = inps['turbine_params']
controller_params   = inps['controller_params']

# Ensure minimum generator speed at 50 rpm (for example's sake), turn on peak shaving and cp-maximizing min pitch
controller_params['vs_minspd'] = 50
controller_params['PS_Mode'] = 3

# Instantiate turbine, controller, and file processing classes
turbine         = ROSCO_turbine.Turbine(turbine_params)
controller      = ROSCO_controller.Controller(controller_params)

# Load turbine data from OpenFAST and rotor performance text file
turbine.load_from_fast(path_params['FAST_InputFile'],path_params['FAST_directory'],dev_branch=True,rot_source='txt',txt_filename=path_params['rotor_performance_filename'])

# Tune controller 
controller.tune_controller(turbine)

# Plot minimum pitch schedule
plt.plot(controller.v, controller.pitch_op,label='Steady State Operation')
plt.plot(controller.v, controller.ps_min_bld_pitch, label='Minimum Pitch Schedule')
plt.legend()
plt.xlabel('Wind speed (m/s)')
plt.ylabel('Blade pitch (rad)')

if False:
  plt.show()
else:
  plt.savefig(os.path.join(example_out_dir,'07_MinPitch.png'))
