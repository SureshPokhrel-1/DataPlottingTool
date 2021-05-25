# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 14:17:17 2021

@author: supokhrel
"""

from PyQt5 import QtWidgets, uic, QtCore
import sys
import os
import threading

File_Path = '' 
init_dir = os.getcwd()



def BrowseFile():
    global status
    global File_Path
    global init_dir
#    print("Browsing...")
    fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Single File', init_dir , '*.csv')
#    print(fileName)
    
    if (fileName == ''):
        call.lineEdit.setText("!!!! File Not selected")
        File_Path = ''
    else:
        call.lineEdit.setText(fileName)
        File_Path = fileName
        init_dir = os.path.dirname(os.path.abspath(fileName))
        call.lineEdit_7.setText("Filling Entries")
        

def string_conveter_func(get_str):

    new_str = get_str.replace("PM10", "PM$\mathregular{_{10}}$")
    new_str = new_str.replace("PM2.5", "PM$\mathregular{_{2.5}}$")
    new_str = new_str.replace("PM1", "PM$\mathregular{_{1}}$")
    new_str = new_str.replace("O3", "O$\mathregular{_{3}}$")
    new_str = new_str.replace("CO2", "CO$\mathregular{_{2}}$")
    new_str = new_str.replace("SO2", "SO$\mathregular{_{2}}$")
    new_str = new_str.replace("NOx", "NO$\mathregular{_{x}}$")
    new_str = new_str.replace("NO2", "NO$\mathregular{_{2}}$")
    
    new_str = new_str.replace("ug/m3", "µg/m$\mathregular{^{3}}$")
    new_str = new_str.replace("DEG", "$\degree$")
    
    return new_str
 
def is_int_or_float(s):
    ''' return 1 for int, 2 for float, -1 for not a number'''
    try:
        float(s)

        return 1 if s.count('.')==0 else 2
    except ValueError:
        return -1     

from matplotlib import pyplot as plt 
#import numpy as np
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
 
def Data_process():
#    print("Started")
#    call.update()
    call.lineEdit_7.setText('Processing.......      Please do not press any button')
    import pandas as pd
    import glob
#    import numpy as np
     
    from matplotlib import rc
    from datetime import datetime
        
    global fig, ax 
#    ax = None
#    fig, ax = plt.subplots()
    File = glob.glob(File_Path)

    if not File:
#        print("Empty Filename")
#        window.destroy()
        
        call.lineEdit_7.setText('Error: No input file selected.')
        return 0

    
    
    Plot_title = call.lineEdit_2.text()
    Plot_title = string_conveter_func(Plot_title)
    X_lab = call.lineEdit_3.text()
    X_lab = string_conveter_func(X_lab)
    Y_lab = call.lineEdit_4.text()
    Y_lab = string_conveter_func(Y_lab)
    
    y_min = call.lineEdit_5.text()
    y_min_contain = False
    if(y_min != ''):
        y_min_contain = True
        check_ymin = is_int_or_float(y_min)
        if (check_ymin == 1):
            y_min = int(y_min)
        elif (check_ymin == 2):
            y_min = float(y_min)
        else:
            call.lineEdit_7.setText('Error: Y-min is not a numerical value')
            return 0 
     
    y_max = call.lineEdit_6.text()
    y_max_contain = False
    if(y_max !=''):
        y_max_contain = True
        check_ymax = is_int_or_float(y_max)
        if (check_ymax == 1):
            y_max = int(y_max)
        elif (check_ymax == 2):
            y_max = float(y_max)
        else:
            call.lineEdit_7.setText('Error: Y-max is not a numerical value')
            return 0 
        
    plot_type = call.comboBox.currentText()
#    print("Plot-type",plot_type )
    res_dpi = call.comboBox_2.currentText()
    X_size = int(call.comboBox_3.currentText())
    Y_size = int(call.comboBox_4.currentText())
    X_grid = call.radioButton_3.isChecked()
    Y_grid = call.radioButton_5.isChecked()
    try:
        df = pd.concat([pd.read_csv(fp, low_memory=False) for fp in File], ignore_index=True)
    except:
        call.lineEdit_7.setText('E  rror in reading th  e input f ile')
        return 0
    
    for i in range(1, len(df.columns)):
        df[df.columns[i]] = pd.to_numeric(df[df.columns[i]], errors='coerce')
        df.rename(columns={df.columns[i]:string_conveter_func(df.columns[i])}, inplace = True)
   
    rc('font', weight='bold') 
#    plt.pause(0.001)
    
    if (plot_type != 'Bar'):
        df.insert(0, 'Date_temp', pd.to_datetime(df[df.columns[0]]))
        df.drop(columns=[df.columns[1]], inplace = True)
        df.rename(columns = {'Date_temp':'Date'}, inplace = True)
        
        df.drop_duplicates(subset='Date', keep = 'last', inplace = True)
        df = df.sort_values(by='Date')
        df = df.set_index(['Date'])
#        df = df.reindex(pd.DatetimeIndex(df.index), fill_value=np.nan)
    
        if (plot_type == 'Line'):
             df.plot(figsize = (X_size,Y_size), ax=ax)
        elif (plot_type == 'Scatter'):
             df.plot(ax=ax, style = 'o',  ms=1.5, figsize = (X_size,Y_size))
        elif (plot_type == 'Box'):
             df.boxplot(ax=ax, showmeans=True, showfliers=False, figsize = (X_size,Y_size))
#           print("Box-plot is plotted") 
    else:
        
        df = df.set_index([df.columns[0]])
#        print(df)
        df.plot.bar(ax=ax, rot=0, figsize = (X_size,Y_size))
    
    ax.set_title(Plot_title,fontsize=14, fontweight='bold')
    ax.set_ylabel(Y_lab, fontsize=12, fontweight='bold')
    ax.set_xlabel(X_lab, fontsize=12,  fontweight='bold')
    
    if(X_grid):
        ax.grid(b=True, which='major', axis='x' , lw = 0.2)
    else:
        ax.grid(b=False, which='major', axis='x' )
    if(Y_grid):
        ax.grid(b=True, which='major', axis='y', lw = 0.2 )
    else:
        ax.grid(b=False, which='major', axis='y' )
    if(y_min_contain):
        ax.set_ylim(ymin= y_min)
    if(y_max_contain):
        ax.set_ylim(ymax= y_max)
    if(len(df.columns) < 2 and plot_type != 'Box'):
        ax.get_legend().remove()
#    plt.show()
#    fig.show()
    InputFolder_path = os.path.dirname(os.path.abspath(File_Path)) 
    InputFileName_ = os.path.basename(File_Path)
    InputFileName = os.path.splitext(InputFileName_)[0]
#    print(InputFolder_path)
#    print(InputFileName) 
    now = datetime.now()
    dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
    Output_FilePath = InputFolder_path+'/' + dt_string+ '_' + InputFileName+'.jpg'
#    print(Output_FilePath)
    fig.savefig(Output_FilePath,dpi=int(res_dpi),bbox_inches = 'tight')
    ax.cla()
    call.lineEdit_7.setText('Successfully completed:')
    os.startfile(InputFolder_path)
    print('\a')
    
    
    

app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)

import time
def start_process():
    Data_process()
    time.sleep(4)

def btn_run():
     
     my_Thread = threading.Thread(target=start_process, args=())
     my_Thread.start()
     
  
      
        
call  = uic.loadUi("GUI.ui")
call.setWindowTitle('Data Plotting Tool v21.1 (Beta)')
call.setGeometry(250, 250, 800, 500)
call.comboBox_3.setCurrentIndex(5);
call.pushButton.clicked.connect(BrowseFile)
call.pushButton_2.clicked.connect(btn_run)


fig, ax = plt.subplots()

call.show()
app.exec()
