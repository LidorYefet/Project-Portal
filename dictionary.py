import os
import pandas as pd
from tika import parser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Create dictionary of keywords for each class
keyword_dict = {
    "Gaming and science fiction": ['משחק', 'שחקן', 'שחקנים', 'קרב',  'ניצחון',  'הפסד',  'Unity', 'גיימינג' , 'עלילה', 'פאזל', 'פאזלים' , 'עלילתי' , 'חייזר' , 'שחקני' ,'שלב' , 'יוניטי', 'מסתורי', 'ניקוד', 'אסטרטגיה', 'יריב',  'תחרות', 'משימה', 'אויב', 'הרפתקאות', 'הרפתקה', 'מכשולים',  'להילחם', 'פסילה', 'חייל'],
    
    "laws": ['משפטיים' , 'משפטיות' , 'משפטי', 'משפטית', 'עורך' , 'עורכי' , 'דין' , 'משפט' ,'זכות' , 'זכויות' , 'תביעה' , 'חוקים', 'חקיקה' , 'נחקק' , 'חוק' , 'סעיף' , 'פרקליט', 'עדות' , 'עדויות', 'ראיות' , 'דיון' , 'דיונים' , 'תיק'],
    
    "school and academia": ['מרצה' , 'מרצים', 'אקדמיה', 'מחלקה' , 'ועדה' , 'הרצאות', 'מצגות', 'מצגת', 'בתי ספר' , 'בתי הספר', 'בית הספר' , 'בית ספר' , 'לימודים' , 'תלמיד' , 'קורס', 'מקצוע', 'מורים' ,'מורה', 'הוראה', 'שיעור', 'חינוך', 'כיתה', 'כיתתי'],
    
    "Family and relationship": ['ילד' , 'ילדים', 'זיווג', 'הורות' , 'משפחה' , 'זוג' ,'לידה' , 'שידוך','שידוכים', 'זוגיות', 'בן זוג', 'בת זוג', 'היכרות', 'תינוק'],
    
    "medicine": ['תור'  , 'רופא' , 'מטופל' , 'מטפל' , 'טיפול', 'רפואה' , 'רפואי' , 'מדד' , 'לחץ דם' , 'דופק' , 'סטורציה' , 'נשימה' , 'נשימות', 'אבחון' , 'הפרעה' , 'הפרעות', 'אירידיולוגיה'],
    
    "communication ": ['מוקדים' , 'טלפוניים',  'טלפון', 'מייל' , 'דיווח', 'לדווח' , 'מוקד' , 'פניה' , 'פניות' , 'מדווח' , 'להגיב'],
    
    "social": ['קהל', 'אנשים', 'שאלונים' , 'שאלון', 'סקר', 'שאלות', 'התנדבות' , 'אוכלוסייה' , 'מתנדב' , 'חברתי' , 'תוכן', 'תכנים' , 'שיתופי'],
    
    "market": ['רכישה', 'חנות' , 'מפעל' , 'יצרן' , 'יצרנים' , 'מוצר', 'מחיר' , 'עסק' ,'מסחר' , 'משלוח' , 'חשבונית' , 'חשבוניות' , 'יד שניה', 'מכירה', 'מפרסם', 'עלות', 'תשלום', 'פריט', 'שוק', 'סופרמרקט', 'קופה', 'קופאי', 'ספק', 'חנויות', 'הזמנה', 'עובד' , 'כוח אדם' , 'מסגרת' , 'הכשרה' ],
    
    "Leisure and culture": ['מוזיקלי', 'מוזיקה' , 'קול' , 'אפקט', 'סאונד' , 'הופעה' , 'תייר' , 'מסורת' , 'תרבות' , 'אטרקציות' , 'אטרקציה' , 'מסעדה'  , 'מסעדות' , 'מוזיאון' , 'סרט','Movie', 'אמן' , 'אמנים' ,'כרטיס', 'ספריה', 'מוזמנים', 'אירוע', 'תופים', 'נגינה', 'מזון', 'ירקות', 'פירות', 'בשר', 'חלב', 'מתכונים', 'מתכון'],
    
    "Health and sport": ['בריאות', 'כושר', 'אימון', 'אימון אישי', 'מתאמן', 'תזונה', 'מאמנים', 'עישון',  'מעשן', 'גמילה', 'מעשנים', 'סיגריה', 'סיגריות'],
    
    "math": ['מתמטי' , 'פונקציה' , 'פונקציות' , 'אלגברה' , 'מטריצה' , 'דטרמיננטה' , 'גרף', 'גרפים', 'קודקוד'],
    
    "housework": ['דירה' , 'דייר' , 'השכרה', 'השכרת', 'דירות' , 'שוכר', 'משכיר', 'חשמל', 'מים', 'ארנונה', 'משכנתא', 'הוצאות', 'הכנסות', 'חסכונית', 'חשבון', 'חשבונות', 'דוח'],
    
    "Design": ['עיצוב' , 'לעצב' , 'יעצב' , 'תמונה' , 'תמונות' , 'פילטר' , 'filter' ],
    
    "Nature , navigation and driving": ['נהג' , 'צמיג' , 'רכב', 'מוסך' , 'נסיעות' , 'יעד' , 'ניווט' , 'waze' , 'לנסוע' ,'כביש' , 'דרך'  , 'דרכים' , 'הגה' , 'נהיגה' , 'נתיב', 'נוסע', 'נסיעה', 'מפה', 'מצפן', 'מיקום', 'מרחק', 'מסלול', 'טיול' , 'הליכה' , 'כלב' , 'סביבה'],
    
    "criminal and emergency": ['סכנות' ,'מסוכן', 'סכנה' , 'נזק' , 'שריפה', 'שריפות', 'להתריע' , 'התרעה', 'חירום', 'הצלה', 'לכוד', 'לכודים',  'מצוקה', 'בריונות' , 'אלימות' , 'אלימה' , 'אלים' , 'התעללות' ],
    
    "documents and text": ['מסמכים', 'טקסטים' , 'טקסט' , 'טקסטואליות', 'טקסטואלית', 'מסמך', 'תרגום', 'ביטוי', 'חילוץ', 'ביטויים', 'ארכיון', 'ארכיונים', 'קריאה'],
    
    "Support for the disabled": ['כבדי שמיעה', 'כבד השמיעה' , 'לקות',  'שפת הסימנים', 'חירש' , 'בעלי מוגבלות' , 'לקויות' , 'עיוורים' , 'אוטיזם' , 'אוטיסט' , 'נויורולוגי' , 'נחייה', 'אילם', 'אילמים'],
    
    "Software & Hardware": ['קוד', 'שגיאה', 'זמן ריצה', 'פיתוח', 'מתכנת',  'stack overflow', 'אובייקט', 'תחזוקה',  'שרת', 'חומרה']
}

