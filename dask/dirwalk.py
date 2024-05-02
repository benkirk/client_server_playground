#!/usr/bin/env python
# coding: utf-8

# ## Start Dask Client
# 
# Unlike for arrays and dataframes, you need the Dask client to use the Futures interface.  Additionally the client provides a dashboard which 
# is useful to gain insight on the computation.
# 
# The link to the dashboard will become visible when you create the client below.  We recommend having it open on one side of your screen while using your notebook on the other side.  This can take some effort to arrange your windows, but seeing them both at the same is very useful when learning.

# In[ ]:


from dask.distributed import Client, progress
client = Client(threads_per_worker=8, n_workers=1)
client


# In[ ]:


import os, sys, stat
import shutil

def process_directory(dirname):
    more_dirs = []
    # last-minute check for a race condition:
    if not os.path.exists(dirname):
        print('directory \'{}\' vanished'.format(dirname), file=sys.stderr)
        return more_dirs

    #print(dirname)

    try:
        for di in os.scandir(dirname):
            pathname = di.path
            statinfo = di.stat(follow_symlinks=False)
            #print(statinfo)
            
            # decode file type
            fmode = statinfo.st_mode

            if stat.S_ISDIR(fmode):
                #print('d: '+pathname)
                more_dirs.append(pathname)
            else:
                #print('f: '+pathname)
                pass
            
    except PermissionError as error:
        print('Cannot scan: {}'.format(error), file=sys.stderr)
        #raise
        
    return more_dirs

#def process_directories(list_of_dirs):
#    more_dirs = 
#    for d in list_of_dirs:


# In[ ]:


#client.cluster.scale(10)  # ask for ten 4-thread workers


# In[ ]:


#process_directory(os.getenv('HOME'))


# In[ ]:


get_ipython().run_cell_magic('time', '', "from dask.distributed import as_completed\n\nzs = []\nzs.append(client.submit(process_directory, os.getenv('HOME')))\nzs.append(client.submit(process_directory, '/usr/local'))\n\nseq = as_completed(zs,with_results=True)\n\nfor future,result in seq:\n    for d in result:\n        #print(d)\n        seq.add(client.submit(process_directory, d))\n")


# In[ ]:




