import os

import org.sikuli.basics.SikuliXforJython
from sikuli import *
#from sikuli.Sikuli import *


import sikuli_extend
class BuxPage:
    time_page_load = 180
    time_to_exit = 90
    banner = Region(0,60,SCREEN.w,60)
    (VISIT,ADDS,CLOSE,NEXT,CONFIRM,ADV_PAGE,ADV_LOADED,LOGIN,ADV_PAGE_LOADED,BALANCE,CHANCES,ACCOUNT,BANNER) = (0,1,2,3,4,5,6,7,8,9,10,11,12)
    def __init__(self,im_p=""):
        self.buttons = {}
        self.image_path = im_p
    def addButton(self,name,image,sim=0.9,x=0,y=0,color = False):
        fname = self.image_path+image
        if not os.path.exists(fname):
            raise Exception("File : "+fname+" not found on disk")
        b = sikuli_extend.Pattern(self.image_path+image).similar(sim).targetOffset(x,y)
        b.setColorDiff(color)
        if name in self.buttons: 
            self.buttons[name].append(b)
        else:
            self.buttons[name] = [b]
    
class BuxSite(BuxPage):
    
#    visit_buttons = []
#    adds_buttons = []
#   confirm_button = False
#    close_buttons = []

#    exit_button = ""
#    next_button =""
#    (VISIT,ADDS,CLOSE,NEXT,CONFIRM,ADV_PAGE,ADV_LOADED,LOGIN) = (0,1,2,3,4,5,6,7)
    (REFRESH,SCROLL) = (0,1) 
    def __init__(self,url,im_p):
        BuxPage.__init__(self,im_p)
        #self.buttons = {}
        self.url = url
        self.canLogin = False
        #addImagePath(im_p)
        #self.image_path = im_p
        self.browser = False
        self.links = []
        self.adds = []
        #self.add_page = False
        self.page_load = False
        self.autoclose = False
        self.oneLink = False
        self.puzzle = False
        self.balance_len = 45
        self.walk_method = self.SCROLL
        self.grid = False
        self.oneScan = False
    def skipBanners(self):
         if self.BANNER in self.buttons:
             if exists(self.buttons[self.BANNER][0]): 
                 click(self.buttons[self.BANNER][0])
                 wait(1)
    def pageWalk(self,wait_for = False):
        #popup(self.walk_method)
        self.scans = 0
        if self.walk_method == self.REFRESH:
            self.browser.refresh(wait_for)
        else:
           if self.browser.scrollDown() == False:
               return False
        return True
    def  isLogged(self):
        wait(0.5)
        if exists(self.buttons[self.LOGIN][0]) == None and exists(self.buttons[self.ACCOUNT][0]): 
            return True
        if exists(self.buttons[self.LOGIN][0])  and exists(self.buttons[self.ACCOUNT][0]) == None: 
            return False
        raise Exception("Site not loaded properly")
    def tryLogin(self,name,pwd):
        if self.isLogged():
            return True
        if not (self.LOGIN in self.buttons):
            return False
        if len(self.buttons[self.LOGIN])< 4:
            return False
        #click(self.buttons[self.LOGIN][0])
        self.browser.clickLink(self.buttons[self.LOGIN][0],self.buttons[self.LOGIN][3])
        #self.browser.waitForLoad(self.buttons[self.LOGIN][3])
        click(self.buttons[self.LOGIN][1])
        keyDown(Key.CTRL)
        type("a")
        keyUp(Key.CTRL)
        paste(name)
        mouseMove(Env.getMouseLocation().offset(00,-60))
        click(Env.getMouseLocation())
        wait(0.5)
        click(self.buttons[self.LOGIN][2])
        click(self.buttons[self.LOGIN][2])
        wait(2)
        keyDown(Key.CTRL)
        type("a")
        keyUp(Key.CTRL)
        paste(pwd)
        wait(0.5)
        # Captcha 
        if len(self.buttons[self.LOGIN])> 4:
            s_code = self.getCaptcha()
            print s_code
            wait(0.5)
            click(self.buttons[self.LOGIN][5])
            keyDown(Key.CTRL)
            type("a")
            keyUp(Key.CTRL)
            paste(s_code)
            wait(0.1)
        click(self.buttons[self.LOGIN][3])
        waitVanish(self.buttons[self.LOGIN][0],self.time_page_load)
        self.browser.waitForLoad()
        return self.isLogged()
    def getCaptcha(self,label = False,w = 50,h =18,ln=-5):
        if label == False:
            label = self.buttons[self.LOGIN][4]
        l = find(label);
        #l.highlight(3)
        to = label.getTargetOffset();
        reg = Region(l.x+to.x,l.y+to.y,w,h)
        reg.highlight(3)
        t = reg.text()
        t = t[ln:]
        return t
        
    def goToAdvPage(self):
        self.skipBanners()
        if self.ADV_PAGE in self.buttons:
            for b in self.buttons[self.ADV_PAGE]:
                if exists(b) ==None:
                    return False
                click(b)
                self.browser.waitForLoad()
                if self.ADV_PAGE_LOADED in self.buttons:
                    wait(self.buttons[self.ADV_PAGE][0])
    def goToAddPage(self):
        if self.grid.url != False:
            self.browser.openUrl(self.grid.url)
    def hasAdds(self):
        if len(self.adds) > 0: 
            return True
        else:
            if not (self.ADDS in self.buttons):
                return False
            a = self.scanScreen(self.buttons[self.ADDS])
            if a == False:
                return False
            else:
                self.adds = a
                return True 
    def hasLinks(self):
        if len(self.links) > 0:
            #popup(str(self.links))
            return True
        #popup("Scan")
        x = self.scanScreen(self.buttons[self.VISIT])
        if x == False:
            return False
        else:
            self.links = x
            return True 
    def canUpdate(self):
        if self.oneScan == True and self.scans > 0:
            return False
        else:
            return True     
    def scanScreen(self,patt):
        if  self.walk_method == self.REFRESH and self.oneLink == True:
            self.pageWalk()
        l = False
        if  self.canUpdate() ==True:
            l = self.getLinks(patt)
        else:
            print "Cant update visit buttons"
        bad_try = 0
        while (l == False):
            if self.pageWalk() == False: 
                break
            l = self.getLinks(patt)
            if l != False:
                bad_try = 0
            else:
                bad_try +=1 
            if  self.walk_method == self.REFRESH and l == False: 
                break
            if  self.walk_method != self.REFRESH and bad_try > 10: 
                break
        return l;
    def getLinks(self,butt_list):
        self.scans = self.scans+1
        my_ad = []
        c = 0
        for butt in butt_list:
            try:
                if self.oneLink == True:
                    my_ad.append(sikuli_extend.find(butt))
                else:
                    #findAll(butt)
                    #my_ad.extend(list(getLastMatches()))
                    my_ad.extend(sikuli_extend.findAll(butt))
                    #popup(str(butt) + str(my_ad))
            except:
                c=c+1  
        #popup(str(my_ad))
        if (len(my_ad)) == 0:
                return False
        return my_ad
    def goToNextLink(self):
        res = True
        try:
            if len(self.links) == 0: 
                return False
            self.links[0].highlight(2)
            self.links[0].click()
            mouseMove(Location(0,0))
            if self.CONFIRM in self.buttons:
                fin=wait(self.buttons[self.CONFIRM][0],30)
                fin.click()
        except:
            res = False
        finally:
            self.links.pop(0)
            return res
    def goToNextAdd(self):
        if len(self.adds) == 0: 
           raise Exception("Adds list empty")
        self.adds[0].click()
        self.adds.pop(0)
    def Addpuzzle(self):
        ex = self.banner.wait(self.buttons[self.CLOSE][0],self.time_to_exit)
        nb = exists(self.buttons[self.NEXT][0])
        if nb :
            nb.click()
            mouseMove(Env.getMouseLocation().offset(0, 30)) 
            self.browser.close_popups()
            self.Addpuzzle()
        return ex
    def viewAdds(self):
        try:
            if self.page_load:
                wait(self.page_load,self.time_page_load)
            exit_bt = self.Addpuzzle()
            if exit_bt != False: 
                exit_bt.click()
                return True
            return False
        except:
            return False

    def viewLink(self):
        try:
            if self.ADV_LOADED in self.buttons:
                sikuli_extend.waitList(self.buttons[self.ADV_LOADED],self.time_page_load)
                #wait(self.buttons[self.ADV_LOADED][0],self.time_page_load)
            wait(0.5)
            self.browser.closeMessages()
            if self.puzzle != False:
                exit_bt = self.puzzle.execute()
            else:
                if self.CLOSE in self.buttons:
                    exit_bt = self.banner.wait(self.buttons[self.CLOSE][0],self.time_to_exit)
                else:
                    return True
            #popup(str(exit_bt))
            if exit_bt != False: 
                exit_bt.click()
                return True
            return False
        except:
