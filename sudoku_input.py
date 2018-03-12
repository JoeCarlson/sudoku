#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
""" A script for displaying and initializing a sudoko board
A Qt app shows a sudoku board and reads an from user input
When the 'solve' button is pressed, a JSON structure is passed
to the solver
"""
__author__    = "Joe Carlson"
__copyright__ = "Copyright 2018 All rights retained"
import sys
import json
import subprocess
import json
from PyQt4.QtGui import *
from PyQt4.QtCore import *

numberSize = 50

class SudokuCell(QLineEdit):
  """A class to describe a single cell in a board"""

  board = 0

  def __init__(self,b):
    self.board = b
    super(SudokuCell,self).__init__()
    self.setFixedSize(numberSize,numberSize)
    self.setMaxLength(1)
    self.setAlignment(Qt.AlignHCenter)
    validator = QIntValidator(1,9,b)
    self.setValidator(validator)
    font = QFont()
    font.setFamily("Helvetica")
    font.setFixedPitch(True)
    font.setPixelSize(30)
    self.setFont(font)

  def keyPressEvent(self,e):
    if e.key() == Qt.Key_Left:
      self.board.moveToCell("left")
    if e.key() == Qt.Key_Right:
      self.board.moveToCell("right")
    if e.key() == Qt.Key_Up:
      self.board.moveToCell("up")
    if e.key() == Qt.Key_Down:
      self.board.moveToCell("down")
    if e.key() == Qt.Key_Tab:
      self.board.moveToCell("next")

    super(SudokuCell,self).keyPressEvent(e)

class SudokuBoard(QWidget):
  """A class to describe a sudoko board"""

  cells = []
  activeCell = 0

  def __init__(self):
    super(SudokuBoard, self).__init__()
    self.initUI()

  def clearCells(self,bo):
    for row in self.cells:
      for col in row:
        col.clear()

  def moveToCell(self,direction):

    activeRow = self.activeCell/9
    activeCol = self.activeCell%9

    if direction == 'left':
      activeCol -= 1
      activeCol = (activeCol+9)%9
      self.activeCell = 9*activeRow + activeCol
    if direction == 'right':
      activeCol += 1
      activeCol = (activeCol+9)%9
      self.activeCell = 9*activeRow + activeCol
    if direction == 'up':
      activeRow -= 1
      activeRow = (activeRow+9)%9
      self.activeCell = 9*activeRow + activeCol
    if direction == 'down':
      activeRow += 1
      activeRow = (activeRow+9)%9
      self.activeCell = 9*activeRow + activeCol
    if direction == 'next':
      self.activeCell += 1
      self.activeCell = (self.activeCell+81)%81
      activeRow = self.activeCell/9
      activeCol = self.activeCell%9

    print "active row/col are now "+str(activeRow)+" "+str(activeCol)
    self.cells[activeRow][activeCol].setFocus()

  def solvePuzzle(self,bo):
    rowN = 0
    jsonArray = []
    for row in self.cells:
      rowN += 1
      colN = 0
      for col in row:
         colN += 1
         if not col.text().isEmpty():
           jsonArray.append({"row":rowN, "col":colN, "val":col.text().toShort()[0]});
    proc = subprocess.Popen(["./sudoku_numpy.py"], stdin=subprocess.PIPE)
    proc.stdin.write(json.dumps(jsonArray)+'\n')

  def initUI(self):
    self.cells = []

    ## the UI
    ##w = QWidget()
    # Set window size.
    self.resize(9*numberSize,10*numberSize)

    # Set window title
    self.setWindowTitle("SudokuTF")

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

    # Add a solve button
    btn2 = QPushButton('Solve', buttonFrame)
    btn2.setToolTip('Click to solve')
    btn2.clicked.connect(self.solvePuzzle)
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

    # Show window
    self.show()

def main():
  # Create an PyQT4 application object.
  a = QApplication(sys.argv)
  board = SudokuBoard()
  sys.exit(a.exec_())

if __name__ == '__main__':
  main()
