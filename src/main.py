if __name__ == '__main__':
    pass




import class_db
reload(class_db)
from class_db import *

import class_os
reload(class_os)
from class_os import *

import top_level
reload(top_level)
from top_level import *

#============== Config ===============================

# For Lenovo
script_dir = "D:\\Works\\Dropbox\\Projects\\Cliks\\lenovo\\"
os_path = "os\\win7\\"
os_browser = "D:\\Clicks\\users\\browsers\\"
#os_browser = "D:\\Clicks\\users\\browsers\\"
#start_panel = Region(0,723,1366,45)
start_panel = Region(0,SCREEN.h-60,SCREEN.w,60)
speed_index = 1

# For Asus
"""
script_dir = "D:\\Works\\Dropbox\\Projects\\Cliks\\asus\\"
os_path = "os\\xp\\"
start_panel = Region(0,564,1024,36)
speed_index = 2
os_browser = "D:\\Clicks\\users\\browsers\\"
"""
#my_os.start_panel = Region(0,564,1024,36)
#==============End config ============================
Settings.OcrTextRead = True
log_dir = script_dir+"logs\\"
LOG_FILENAME=log_dir+"log.txt"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,filemode='w',format='%(asctime)s %(levelname)s %(message)s')
my_os=GanOs(script_dir+os_path)
my_os.start_panel = start_panel
#my_os.browsers_dir = os_browser
#my_browser = Browser(script_dir+"browser\\firefox\\")
#my_browser.page_load_time *=speed_index
Browser.image_path = script_dir+"browser\\firefox\\"
Browser.browsers_dir =  os_browser
Browser.page_load_time *=speed_index
BuxPage.time_to_exit *=speed_index
BuxPage.time_page_load = Browser.page_load_time



DB_excel = my_db()
ulist = DB_excel.get_users_list()

xs = "User sequence: "
for u in ulist:
    xs += " , "+str(u.login)
logging.debug(xs)


if checkIp(ulist) == False:
    
    print('Some ip is bad')
    logging.debug('Some ip is bad')
else:
    slist = getSitesList(script_dir,)
    try:
        rotateUsers(my_os,DB_excel,ulist,slist,log_dir)
        viewBySuperuser(my_os,DB_excel,slist,log_dir)
    except:
        logging.debug("Global error: "+saveError(log_dir))
    DB_excel.close() 
   
print "All finished"
    #DB_excel.close()

