# !/usr/bin/python
# coding=utf8

import sys
from nucleon import *

def main():
    app = QApplication(sys.argv)
    window = Nucleon()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()