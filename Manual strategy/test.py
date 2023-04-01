# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 21:31:39 2018

@author: steve
"""
import pandas as pd
import numpy as np
import datetime as dt
import os
import math
from util import get_data, plot_data
import matplotlib.pyplot as plt

import BestPossibleStrategy as bps
df_trades = bps.testPolicy(symbol = "AAPL", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000) 
