import os  
import sys

my_dir = os.path.dirname(sys.argv[0])
sys.stdout.write("In INIT")
sys.stdout.flush()
script_path = os.path.join(my_dir, 'setup.py')
print script_path
os.system(' %s %s %s' % (sys.executable, script_path, "install"))
