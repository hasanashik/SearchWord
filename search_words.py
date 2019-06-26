
# coding: utf-8

# In[18]:
#all imports
import mmap
from inspect import getsourcefile
from os.path import abspath
import re
from subprocess import check_output
#function returns true if text found parameters 1st one file name, 2nd one text name
#import mmap
def search_str(file_name,searched_item):
    try:
        with open(file_name, 'rb', 0) as file,              mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(bytes(searched_item.encode())) != -1:
                return 1
            else:
                return 0
    except:
        print('Failed t0 open file:',file_name)


# In[19]:


def give_me_root():
    #from inspect import getsourcefile
    #from os.path import abspath
    #import re
    dir_path=abspath(getsourcefile(lambda:0))
    base_dir=re.findall('(.+)\\\\',dir_path)
    base_dir=base_dir[0]+'\\'
    #print('root directory=',base_dir)
    return base_dir


# In[20]:


#give_me_root()


# In[21]:


def give_file_list(directory):
    #from subprocess import check_output
    #import re
    msg='cd '+directory+'&dir'
    shell_output=check_output(msg, shell=True).decode()
    #print(shell_output)
    found_file_names=re.findall('[0-9]+\s([0-9A-Za-z-_]+[\.]\S+)\r',shell_output)
    #print('found_file_names=',found_file_names)
    return found_file_names
    


# In[22]:


#give_file_list(give_me_root())


# In[23]:


def give_dir_list(directory):
    #from subprocess import check_output
    #import re
    msg='cd '+directory+'&dir'
    shell_output=check_output(msg, shell=True).decode()
    #print(shell_output)
    found_directory_names=re.findall('<DIR>\s+([0-9A-Za-z]\S+.*-*.*)\r',shell_output)
    #print('found_directory_names=',found_directory_names)
    return found_directory_names


# In[24]:


#give_dir_list('D:\search_word_test\js')


# In[35]:


def give_me_result_of_one_directory(directories,root_dir,searched_item,location,count):
    
    for item in range(len(directories)):
        refined=root_dir+directories[item]+'\\'
        #print(refined)
        
        dir_list=give_dir_list(refined)
        #print('===',dir_list)
        if len(dir_list)>0:
            count,location=give_me_result_of_one_directory(dir_list,refined,searched_item,location,count)

        files=give_file_list(refined)
        #print(files)
    
        
        for item in range(len(files)):
            #print(files[item])
            refine_dir=refined+files[item]
            #print('searching in ======',refine_dir)
            r=search_str(refine_dir,searched_item)
            #print(r)
            if r==1:
                #print('success')
                count=count+1
                location.append(refine_dir)
            #else:
                #print('Not foind in',refine_dir)
                
    return count,location
    #print('found',count,' times', 'in',location)
    


# In[39]:


searched_item=input('enter word:')
if len(searched_item):
    #searched_item='f'

    directories=give_dir_list(give_me_root())
    root_dir=give_me_root()
    location=list()
    count=0
    count,location=give_me_result_of_one_directory(directories,root_dir,searched_item,location,count)

    files=give_file_list(root_dir)
    for item in range(len(files)):
        #print(files[item])
        refine_dir=root_dir+files[item]
        #print('searching in ======',refine_dir)
        r=search_str(refine_dir,searched_item)
        #print(r)
        if r==1:
            #print('success')
            count=count+1
            location.append(refine_dir)
        #else:
            #print('Not foind in',refine_dir)

    print('\n\n',searched_item,'--> appeared',count,' times', '')
    for item in range(len(location)):
        print(location[item])

    location=[]
    count=0
else:
    print('No word given')
print('\n\n-------------------------------------\n')
print('Created by hasanashik\n')
input('Press enter to exit')