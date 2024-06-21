# -------------------------

# Lidor Yefet - 208063859
# Guy Barel - 206174815

# -------------------------
import os
import shutil
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, QSortFilterProxyModel
from tika import parser

# declaration of the dictionary of topics and their keywords
keyword_dict = {
    "gaming and science fiction": ['משחק', 'שחקן', 'שחקנים', 'קרב',  'ניצחון',  'הפסד',  'unity', 'גיימינג' , 'עלילה',
                                    'פאזל', 'פאזלים' , 'עלילתי' , 'חייזר' , 'שחקני' ,'שלב' , 'יוניטי', 'מסתורי',
                                      'ניקוד', 'אסטרטגיה', 'יריב',  'תחרות', 'משימה', 'אויב', 'הרפתקאות', 'הרפתקה',
                                        'מכשולים',  'להילחם', 'פסילה', 'חייל'],
    
    "laws": ['משפטיים' , 'משפטיות' , 'משפטי', 'משפטית', 'עורך' , 'עורכי' , 'דין' ,
              'משפט' ,'זכות' , 'זכויות' , 'תביעה' , 'חוקים', 'חקיקה' , 'נחקק' , 'חוק' ,
                'סעיף' , 'פרקליט', 'עדות' , 'עדויות', 'ראיות' , 'דיון' , 'דיונים' , 'תיק'],
    
    "school and academia": ['מרצה' , 'מרצים', 'אקדמיה', 'מחלקה' , 'ועדה' , 'הרצאות',
                             'מצגות', 'מצגת', 'בתי ספר' , 'בתי הספר', 'בית הספר' , 
                             'בית ספר' , 'לימודים' , 'תלמיד' , 'קורס', 'מקצוע', 'מורים' ,
                             'מורה', 'הוראה', 'שיעור', 'חינוך', 'כיתה', 'כיתתי'],
    
    "family and relationship": ['ילד' , 'ילדים', 'זיווג', 'הורות' , 'משפחה' ,
                                 'זוג' ,'לידה' , 'שידוך','שידוכים', 'זוגיות',
                                   'בן זוג', 'בת זוג', 'היכרות', 'תינוק'],
    
    "medicine": ['תור'  , 'רופא' , 'מטופל' , 'מטפל' , 'טיפול', 'רפואה' ,
                  'רפואי' , 'מדד' , 'לחץ דם' , 'דופק' , 'סטורציה' , 'נשימה' ,
                    'נשימות', 'אבחון' , 'הפרעה' , 'הפרעות', 'אירידיולוגיה'],
    
    "communication": ['מוקדים' , 'טלפוניים',  'טלפון', 'מייל' , 'דיווח',
                       'לדווח' , 'מוקד' , 'פניה' , 'פניות' , 'מדווח' , 'להגיב'],
    
    "social": ['קהל', 'אנשים', 'שאלונים' , 'שאלון', 'סקר', 'שאלות', 'התנדבות' , 'אוכלוסייה' , 'מתנדב' , 'חברתי' , 'תוכן', 'תכנים' , 'שיתופי'],
    
    "business and market": ['רכישה', 'חנות' , 'מפעל' , 'יצרן' , 'יצרנים' , 'מוצר', 'מחיר' , 'עסק' ,'מסחר' , 'משלוח' , 'חשבונית' , 'חשבוניות' , 'יד שניה', 'מכירה', 'מפרסם', 'עלות', 'תשלום', 'פריט', 'שוק', 'סופרמרקט', 'קופה', 'קופאי', 'ספק', 'חנויות', 'הזמנה', 'עובד' , 'כוח אדם' , 'מסגרת' , 'הכשרה' ],
    
    "leisure and culture": ['מוזיקלי','כנס', 'מוזיקה' , 'קול' , 'אפקט', 'סאונד' , 'הופעה' , 'תייר' , 'מסורת' , 'תרבות' , 'אטרקציות' , 'אטרקציה' , 'מסעדה'  , 'מסעדות' , 'מוזיאון' , 'סרט','Movie', 'אמן' , 'אמנים' ,'כרטיס', 'ספריה', 'מוזמנים', 'אירוע', 'תופים', 'נגינה', 'מזון', 'ירקות', 'פירות', 'בשר', 'חלב', 'מתכונים', 'מתכון'],
    
    "health and sport": ['בריאות', 'כושר', 'אימון', 'אימון אישי', 'מתאמן', 'תזונה', 'מאמנים', 'עישון',  'מעשן', 'גמילה', 'מעשנים', 'סיגריה', 'סיגריות'],
    
    "math": ['מתמטי' , 'פונקציה' , 'פונקציות' , 'אלגברה' , 'מטריצה' , 'דטרמיננטה' , 'גרף', 'גרפים', 'קודקוד'],
    
    "housework": ['דירה' , 'דייר' , 'השכרה', 'השכרת', 'דירות' , 'שוכר', 'משכיר', 'חשמל', 'מים', 'ארנונה', 'משכנתא', 'הוצאות', 'הכנסות', 'חסכונית', 'חשבון', 'חשבונות', 'דוח'],
    
    "design": ['עיצוב' , 'לעצב' , 'יעצב' , 'פילטר' , 'filter' ],
    
    "nature , navigation and driving": ['נהג' , 'צמיג' , 'רכב', 'מוסך' , 'נסיעות' , 'יעד' , 'ניווט' , 'waze' , 'לנסוע' ,'כביש' , 'דרך'  , 'דרכים' , 'הגה' , 'נהיגה' , 'נתיב', 'נוסע', 'נסיעה', 'מפה', 'מצפן', 'מיקום', 'מרחק', 'מסלול', 'טיול' , 'הליכה' , 'כלב' , 'סביבה'],
    
    "criminal and emergency": ['סכנות' ,'מסוכן', 'סכנה' , 'נזק' , 'שריפה', 'שריפות', 'להתריע' , 'התרעה', 'חירום', 'הצלה', 'לכוד', 'לכודים',  'מצוקה', 'בריונות' , 'אלימות' , 'אלימה' , 'אלים' , 'התעללות' ],
    
    "documents and text": ['מסמכים', 'טקסטים' , 'טקסט' , 'טקסטואליות', 'טקסטואלית', 'מסמך', 'תרגום','מילים','מילון', 'ביטוי', 'חילוץ', 'ביטויים', 'ארכיון', 'ארכיונים', 'קריאה'],
    
    "support for the disabled": ['כבדי שמיעה', 'כבד השמיעה' , 'לקות',  'שפת הסימנים', 'חירש' , 'בעלי מוגבלות' , 'לקויות' , 'עיוורים' , 'אוטיזם' , 'אוטיסט' , 'נויורולוגי' , 'נחייה', 'אילם', 'אילמים'],
    
    "software & hardware": ['קוד', 'שגיאה', 'זמן ריצה', 'פיתוח', 'מתכנת',  'stack overflow', 'אובייקט', 'תחזוקה',  'שרת', 'חומרה','נוזקה','נוזקות']
}


