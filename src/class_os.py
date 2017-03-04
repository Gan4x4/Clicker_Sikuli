'''
Created on 11.08.2013

@author: Anton
'''
import org.sikuli.basics.SikuliXforJython
from sikuli import *
#from sikuli.Sikuli import *
class GanOs:
    def __init__(self,im_p=""):
        self.image_path = im_p
        self.start_panel = Region(0,723,1366,45)
        self.browsers_dir = ""
    def setEnglish(self):
        en = Pattern(self.image_path+"EN.png").similar(0.97)
        if self.start_panel.exists(en) == None:
            keyDown(Key.SHIFT)
            keyDown(Key.ALT)
            wait(0.5)
            keyUp(Key.ALT)
            keyUp(Key.SHIFT)
            wait(0.5)
        return True
    def setTable(self):
        self.start_panel.click(self.image_path+"table.png")
    def launchBrowser(self,icon,logo):
        self.setTable()
        click(Location(0,0))
        wait(0.5)
        doubleClick(icon)
        wait(logo,200)       
        
             
            
        
