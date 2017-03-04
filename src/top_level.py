import class_site
reload(class_site)
from class_site import *

import class_browser
reload(class_browser)
from class_browser import *


import class_user
reload(class_user)
from class_user import *

import shutil
import os
import logging

def checkIp(userlist,bad_ip_list = []):
    ips = [] 
    for u in userlist:
        nuip =  u.getCurrentIp()
        if nuip == False:
            continue
        if nuip in bad_ip_list:
            return False
        if nuip in ips:
            return False
        else:
           ips.append(nuip)
    return True

def saveError(log_dir):
    error_inf = sys.exc_info()
    for inf in error_inf:
        if inf != None:
            logging.debug(inf)
    file_name = SCREEN.capture(SCREEN.x,SCREEN.y,SCREEN.w,SCREEN.h)
    shutil.copy(file_name,log_dir)
    return os.path.basename(log_dir+file_name)  
    

def getSitesList(script_dir):
    
    
    site1 = BuxSite("http://www.site1.com/",script_dir+"sites\\site1\\")
    site1.addButton(BuxSite.ADV_PAGE,"adv_page.png",0.97)
    site1.addButton(BuxSite.ADV_PAGE,"adv_page1.png",0.95)
    site1.addButton(BuxSite.VISIT,"visit.png",0.99,-220,0,5)
    site1.addButton(BuxSite.ADV_LOADED,"adv_loaded.png",0.7)
    site1.addButton(BuxSite.ADV_LOADED,"adv_loaded1.png",0.7)
    site1.addButton(BuxSite.LOGIN,"login.png")
    site1.addButton(BuxSite.LOGIN,"username.png",0.9,130,0)
    site1.addButton(BuxSite.LOGIN,"password.png",0.9,130,0)
    site1.addButton(BuxSite.LOGIN,"confirm_login.png",0.9)
    site1.addButton(BuxSite.BALANCE,"balance.png",0.90,-20,0)
    site1.addButton(BuxSite.BANNER,"banner.png",0.95)
    site1.addButton(BuxSite.ACCOUNT,"account.png",0.90)
    site1.addButton(BuxSite.CLOSE,"puzzle\\finish.png",0.6)
    site1.balance_len = 45
    site1.walk_method = BuxSite.SCROLL
    site1.oneLink = False
    site1.autoclose = False
    site1.oneScan = True;
    
    p = PuzzleFindPic(Region(418,68,306,55),site1.image_path+"puzzle\\")
    p.addButton(p.CLOSE,"finish.png",0.7)
    p.banner = Region(128,60,868,90)
    ptcsolution.puzzle = p
    
    site2  = BuxSite("http://www.site2.com",script_dir+"sites\\site2\\")
    site2.addButton(BuxSite.ADV_PAGE,"adv_page.png",0.97)
    site2.addButton(BuxSite.ADV_PAGE,"adv_page1.png",0.97)
    site2.addButton(BuxSite.VISIT,"visit.png",0.97,-230,0,5)
    site2.addButton(BuxSite.ADV_LOADED,"adv_loaded.png",0.7)
    site2.addButton(BuxSite.ACCOUNT,"account.png",0.90)
    site2.addButton(BuxSite.BANNER,"banner.png",0.95)
    site2.addButton(BuxSite.BALANCE,"balance.png",0.90)
    site2.addButton(BuxSite.LOGIN,"login.png")
    site2.addButton(BuxSite.LOGIN,"username.png",0.9,130,0)
    site2.addButton(BuxSite.LOGIN,"password.png",0.9,130,0)
    site2.addButton(BuxSite.LOGIN,"confirm_login.png",0.9)
    site2.addButton(BuxSite.CLOSE,"puzzle\\finish.png",0.7)
    
    site2.balance_len=45
    site2.autoclose = False
    site2.oneLink = False
    site2.oneScan = True;
    site2.walk_method = BuxSite.SCROLL
    
    p = PuzzleFindPic(Region(371,70,152,50),site2.image_path+"puzzle\\")
    p.addButton(p.CLOSE,"finish.png",0.7)
    p.banner = Region(200,60,300,90)
    site2.puzzle = p
   
    slist = [site1,site2]
    return slist


