#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
""" A script for displaying a solving sudoko board.
A Qt app shows a sudoku board and reads an input
JSON stream to display a solution in progress
"""
__author__    = "Joe Carlson"
__copyright__ = "Copyright 2018 All rights retained"

import sys
import json
import math
from PyQt4.QtGui import *
from PyQt4.QtCore import *

numberSize = 50
charHeight = 50


class SudokuCell(QLabel):
  """A class for describing a single cell in a sudoko board"""

  data = [0.,0.,0.,0.,0.,0.,0.,0.,0.]
  def __init__(self,b):
    super(SudokuCell,self).__init__()
    self.setFixedSize(numberSize,numberSize)
    palette = QPalette()
    palette.setColor(QPalette.Background,Qt.white)
    self.setPalette(palette)
    self.setAutoFillBackground(True)

  def paintEvent(self,event):
    painter = QPainter()
    painter.begin(self)
    font = QFont()
    font.setFamily("Helvetica")
    font.setFixedPitch(True)
    font.setPixelSize(charHeight)
    charWidth = QFontMetrics(font).maxWidth()
    number = 1
    norm = math.sqrt(sum(i*i for i in self.data))
    if abs(norm) < 1e-4:
      norm = 1;
    for val in self.data:
      brush = QBrush(QColor(0,0,128,round(max(0,min(255,abs(val/norm)*255)))))
      painter.setBrush(brush)
      pen = QPen()
      pen.setBrush(brush)
      painter.setPen(pen)
      painter.setFont(font)
      painter.drawText(0,0,charWidth,charHeight,Qt.AlignCenter,str(number))
      number = number + 1
    painter.end()

  def setData(self,vals):
    self.data = vals

class SudokuBoard(QWidget):
  """A class for describing a sudoko board"""

  cells = []
  activeCell = 0

  def __init__(self):
    super(SudokuBoard, self).__init__()
    self.initUI()

  def clearCells(self,bo):
    for row in self.cells:
      for col in row:
        col.clear()

  def savePuzzle(self,a):
    exit

  def initUI(self):
    self.cells = []

    ## the UI
    ##w = QWidget()
    # Set window size.
    self.resize(9*numberSize,10*numberSize)

    # Set window title
    self.setWindowTitle("SudokuSolution")

    windowLayout = QVBoxLayout(self)
    self.setLayout(windowLayout)

    boardFrame = QFrame(self)
    boardFrame.resize(10*numberSize,10*numberSize)
    boardFrame.setFixedSize(10*numberSize,10*numberSize)
    palette = QPalette()
    palette.setColor(QPalette.Background,Qt.black)
    boardFrame.setAutoFillBackground(1)
    boardFrame.setPalette(palette)

    windowLayout.addWidget(boardFrame)
    windowLayout.addStretch()
    buttonFrame = QFrame(self)
    buttonFrame.resize(9*numberSize,numberSize)
    windowLayout.addWidget(buttonFrame)

    boardLayout = QGridLayout()
    boardLayout.setSpacing(0)
    boardLayout.setContentsMargins(0,0,0,0)
    buttonLayout = QHBoxLayout()
    boardFrame.setLayout(boardLayout)

    for row in range(0,9):
      self.cells.append([])
      for col in range(0,9):
        cell = SudokuCell(self)
        boardLayout.addWidget(cell,row,col)
        self.cells[row].append(cell)

    # Add a clear button
    btn1 = QPushButton('Clear', buttonFrame)
    btn1.setToolTip('Click to clear')
    btn1.clicked.connect(self.clearCells)
    btn1.resize(btn1.sizeHint())
    buttonLayout.addStretch()
    buttonLayout.addWidget(btn1)
    buttonLayout.addStretch()

    # Add a save button
    btn2 = QPushButton('Save', buttonFrame)
    btn2.setToolTip('Click to save solution')
    btn2.clicked.connect(self.savePuzzle)
    btn2.resize(btn2.sizeHint())
    buttonLayout.addWidget(btn2)
    buttonLayout.addStretch()
    buttonFrame.setLayout(buttonLayout)

    # Add a quit button
    btn3 = QPushButton('Quit', buttonFrame)
    btn3.setToolTip('Click to exit')
    btn3.clicked.connect(exit)
    btn3.resize(btn3.sizeHint())
    buttonLayout.addWidget(btn3)
    buttonLayout.addStretch()
    buttonFrame.setLayout(buttonLayout)

    # connect stdin
    self.qsn = QSocketNotifier(0, QSocketNotifier.Read, self)
    self.connect(self.qsn, SIGNAL('activated(int)'), self.on_qsn)
    self.stdin = QFile("/dev/stdin")
    self.stdin.open(QIODevice.ReadOnly)
    self.connect(self.stdin, SIGNAL('readyRead()'), self.on_stdinReadyRead)

    # Show window
    self.show()

  def on_qsn(self, i): 
    self.on_stdinReadyRead() 

  def on_stdinReadyRead(self): 
    line =  self.stdin.readLineData(50000)
    if line != None:
      jsonData = json.loads(line)
      for ele in jsonData['data']:
        row = ele['row']
        col = ele['col']
        self.cells[row-1][col-1].data = ele['data']
        self.cells[row-1][col-1].repaint()
    

def main():
  # Create an PyQT4 application object.
  a = QApplication(sys.argv)
  board = SudokuBoard()
  sys.exit(a.exec_())

if __name__ == '__main__':
  main()
  t = SudokuBoard()
  print t.__doc__
