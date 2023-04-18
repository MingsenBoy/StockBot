import mysql.connector
import pandas as pd
import requests
from stock import  stock_change
import re
from bs4 import BeautifulSoup
import emoji

import pyodbc
connection_string = "Driver=SQL Server;Server=localhost;Database={0};Trusted_Connection=Yes;Database={0};" 
cnxn = pyodbc.connect(connection_string.format("linebot"), autocommit=True)

## test