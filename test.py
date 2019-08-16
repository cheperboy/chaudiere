"""
How to call a shell command from python script
"""

# import subprocess
from subprocess import Popen, PIPE, check_output, STDOUT

# Method 1 : retrieve stdout, stderr and return code separatly
print ("----Method 1----")
p = Popen(['ls', '-la'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate()
rc = p.returncode
output = output.decode('utf-8')
err = err.decode('utf-8')
print ("----OUTPUT----")
print (output)
print ("----ERR----")
print (err)
print ("----RC----")
print (rc)

# Method 2 : only retrieve stdout
print ("----Method 2----")
output = check_output("ls -la", shell=True).decode('utf-8')
print ("----OUTPUT----")
print (output)

# Method 3 : retrieve stdout and stderr in the same output variable
print ("----Method 3----")
output = check_output("ls -la", stderr=STDOUT, shell=True).decode('utf-8')
print ("----OUTPUT----")
print (output)

