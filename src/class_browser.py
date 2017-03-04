import org.sikuli.basics.SikuliXforJython
from sikuli import *
#from sikuli.Sikuli import *
class Browser:
    name = 'Firefox'
    image_path = ""
    page_load_time = 60
    debug = True
    browsers_dir = ""
    image_path =""
    #right_bar = Region(SCREEN.w-25,43,25,SCREEN.h-43*2)
    right_bar = Region(SCREEN.w-25,43,25,SCREEN.h-50)
    #right_bar_top =Region(SCREEN.w-25,SCREEN.h-43-51,25,51)
    bar_adress =Region(0,26,SCREEN.w,45)
    bar_tabs = Region(0,0,SCREEN.w,25)
    def __init__(self,code_p):
        #self.image_path = im_p
        self.code_dir = self.browsers_dir + code_p;  
        self.app = False
        self.icon = False
        #self.right_bar.highlight(6)
        #self.bar_adress.highlight(6)
    def open(self):
        #myApp = App(self.name)
        #if not myApp.window(): # no window(0) - Firefox not open
        #    App.open("c:\\Program Files\\Mozilla Firefox\\firefox.exe")
        #wait(2)
        #myApp.focus()
        #click(Pattern(self.image_path+"logo.png").targetOffset(0,14))
        self.app = App.open(self.code_dir+"\\FirefoxPortable.exe");
        self.icon = Pattern(self.image_path+"icon.png").similar(0.85)
        x = wait(self.icon,160)
        #x.highlight(6)
        #click(icon)
        #wait(self.image_path+"logo.png",60)
        #sleep(60)
        self.focus()
    def focus(self):
        #self.app.focus()
        #icon = Pattern(self.image_path+"icon.png").similar(0.7)
        #if exists(icon) != None:
        #    click(icon)
        logo =  Pattern(self.image_path+"Logo.png").targetOffset(0,14)
        wait(logo,30)
        click(logo)
    def openUrl(self,url):
        self.focus()
        keyDown(Key.CTRL)
        type("t")
        keyUp(Key.CTRL)
        wait(0.5)
        """
        click(Pattern(self.image_path+"logo.png").targetOffset(20,30))
        #type(Key.F6)
        #wait(2)
        wait(0.2)"""
        keyDown(Key.ALT)
        type("d")
        keyUp(Key.ALT)
        paste(url)
        #wait(0.2)
        print "URL "+url
        type(Key.ENTER)
        
    def getLink(self):
        return self.image_path+"lnk.png"
    def getLogo(self):
        return self.image_path+"logo.png"
    def copyText(self,x,y,length):
        mouseMove(Location(x,y))
        mouseDown(Button.LEFT)
        mouseMove(Location(x+length,y))
        mouseUp(Button.LEFT)
        keyDown(Key.CTRL)
        type("c")
        keyUp(Key.CTRL)
        st = str(Env.getClipboard())
        if len(st) == 0:
            return False
        return st
    def getIp(self):
        try:
            #self.openUrl("http://myip.ru")
            self.openUrl("http://www.ip-ping.ru/")
            #self.refresh()
            #self.refresh()
            ip_ban = self.image_path+"ip_banner.png"
            self.waitForLoad(ip_ban)
            ban1 = Pattern(ip_ban)
            ban = wait(ban1,60)
            mouseMove(Location(ban.x+10,ban.y+ban.h+20))
            mouseDown(Button.LEFT)
            mouseMove(Location(ban.x+ban.w-10,ban.y+ban.h+20))
            mouseUp(Button.LEFT)
            keyDown(Key.CTRL)
            type("c")
            keyUp(Key.CTRL)
            return Env.getClipboard()
        except:
            return False
    def getTabsNum(self):
        #self.bar_tabs.highlight(4)
        pat = Pattern(self.image_path+"cross.png").similar(0.8)
        try:
            tabs = list(self.bar_tabs.findAll(pat))
            return len(tabs)
        except:
            if exists(self.image_path+"Logo.png") !=None:
                return 1
            else:
                return 0
    def closeTab(self):
        keyDown(Key.CTRL)
        type("w")
        keyUp(Key.CTRL)
        self.close_popups()
    def refresh(self,wait_for = False ):
        type(Key.F5)
        wait(0.5)
        self.waitForLoad(wait_for)
    def close_popups(self):
        wait(1)
        p = Pattern(self.image_path+"close_modal.png")
        l = Pattern(self.image_path+"leave_page.png")
        leave  = exists(l)
        #modal  = Region(350,224,750,295).exists(p)
        modal  = Region(10,100,SCREEN.w-20,SCREEN.h-250).exists(p)
        if modal != None and leave == None:
            modal.click()
            wait(0.5)
        leave  = exists(l)
        while leave != None:
            leave.click()
            wait(1)
            leave  = exists(l)
    def closeMessages(self):
        l = Pattern(self.image_path+"message_close.png").similar(0.90)
        reg = Region(SCREEN.w-100,55,100,50)
        #reg.highlight(2)
        mess = reg.exists(l)
        if mess != None:
            mess.click()
    def scrollDown(self):
        if self.canScrollDown() == True:
            type(Key.PAGE_DOWN)
            wait(1)
            return True
        return False
    def canScrollDown(self):
        s = Pattern(self.image_path+"scroll_arrow.png")
        if self.right_bar.exists(s.similar(0.95)) == None:
            #popup("cant scroll")
            return False
        sc = Pattern(self.image_path+"sdn.png")
        if self.right_bar.exists(sc.similar(0.97)):
            return False
        return True
    def isPageLoad(self):
        wait(0.5)
        if self.bar_adress.exists(self.image_path+"page_is_load.png") != None:
            return True
        return False
    def tryToLoad(self,control_im = False):
        try:
            p1=Pattern(self.image_path+"page_now_loading.png").similar(0.65)
            x=self.bar_adress.wait(p1,5)
            wait(3)
            if control_im == False:
                p2=Pattern(self.image_path+"page_is_load.png").similar(0.8)
                x=self.bar_adress.wait(p2,self.page_load_time)
            else:
                x=wait(control_im,self.page_load_time)
            return True
        except:
            return False
        
    def waitForLoad(self,control_im = False):
        res = self.tryToLoad(control_im) 
        p_reload =  Pattern(self.image_path+"try_again.png").similar(0.7)
        rel = exists(p_reload)
        if rel != None:
            click(rel)
            return self.tryToLoad(control_im)
        return res

    def clickLink(self,link,control_im = False):
        click(link)
        self.waitForLoad(control_im)
    def close(self):
        #self.open()
        self.focus()
        keyDown(Key.CTRL)
        keyDown(Key.SHIFT)
        type("w")
        keyUp(Key.CTRL)
        keyUp(Key.SHIFT)
        wait(15)
        if exists(self.icon) != None:
            raise Exception("Broser not closed !") 
    def openMenuOptions(self):
        keyDown(Key.ALT)
        type("t")
        wait(0.5)
        type("o")
        keyUp(Key.ALT)
        #wait(0.5)
        wait(self.image_path+"advanced_tab.png",10)
    def closeMenuOptions(self):
        click(Pattern(self.image_path+"buttons_och.png").targetOffset(-87,0))
    def clearCookie(self):
        return True
        click(self.image_path+"private.png")
        pat =Pattern(self.image_path+"cookie_mode.png").similar(0.90)
        wait(pat,20)
        click(self.image_path+"show_cookies.png")
        wait(0.5)
        rem = exists(self.image_path+"cookie_remove.png")
        if rem != None:
            click()
        wait(0.5)
        click(self.image_path+"close.png")
    def open_proxy_dialog(self):
        self.openMenuOptions()
        #a = exists(self.image_path+"advanced_tab.png")
        #if a != None:
        #    a.click()
        click(self.image_path+"advanced_tab.png")
        wait(0.5)
        click(self.image_path+"network_tab.png")
        wait(0.5)
        click(Pattern(self.image_path+"conn_settings.png").targetOffset(171,6))
        wait(0.5)
    def close_proxy_dialog(self):
        click(self.image_path+"button_ok.png")
        mouseMove(Location(0,0))
    def proxy_off(self):
        self.open_proxy_dialog()
        click(Pattern(self.image_path+"no_proxy.png").similar(0.65).targetOffset(-36,0))
        self.close_proxy_dialog()
        #self.clearCookie()
        self.closeMenuOptions()
    def proxy_on(self,ip,port = '3128'):
        port=str(port)
        self.open_proxy_dialog()
        click(Pattern(self.image_path+"proxy_manual.png").targetOffset(-87,0))
        loc = find(self.image_path+"http_proxy.png")
        loc2=Pattern(self.image_path+"http_proxy.png").targetOffset(50,0)
        click(loc2)
        keyDown(Key.CTRL)
        type('a')
        keyUp(Key.CTRL)
        paste(ip)
        proxy_vert = Region(loc.x,loc.y-20,SCREEN.w-loc.x,loc.h+40)
        #proxy_vert.highlight(5)
        proxy_vert.click(Pattern(self.image_path+"proxy_port.png").targetOffset(28,0))
        #click(Pattern(self.image_path+"http_proxy.png").targetOffset(40,0))
        keyDown(Key.CTRL)
        type('a')
        keyUp(Key.CTRL)
        paste(port) 
        wait(0.5)
        self.close_proxy_dialog()
        #self.clearCookie()
        self.closeMenuOptions()
    def getDigits(self,pat,length = 45,symbols = 7):
        bal = exists(pat)
        if bal != None:
            clk_loc = pat.getTargetOffset()
            b = self.copyText(bal.x+bal.w+clk_loc.x,bal.y+bal.h/2+clk_loc.y,length)
            if b == False:
                return False            
            try:
                symbols = -1*symbols
                b = b[symbols:]
                bs = ''.join(x for x in b if x.isdigit() or x == '.')
                res = float(bs)
                return res
            except:
                return False
        return False
        