def viewSites(slist,user,my_browser,my_db,cur_ip,log_dir):
    print "Start view sites"
    for current_site in slist:
        try:
            print user.login + "  -- " + current_site.url
            if user.asseptSite(current_site.url):
                print "Accepted"
                logging.debug('User: '+user.login+" with ip:"+cur_ip+' watching site: '+current_site.url)
                #my_browser = Browser(user.login) 
                current_site.browser = my_browser 
                my_browser.openUrl(current_site.url)
                my_browser.waitForLoad()
                my_browser.refresh()
                my_browser.waitForLoad()
                login = current_site.isLogged()
                if login == False:
                    login = current_site.tryLogin(user.login,user.password)
                if login == False: 
                    logging.debug('User: '+user.login+" with ip:"+cur_ip+' cant login to: '+current_site.url)
                    logging.debug(saveError(log_dir))
                    my_browser.closeTab()
                    continue
                my_browser.waitForLoad()
                balance = current_site.getBalance()
                if balance != False:
                    logging.debug(" Start balance: "+str(balance))
                else:
                    logging.debug("Cant get balance : "+saveError(log_dir))
                current_site.goToAdvPage()
                cliks = 0
                click_bad = 0
                bad_seq = 0
                current_site.scans = 0
                while current_site.hasLinks():
                    tabs = my_browser.getTabsNum()
                    if current_site.goToNextLink() != False:
                        wait(4)
                        if my_browser.getTabsNum() != (tabs+1):
                            logging.debug('Page not opened  ')
                            continue
                        cliks += 1
                        res = current_site.viewLink()
                        if res == False:
                            click_bad += 1
                            bad_seq +=1
                        else:
                            bad_seq = 0
                        if res == False or current_site.autoclose == False:
                            my_browser.closeTab()
                        else:
                            my_browser.close_popups()
                        if bad_seq > 5:
                            logging.debug('Many bad clicks by : '+user.login+' on site: '+current_site.url+" Break.")
                            break
                        while my_browser.getTabsNum() > tabs :
                            print "Close bad tabs "+str(tabs) 
                            my_browser.closeTab()
                    else:
                        logging.debug('Some links cant be clicked  : '+current_site.url+" user "+user.login)
                        logging.debug(saveError(log_dir))
                        break
                logging.debug('User: '+user.login+" has : "+str(cliks)+' click on site: '+current_site.url+" unsucsessful cliks :" + str(click_bad))
                # Grid
                if current_site.grid != False:
                    logging.debug('Grid_start')
                    my_browser.openUrl(current_site.grid.url)
                    my_browser.waitForLoad()
                    if current_site.grid.getChances(my_browser) > 0:
                        logging.debug('Grid_chances'+str(current_site.grid.chances))
                        my_browser.scrollDown()
                        current_site.grid.start()
                        i = 0
                        while current_site.grid.hasAdds(my_browser):
                            current_site.grid.goToNextAdd()
                            res = current_site.viewLink()
                            if res == False or current_site.autoclose == False:
                                my_browser.closeTab()
                            else:
                                my_browser.close_popups()
                            if res == False:
                                break
                            i += 1
                        logging.debug('Grid_end ' + str(i) + "clicks")
                    my_browser.closeTab()
                    # Grid end        
                while current_site.hasAdds():
                    current_site.goToNextAdd()
                    if current_site.viewAdds() == False or current_site.autoclose == False :
                        my_browser.closeTab()
                    else:
                        my_browser.close_popups()
                
                if my_db != False :
                    my_db.updateVisitTime(user.login,user.asseptSite(current_site.url),balance)
                my_browser.closeTab()
            else:
                print "Site rejected by "+user.login 
        except:
            logging.debug('Site : '+current_site.url+" not procceed with "+user.login)
            logging.debug(saveError(log_dir))
                                    
def rotateUsers(my_os,my_db,ulist,slist,log_dir):
    for user in ulist:
        if len(user.sites) == 0:
            continue
        # prepare enviroment
        my_browser = Browser(user.login)
        my_browser.open()
        my_os.setEnglish()
        i = 0
        max_try = 10
        proxy_ip = False
        while i < max_try: 
            cur_ip = my_browser.getIp()
            if cur_ip == False and proxy_ip != False:
                print "Bad ip "+str(proxy_ip)
                logging.debug('ip '+str(proxy_ip)+'is not response')
                my_db.markIp(proxy_ip,'Dead')
                i = i + 1
            if not user.asseptIp(cur_ip) :
                logging.debug('Ip '+str(cur_ip)+' not assepted by '+user.login)
                user_ip = user.getIp(i)
                if user_ip == False:
                    clear_ip = my_db.getFreeIp(user.login)
                    if clear_ip == False:
                        print "Cant get free ip for "+user.login
                        logging.debug('No free ip found fo user'+user.login)
                        break
                    #test ip
                    user.addIp(clear_ip['ip'],clear_ip['port'])
                    if not my_db.bindIpToUser(clear_ip['ip'],user.login):
                        logging.debug('Cant bind ip :'+str(clear_ip['ip'])+' to user '+user.login)
                        print my_db.getUserIpList(user.login)
                        break
                    else:
                        logging.debug('Assigned new ip :'+str(clear_ip['ip'])+' for '+user.login)
                        user_ip = clear_ip
                print "Setup proxy"
                my_browser.proxy_on(user_ip['ip'],user_ip['port'])
                proxy_ip = user_ip['ip']
                continue
                # ip has switched
                # main execution
            viewSites(slist,user,my_browser,my_db,cur_ip,log_dir)
            break
        my_os.setEnglish()
        my_browser.close()
        wait(10)
        
def viewBySuperuser(my_os,my_db,slist,log_dir):
    # For my account
    gan4x4 =  User("name","password")
    my_browser = Browser(gan4x4.login) 
    my_browser.open()
    my_browser.focus()
    my_os.setEnglish()
    cip=my_browser.getIp()
    if  my_db.isIpExists(cip) or cip == False:
        logging.debug("Bad IP : "+str(cip))
    else:
        gan4x4.sites= ['site1.com','site2.com']
        gan4x4.addIp(cip,0)
        viewSites(slist,gan4x4,my_browser,False,cip,log_dir)
    