#            popup("except")
            return False
    def getBalance(self):
        try:
            self.skipBanners()
            return self.browser.getDigits(self.buttons[self.BALANCE][0],self.balance_len);
        except:
            return False
class ad_page:
    url =''
    def __init__(self,url):
        self.url = url
class Puzzle(BuxPage):
    def doExit(self):
        #popup(str(self.buttons))
        if self.CLOSE in self.buttons:
            ex = self.banner.wait(self.buttons[self.CLOSE][0],self.time_to_exit)
            return ex
        else:
            #popup("bad")
            return False
    def execute(self):
        return self.doExit()
class FindPicByPattern(Puzzle):
    def __init__(self,pattern,target,im_p):
        Puzzle.__init__(self,im_p)
        self.pattern_place = pattern
        self.target_place = target
    def execute(self):
        litera = capture(self.pattern_place)
        self.target_place.click(litera) 
        mouseMove(Env.getMouseLocation().offset(00,-60))
        e = self.doExit()
#        if e != False:
#            e.highlight(4)
        return e

class PuzzleFindPic(Puzzle):
    def __init__(self,reg,im_p):
        self.reg = reg
        self.image_path = im_p
        self.patt_list = []
        self.buttons = {}
        i = 1
        fn = im_p + str(i)+".png"
        while os.path.exists(fn):
            p = Pattern(fn).similar(0.55)
            self.patt_list.append(p)
            i += 1;
            fn = im_p + str(i)+".png"
    def execute(self):
        #popup(str(self.patt_list))
        #self.reg.highlight(4)
        for g in self.patt_list:
            f = self.reg.exists(g)
            if f != None:
                f.click(g)
                f.highlight(2)
                wait(2)
                e = self.doExit()
                return e
        print "Puzzle not sloved"
        self.reg.click()
        return self.doExit()

