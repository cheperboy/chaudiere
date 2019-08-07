import subprocess
cmd = """ls -l /home/pi/Prod/db | awk '{ print $9 " " $5 }' """
stdout = subprocess.check_output(cmd, shell=True)
stdout = stdout.decode('utf-8')
ret = {}
for line in stdout.splitlines():
    line = line.split( )
    if len(line) > 0:
        size = "{:.0f}".format(int(line[1])/1000)
        size = str(size) + " Mo"
        ret[line[0]] = size
print (ret)
