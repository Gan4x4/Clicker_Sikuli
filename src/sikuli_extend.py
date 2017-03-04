'''
Created on 31.08.2013

@author: Anton
'''

import org.sikuli.basics.SikuliXforJython
from sikuli import *
import org.sikuli as SKL
#import sikuli.Sikuli as SKL
#import java.awt.Robot as JRobot
#import java.awt.image.BufferedImage;
#import java.awt.image.DataBufferByte;
import java.awt.Color as JColor;
import javax.imageio.ImageIO as IIO
import java.io as jf
#import org.sikuli.script as Jskl
#import org.sikuli.script.Pattern


# ============== Helper function =======================

class Pattern(SKL.Pattern):
    def __init__(self,file_name):
        SKL.Pattern.__init__(self,file_name)
        self.depth = False
    def setColorDiff(self,d):
        self.depth = d

def getColorFormImage(fn):
    f = jf.File(fn) 
    img =  IIO.read(f)
    x = img.getWidth()/2
    y = img.getHeight()/2
    #print "gk "+str(x) +str(y)
    return JColor(img.getRGB(x,y))
def getColorFormPattern(pn):
    #f = jf.File(fn) 
    img =  pn.getImage()
    x = img.getWidth()/2
    y = img.getHeight()/2
    #print "gk "+str(x) +str(y)
    return JColor(img.getRGB(x,y))

def getColorFromScreen(pat):
    #p = pat.getCenter()
    myRobot = JRobot()
    #print " pat center "+str(pat.x+pat.w/2)+" "+str(pat.y+pat.h/2)
    #print "scr "+str(p.x)+"  "+str(p.y)
    return myRobot.getPixelColor(pat.x+pat.w/2, pat.y+pat.h/2)


def compareColors(match,pattern):
    c1 = getColorFromScreen(match) 
    c2 = getColorFormPattern(pattern)
    print c1
    print c2
    if (pattern.depth != False):
        max_diff = pattern.depth
        if abs(c1.getRed() - c2.getRed()) > max_diff or abs(c1.getGreen() - c2.getGreen()) > max_diff or abs(c1.getBlue() - c2.getBlue()) > max_diff:
            print "False"
            return False
    #match.highlight(2)
    print "True"
    return True


# ========= Chanded Sikuli functions =============
def exists(p):
    m = SKL.exists(p)
    if res != None:
        if compareColors(m,p):
            return res
    return None

        
def findAll(p):
    SKL.findAll(p)
    good_list = []
    finded  = list(SKL.getLastMatches())
    if len(finded) > 0 :
        for m in finded:
            if compareColors(m,p) :
                good_list.append(m)
    return good_list
def find(p):
    m = SKL.find(p)
    if compareColors(m,p):
        return m
    raise Exception("Find not proceed color check") 
def waitList(lst,time):
    i = 0
    t = 0
    step = 2
    while time > t:
        for p in lst:
            f = SKL.exists(p) 
            if f != None :
                return f
        SKL.wait(step)
        t = t + step
    return False

    
            
