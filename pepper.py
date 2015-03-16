#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, re, random
from xml.etree import ElementTree
from naoqi import ALProxy

class Poser:
  def __init__(self, xapFile):
    xml = open(xapFile).read()
    self.elem = ElementTree.fromstring(xml.replace('xmlns="http://www.aldebaran-robotics.com/schema/choregraphe/position.xsd"',''))
  def apply(self, motion, poseName, speed = 0.5, asnyc = False):
    elem = self.elem
    pos = [e for e in elem.getiterator("position") if e.find("./name").text == poseName][0]
    motors = [[e.find("./name").text, float(e.find("./value").text) ] for e in pos.getiterator("Motor")]
    names = [m[0] for m in motors]
    angles = [m[1] for m in motors]
    if asnyc:
      motion.post.angleInterpolationWithSpeed(names, angles, speed)
    else:
      motion.angleInterpolationWithSpeed(names, angles, speed)
    #anglist = [[m[1]] for m in motors]
    #speedlist = [[1.0] for m in motors]
    #motion.angleInterpolation(names, anglist, speedlist, True)

class PepperBase:
  def __init__(self, host, port):
    self.motion = ALProxy("ALMotion", host, port)
    self.posture = ALProxy("ALRobotPosture", host, port)
    self.tts = ALProxy("ALTextToSpeech", host, port)
    self.tts.setLanguage('Japanese')
    self.poser = Poser('pose.xap')
  def pose(self, name, speed, async):
    self.poser.apply(self.motion, name, speed, async)
  def say(self, str):
    self.tts.say(str)
  def say_async(self, str):
    self.tts.post.say(str)

if __name__ == "__main__":
  host = "localhost"
  port = 60535

  pp = PepperBase(host,port)

  line = sys.stdin.readline()
  while line:
    line = line.rstrip()
    pose = "normal1" if 1 == random.randint(0, 1) else "normal2"
    pp.pose(pose, 0.3, True)
    pp.say_async(line)
    line = sys.stdin.readline()