class Grid(Puzzle):
    w = 600
    h = 400
    cell = 20
    max = 20
    def_chances = 20
    def __init__(self,left_bottom,im_p):
        Puzzle.__init__(self,im_p)
        self.click_count = 0
        self.left_bottom = left_bottom
        self.chances = self.def_chances
        self.url = False   
        self.x=False
        self.y=False
    def hasAdds(self,browser):
        #x = browser.getDigits(self.buttons[self.CHANCES][0])
        #if x != False and x > 0:
        #    return True
        #return False
        if self.click_count <  self.chances:
            return True
        else:
            return False
    def getChances(self,browser):
        try:
            self.chances = browser.getDigits(self.buttons[self.CHANCES][0])
        except:
            self.chances=self.def_chances
        finally:
            return self.chances
    def start(self,delta=0):
        self.click_count = 0
        if delta == 0:
            delta = (self.def_chances - self.chances)*self.cell
        if delta < 0:
            delta = 0
        mouseMove(Location(0,0))
        pat = Pattern(self.image_path+self.left_bottom).similar(0.8)
        start = wait(pat,5) 
        start.highlight(2)
        self.x=start.x
        self.y=start.y - delta
    def goToNextAdd(self):          
        if (self.x == False) or ( self.hasAdds == False):
            return False
        mouseMove(Location(0,0))
        start = wait(self.image_path+self.left_bottom,3)
        start.highlight(2)
        click(Location(self.x+10,self.y-10))
        self.x = self.x+self.cell
        if (self.x >=  start.x + self.w*self.cell):
            self.x = start.x
            self.y = self.y - self.cell
        self.click_count = self.click_count +1


