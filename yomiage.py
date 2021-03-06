#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 生放送コメント読み上げ

from nicolivecomment import *
from pepper import *

class Pepper(PepperBase):
  def __init__(self, host, port):
    PepperBase.__init__(self, host, port)
  def wara(self):
    self.tts.post.say("わらわらわら")
    for x in [1,2,3,4]:
      self.poser.apply(self.motion, "wara")
      self.poser.apply(self.motion, "wara2")
      print(x)
  def pachi(self):
    self.tts.post.say("ぱちぱちぱち")
    for x in [1,2,3,4]:
      self.poser.apply(self.motion, "clap2_1")
      self.poser.apply(self.motion, "clap2_2")
      print(x)
  def on_comment(self, c):
    print(u"{no}({vpos}): {comment}".format(**c))
    line = c['comment'].encode('utf-8')
    line = re.sub(u"ｗ", "w", line)
    line = re.sub(u"８", "8", line)
    line = re.sub(r"w{4,}", "www", line)
    line = re.sub(r"8{4,}", "888", line)
  
    if re.search(r"w{2,}$", line):
      self.say(re.sub(r"w{2,}$", "", line))
      self.wara()
    elif re.search(r"8{2,}$", line):
      self.say(re.sub(r"8{2,}$", "", line))
      self.pachi()
    else:
      line = re.sub(r"w", "わら", line)
      line = re.sub(r"8", "ぱち", line)
      pose = "normal1" if 1 == random.randint(0, 1) else "normal2"
      self.pose(pose, 0.3, True)
      self.say(line)


if len(sys.argv) < 4:
  print("usage: {s} lv12345 email@example.com PASSWORD".format(s = sys.argv[0]))
  print("usage: {s} lv12345 user_session USER_SESSION_STRING".format(s = sys.argv[0]))
  exit

lv = sys.argv[1]
receiver = NicoliveCommentReceiver()
## login or set_user_session
receiver.login(sys.argv[2], sys.argv[3])
host = "localhost"
port = 9559

pp = Pepper(host,port)

receiver.start(lv, pp.on_comment)
