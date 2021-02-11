print("Running testproject.py....")

import subprocess

subprocess.call(['python',"indicators.py"])
subprocess.call(['python',"TheoreticallyOptimalStrategy.py"])

def author():
	return 'Zliu723'

print("Complete runing testproject.py!")