# search graph structure
graph = {
    'root': {
        'children': {}
    }
}
# containing the graph with topics and keywords children for each topic
# loop over each topic and its keyword according to the dictionary
for topic, keywords in keyword_dict.items():
    # create a node for topic with counter
    topic_node = {
        'counter': 0,
        'children': {}
    }
    # loop over every specific keyword 
    for keyword in keywords:
        # create a leaf node for the keyword
        keyword_node = {
            'children': {}
        }
        # convert the specific keyword to a 'keyword_node' formation AND link it to his father topic node
        topic_node['children'][keyword] = keyword_node
    #linking the keywords to their specific topic, make it a topic node AND link it to the root node in the graph
    graph['root']['children'][topic] = topic_node

#function for classifying a new PDF file by self-developed graph-searching algorithm        
def prediction(file_path):
    # reset tree counts before classifying a new file
    reset_tree_counts()

    # extract text from the PDF file using Tika
    parsed_pdf = parser.from_file(file_path)
    text = parsed_pdf['content']
    
    # update the counters in the tree based on the keywords in the text
    for topic_node in graph['root']['children'].values():
        for keyword in topic_node['children']:
            keyword_count = text.count(keyword)
            if keyword_count > 0:
                topic_node['count'] += keyword_count
    
    # find the topic node with the highest count
    max_count = 0
    predicted_topic = "None"
    for topic, topic_node in graph['root']['children'].items():
        if topic_node['count'] > max_count:
            max_count = topic_node['count']
            predicted_topic = topic
    return os.path.basename(file_path), predicted_topic

def reset_tree_counts():
    for topic_node in graph['root']['children'].values():
        topic_node['count'] = 0