# Set your directory path
directory = 'C:/Users/lidor/Documents/Lidor/Lidor Study/Project Portal/data1'

# Prepare lists to store texts and their corresponding classes
texts = []
classes = []


# loop through each folder in the main folder
for sub_folder_name in os.listdir(directory):
    sub_folder_path = os.path.join(directory, sub_folder_name)
    # check if folderpath is a folder (not a file)
    if os.path.isdir(sub_folder_path):
        print('checking : ', sub_folder_name)
        # loop through each PDF file in the folder
        for pdf_file_name in os.listdir(sub_folder_path):
            if pdf_file_name.endswith('.pdf'):
                pdf_filepath = os.path.join(sub_folder_path, pdf_file_name)
                file_data = parser.from_file(pdf_filepath)
                texts.append(file_data['content'])
                classes.append(os.path.basename(sub_folder_path)) # Assumes that class is encoded in the last folder name

print (classes)
# Prepare DataFrame from text and classes
data = pd.DataFrame({
    'text': texts,
    'class': classes
})

print (data['class'].unique())

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(data['text'], data['class'], test_size=0.2, random_state=42)

# Create the pipeline
text_clf = Pipeline([
    ('tfidf', TfidfVectorizer(vocabulary=[word for words in keyword_dict.values() for word in words])), 
    ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)),
])

# Train the classifier
text_clf.fit(X_train, y_train)

# Predict the test set results
predicted = text_clf.predict(X_test)

# Evaluate the performance
print(classification_report(y_test, predicted, target_names=data['class'].unique()))

