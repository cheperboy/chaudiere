# -*- coding: utf-8 -*-
import time, sys

# Print iterations progress
def print_bar(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    
    Example of call:
    items = 100
    for item in range(1, items+1):
        print_bar(item, items)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '¦' * filled_length + '-' * (bar_length - filled_length)

    print('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    #sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.flush()
        print ("\r\n")
        #sys.stdout.write("\r\n")