# PandasModel class for connecting a pandas DataFrame table with a QTableView object
# main target - to display and make interaction with the DataFrame in the GUI application.
class PandasModel(QAbstractTableModel):
    def __init__(self, df = pd.DataFrame(), parent=None):
        QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    # return the numbers of rows in the DataFrame (shape[0]) for knowing how many rows to display in the GUI
    def rowCount(self, parent=None):
        return self._df.shape[0]
    
    # return the numbers of columns in the DataFrame (shape[1]) for knowing how many columns to display in the GUI
    def columnCount(self, parent=None):
        return self._df.shape[1]

    #return the data in the DataFrame - for displaying in the GUI 
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._df.iloc[index.row(), index.column()])
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            try:
                return str(self._df.columns[section])
            except IndexError:
                return None

# MainWindow class - the main application window that will allow all the widgets to be shown
class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        # set global font style for the application
        font = QFont()
        font.setPointSize(15)  # set font size
        font.setWeight(20)  # set font weight
        QApplication.setFont(font)

        # create QTableView object - a widget that presents data in a spreadsheet-like table view. 
        self.table = QTableView()
        
        # connect the doubleClicked signal to the open_file function (show the PDF file in the computer)
        self.table.doubleClicked.connect(self.open_file)

        # make a pandas DataFrame two-dimensional table based on an excel file
        self.df = pd.read_excel("C:/Users/lidor/Documents/Lidor/Lidor Study/Project Portal/data_table_GUI.xlsx")  

        #creating a PandasModel object according to the pandas DataFrame table (for better compatibility with the GUI)
        model = PandasModel(self.df)

        #display the pandas table into the GUI widget
        self.table.setModel(model)

        #creating buttons and link them to the correct functions (by clicking) :

        self.button = QPushButton("Add Project")
        self.button.clicked.connect(self.add_project)

        self.sort_btn = QPushButton("Sort By Subjects")
        self.sort_btn.clicked.connect(self.sort_table)

        self.search_field = QLineEdit()
        self.search_field.textChanged.connect(self.filter_table)

        # create a QVBoxLayout object - arranging all the widgets of the GUI vertically
        widgets_layout = QVBoxLayout()
        widgets_layout.addWidget(self.table)
        widgets_layout.addWidget(self.button)
        widgets_layout.addWidget(self.sort_btn)
        widgets_layout.addWidget(self.search_field)

        # creating a QWidget object - for containing all the layout of the GUI
        layout_container = QWidget()
        layout_container.setLayout(widgets_layout)
        self.setCentralWidget(layout_container)
    
    def open_file(self, index):
        # get the content of the cell that was clicked
        name_of_pdf_file = index.data()  
        file_path = "C:/Users/lidor/Documents/Lidor/Lidor Study/Project Portal/database_GUI/" + name_of_pdf_file
        # check if the file exists in the database file and open it in front of the user
        if os.path.isfile(file_path): 
            os.startfile(file_path)  

    # add new PDF file to the program , after classifying the topic of the file 
    def add_project(self):
        options = QFileDialog.Options()
        #open a file dialog and wait for the user to select a file
        file_path, _ = QFileDialog.getOpenFileName(self,"Select File", "", "All Files (*)", options=options)

        if file_path:
            # copy the file to the directory where you're storing the other files
            database_file_path = "C:/Users/lidor/Documents/Lidor/Lidor Study/Project Portal/database_GUI/" + os.path.basename(file_path)
            shutil.copyfile(file_path, database_file_path)
            
            filename, prediction_result = prediction(file_path)

            # create new DataFrame with the new file name and its topic , and link it to the existing table 
            new_data = pd.DataFrame({self.df.columns[0]: [filename], self.df.columns[-1]: [prediction_result]})
            self.df = self.df._append(new_data, ignore_index=True)

            # update the new table according to the changes by adding new file
            self.table.model().beginResetModel()
            self.table.model()._df = self.df
            self.table.model().endResetModel()

    # function for sorting the file names by A-B-C 
    def sort_table(self):
        self.df = self.df.sort_values(self.df.columns[-1])
        self.update_model()

    # function that creates a filtering model base on the search text line
    def filter_table(self, text):
        if text:  # if there is any text typed in the search line - filter by the text
            filter_model = QSortFilterProxyModel()
            filter_model.setSourceModel(self.table.model())
            filter_model.setFilterKeyColumn(-1)  
            filter_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
            filter_model.setFilterRegExp(text)  
            self.table.setModel(filter_model)
        else:  # if the search line is empty - get back to the original table
            model = PandasModel(self.df)
            self.table.setModel(model)
    
    def update_model(self):
        model = PandasModel(self.df)
        self.table.setModel(model)
    
#create the whole GUI application : 

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())

