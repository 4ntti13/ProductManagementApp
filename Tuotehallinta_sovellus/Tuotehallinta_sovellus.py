from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow 
from PyQt5.QtWidgets import QApplication 
import sys
from os import path

from PyQt5.uic import loadUiType # use designer file
FORM_CLASS,_=loadUiType(path.join(path.dirname('__file__'),"main.ui")) 

import sqlite3 # tietokanta


class Main(QMainWindow, FORM_CLASS):
    #ctor:
    def __init__(self, parent = None): 
        super(Main, self).__init:(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handel_buttons()
        self.navigate()



    def handel_buttons(self): # connect buttons to their methods
        self.paivita.clicked.connect(self.get_data) 
        self.etsi.clicked.connect(self.search) 
        self.update_btn.clicked.connect(self.update)
        self.delete_btn.clicked.connect(self.delete)
        self.add_btn.clicked.connect(self.add)


    # Connection to Sqlite3 database and fill the table with data.
    def get_data(self):
        
        db = sqlite3.connect("tuotteet.db") 
        cursor = db.cursor()
        command = ''' SELECT * from tuotteet_table '''  

        result = cursor.execute(command)
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


        
        #productgroup counter for statistics:
        cursor2 = db.cursor() 

        label_2 = ''' SELECT COUNT (DISTINCT viite) from tuotteet_table '''
        result_parts_nbr = cursor2.execute(label_2)
        self.lbl_parts_nbr.setText(str(result_parts_nbr.fetchone()[0]))


    
    # This works
    def search(self): 
        
        db = sqlite3.connect("tuotteet.db")
        cursor = db.cursor()
        nbr = int(self.laskuri.text()) 
        command = ''' SELECT * from tuotteet_table WHERE lukumäärä <=?'''
        result = cursor.execute(command, [nbr])  # replace the ?-mark with nbr var.
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))



    def top(self): # top 3 tuotteet, joita vähiten

        db = sqlite3.connect("tuotteet.db") 
        cursor = db.cursor()

        command = ''' SELECT viite, tuote, lukumäärä FROM tuotteet_table order by lukumäärä asc LIMIT 3 '''  

        result = cursor.execute(command)

        self.table2.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table2.setItem(row_number, column_number, QTableWidgetItem(str(data)))



    def navigate(self): # Muokkaa välilehti

        db = sqlite3.connect("tuotteet.db")
        
        cursor = db.cursor()
        command = ''' SELECT * FROM tuotteet_table '''

        result = cursor.execute(command)
        val = result.fetchone()

        self.id.setText(str(val[0]))
        self.reference.setText(str(val[1]))
        self.part_name.setText(str(val[2]))
        self.count.setValue(val[3])



    #edit data:
    def update(self): 

        db = sqlite3.connect("tuotteet.db") 
        cursor = db.cursor()

        id_ = int(self.id.text())
        reference_= self.reference.text()
        part_name_ = self.part_name.text()
        count_ = str(self.count.value())

        row = (reference_, part_name_, count_, id_)

        command = ''' UPDATE tuotteet_table SET viite = ?, tuote = ?, lukumäärä = ? WHERE ID = ? '''
        cursor.execute(command, row)
        db.commit() # save data after edit.



    def delete(self):

        db = sqlite3.connect("tuotteet.db")
        cursor = db.cursor()

        d = self.id.text()

        command = ''' DELETE FROM tuotteet_table WHERE id=? '''
        cursor.execute(command, d)

        db.commit() # save data after edit.



    def add(self):

        db = sqlite3.connect("tuotteet.db") 
        cursor = db.cursor()


        reference_= self.reference.text()
        part_name_ = self.part_name.text()
        count_ = str(self.count.value())

        row = (reference_, part_name_, count_)

        command = ''' INSERT INTO tuotteet_table (viite, tuote, lukumäärä) VALUES (?, ?, ?) '''

        cursor.execute(command, row)
        db.commit() # tallennetaan data muokkauksen jälkeen.




def main():
    app=QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__=="__main__":
    main()

