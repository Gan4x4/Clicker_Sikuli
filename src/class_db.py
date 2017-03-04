from __future__ import with_statement
from com.ziclix.python.sql import zxJDBC
import class_user
import random
import datetime
class my_db():
    db = False
    def __init__(self):
        self.jdbc_url = "jdbc:odbc:cl"
        self.username = ""
        self.password = ""
        self.driver = "sun.jdbc.odbc.JdbcOdbcDriver"
# obtain a connection using the with-statment
        self.connect()
        
    def connect(self):
        if self.db != False:
            self.db.close()
        self.db = zxJDBC.connect(self.jdbc_url, self.username, self.password, self.driver)
            
    def dict_cursor(self,cursor):
        description = [x[0] for x in cursor.description]
        for row in cursor:
            yield dict(zip(description, row))
    def get_data(self,table,where = ''):
        c = self.db.cursor() 
        query = "SELECT * FROM "+table+" "+where;
        print query
        c.execute(query)
        dc = self.dict_cursor(c)
        #c.close()
        return dc     
    def getFreeIp(self,login):
        res = self.get_data('ip_table',' WHERE user Is Null AND status is Null')
        try:
            print str(res)
            for d in res:
                if (len(d) < 2):
                    return False
                return {'ip':d['ip'],'port':d['port']}
            return False
        except:
            return False
    def isUserNameFree(self,name):
        user = self.get_data('users_table'," WHERE username = '"+name+"'")
        for i in user:
            return False
        return True
    def isIpExists(self,name):
        user = self.get_data('ip_table'," WHERE ip = '"+name+"'")
        for i in user:
            return True
        return False
    def executeQuery(self,query):
        try:
            print query
            c = self.db.cursor() 
            c.execute(query)
            #print c.description()
            #c.commit()
            c.close()
            self.db.commit()
            self.connect()
            return True
        except:
            return False
        
    def markIp(self,ip,status):
        if not self.isIpExists(ip):
            return False
        return self.executeQuery("UPDATE ip_table SET status ='"+status+"' WHERE ip = '"+ip+"'")

    def updateVisitTime(self,user,site,balance = False):
        st = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        if balance != False:
            query = "UPDATE site_binding_table SET last_visit ='"+st+"', balance = "+str(balance)+" WHERE ( (user = '"+user+"') AND (site ='"+site+"') ) "
            #query = "UPDATE site_binding_table SET last_visit ='"+st+"', balance = 0,89 WHERE( (user = '"+user+"') AND (site ='"+site+"') ) "
        else:
            query = "UPDATE site_binding_table SET last_visit ='"+st+"' WHERE ( (user = '"+user+"') AND (site ='"+site+"') ) "
        return self.executeQuery(query)
    
    def bindIpToUser(self,ip,user):
        if self.isUserNameFree(user):
            return False
        if not self.isIpExists(ip):
            return False
        return  self.executeQuery("UPDATE ip_table SET user ='"+user+"' WHERE ip = '"+ip+"'")

    def getUserSites(self,username):
        sl = self.get_data('site_binding_table'," WHERE user = '"+username+"' ")
        s_list = []
        for s in sl:
            if s['site'] == None:
                continue
            s_list.append(s['site'])
    #AND status <> 'Dead'
        return s_list
        
    def getUserIpList(self,username):
        ips = self.get_data('ip_table'," WHERE (user = '"+username+"') AND (status is Null)  ORDER BY date")
        ip_list = []
        for ip in ips:
            if ip['ip'] == None:
                continue
            ip_list.append(ip)
    #AND status <> 'Dead'
        return ip_list
    def get_users_list(self):
        ulist = []
        ud = self.get_data('users_table','ORDER BY Rnd()')
        for u in ud:
            if u['username'] == None:
                continue
            print u['username']
            user = class_user.User(u['username'],u['password'])
            user.ip = self.getUserIpList(user.login)
            user.sites = self.getUserSites(user.login)
            #if user.getCurrentIp() == False:
                #print "User "+u['username']+" has no ip"
                #continue
            ulist.append(user)
        random.shuffle(ulist)
        return ulist
    
    def close(self):
        self.db.close()
        
    def __exit__(self, type, value, traceback):
        self.close()
           

#print "Now here"

#for a in c.description:
#    print a
#for a in dc.fetchall():
#for a in dc:
#    print a['username']