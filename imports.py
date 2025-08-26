import os
import sys
import subprocess
import re
import platform
import pandas as pd
import json
import dotenv
from dotenv import load_dotenv
import fileManagement as FM
import utils as UTILS
import serpapi
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
QLabel, QDialog, QSpinBox, QListWidget, QAbstractItemView, QListWidgetItem )
from PyQt6.QtCore import pyqtSignal
import api
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as CService
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.edge.service import Service as EService
from selenium.webdriver.edge.options import Options as EOptions
import fileManagement as FM
