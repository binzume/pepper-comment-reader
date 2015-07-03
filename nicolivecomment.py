#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, urllib, urllib2, cookielib, socket
from xml.etree import ElementTree

class NicoliveCommentReceiver:
  def __init__(self):
    self.LOGIN_URL = 'https://secure.nicovideo.jp/secure/login?site=niconico'
    self.LIVE_API_URL = 'http://watch.live.nicovideo.jp/api/'
    self.cookies = cookielib.CookieJar()
    cjhdr = urllib2.HTTPCookieProcessor(self.cookies)
    self.opener = urllib2.build_opener(cjhdr)

  def login(self, mail, password):
    if mail == 'user_session':
      self.set_user_session(password)
      return True
    values = {'mail_tel' : mail, 'password' : password}
    postdata = urllib.urlencode(values)
    req = urllib2.Request(self.LOGIN_URL, postdata)
    response = self.opener.open(req)
    page = response.read()
    for c in self.cookies:
      if c.name == 'user_session': return c.value
    return None

  # set session string(ex: user_session_9999999_1234567890abcdef)
  def set_user_session(self, user_session):
    self.opener.addheaders.append(('Cookie', 'user_session=' + user_session))

  def start(self, lv, cbfnc = None):
    player_status_xml = self.opener.open(self.LIVE_API_URL + 'getplayerstatus?v=' + lv).read()
    player_status = ElementTree.fromstring(player_status_xml)
    addr = player_status.find("ms/addr").text
    port = int(player_status.find("ms/port").text)
    thread = player_status.find("ms/thread").text

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))
    sock.send('<thread thread="{thread}" version="20061206" res_from="-1"/>\0'.format(thread=thread))

    data = ''
    while True:
        while data.find("\0") == -1:
          data += sock.recv(1024)
        p = data.find("\0")
        d = ElementTree.fromstring(data[:p])
        data = data[p+1:]
        if d.tag == 'chat':
            num = int(d.get('no') or "-1")
            vpos = int(d.get('vpos') or "-1")
            mail = d.get('mail')
            user_id = d.get('user_id')
            comment = d.text
            if comment == u"/disconnect": break
            if comment.startswith('/'): continue
            if cbfnc != None:
              cbfnc({'comment':comment, 'no':num, 'mail':mail, 'vpos':vpos, 'user_id':user_id})
            else:
              print(comment)

if __name__ == "__main__":
  # sample usage
  if len(sys.argv) < 4:
    print("usage: {s} lv12345 email@example.com PASSWORD".format(s = sys.argv[0]))
    print("usage: {s} lv12345 user_session USER_SESSION_STRING".format(s = sys.argv[0]))
    exit
  lv = sys.argv[1]
  receiver = NicoliveCommentReceiver()
  ## login or set_user_session
  print(receiver.login(sys.argv[2], sys.argv[3]))
  #receiver.set_user_session('user_session_00000000_xxxxxxxxxxxxxxxxxxx')
  def on_comment(c):
    print(u"{no} {vpos}: {comment}".format(**c))
  receiver.start(lv, on_comment)

