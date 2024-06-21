import os
from tika import parser

# Define the topics and their associated keywords
keyword_dict = {
    "gaming and science fiction": ['משחק', 'שחקן', 'שחקנים', 'קרב',  'ניצחון',  'הפסד',  'unity', 'גיימינג' , 'עלילה', 'פאזל', 'פאזלים' , 'עלילתי' , 'חייזר' , 'שחקני' ,'שלב' , 'יוניטי', 'מסתורי', 'ניקוד', 'אסטרטגיה', 'יריב',  'תחרות', 'משימה', 'אויב', 'הרפתקאות', 'הרפתקה', 'מכשולים',  'להילחם', 'פסילה', 'חייל'],
    
    "laws": ['משפטיים' , 'משפטיות' , 'משפטי', 'משפטית', 'עורך' , 'עורכי' , 'דין' , 'משפט' ,'זכות' , 'זכויות' , 'תביעה' , 'חוקים', 'חקיקה' , 'נחקק' , 'חוק' , 'סעיף' , 'פרקליט', 'עדות' , 'עדויות', 'ראיות' , 'דיון' , 'דיונים' , 'תיק'],
    
    "school and academia": ['מרצה' , 'מרצים', 'אקדמיה', 'מחלקה' , 'ועדה' , 'הרצאות', 'מצגות', 'מצגת', 'בתי ספר' , 'בתי הספר', 'בית הספר' , 'בית ספר' , 'לימודים' , 'תלמיד' , 'קורס', 'מקצוע', 'מורים' ,'מורה', 'הוראה', 'שיעור', 'חינוך', 'כיתה', 'כיתתי'],
    
    "family and relationship": ['ילד' , 'ילדים', 'זיווג', 'הורות' , 'משפחה' , 'זוג' ,'לידה' , 'שידוך','שידוכים', 'זוגיות', 'בן זוג', 'בת זוג', 'היכרות', 'תינוק'],
    
    "medicine": ['תור'  , 'רופא' , 'מטופל' , 'מטפל' , 'טיפול', 'רפואה' , 'רפואי' , 'מדד' , 'לחץ דם' , 'דופק' , 'סטורציה' , 'נשימה' , 'נשימות', 'אבחון' , 'הפרעה' , 'הפרעות', 'אירידיולוגיה'],
    
    "communication": ['מוקדים' , 'טלפוניים',  'טלפון', 'מייל' , 'דיווח', 'לדווח' , 'מוקד' , 'פניה' , 'פניות' , 'מדווח' , 'להגיב'],
    
    "social": ['קהל', 'אנשים', 'שאלונים' , 'שאלון', 'סקר', 'שאלות', 'התנדבות' , 'אוכלוסייה' , 'מתנדב' , 'חברתי' , 'תוכן', 'תכנים' , 'שיתופי'],
    
    "market": ['רכישה', 'חנות' , 'מפעל' , 'יצרן' , 'יצרנים' , 'מוצר', 'מחיר' , 'עסק' ,'מסחר' , 'משלוח' , 'חשבונית' , 'חשבוניות' , 'יד שניה', 'מכירה', 'מפרסם', 'עלות', 'תשלום', 'פריט', 'שוק', 'סופרמרקט', 'קופה', 'קופאי', 'ספק', 'חנויות', 'הזמנה', 'עובד' , 'כוח אדם' , 'מסגרת' , 'הכשרה' ],
    
    "leisure and culture": ['מוזיקלי','כנס', 'מוזיקה' , 'קול' , 'אפקט', 'סאונד' , 'הופעה' , 'תייר' , 'מסורת' , 'תרבות' , 'אטרקציות' , 'אטרקציה' , 'מסעדה'  , 'מסעדות' , 'מוזיאון' , 'סרט','Movie', 'אמן' , 'אמנים' ,'כרטיס', 'ספריה', 'מוזמנים', 'אירוע', 'תופים', 'נגינה', 'מזון', 'ירקות', 'פירות', 'בשר', 'חלב', 'מתכונים', 'מתכון'],
    
    "health and sport": ['בריאות', 'כושר', 'אימון', 'אימון אישי', 'מתאמן', 'תזונה', 'מאמנים', 'עישון',  'מעשן', 'גמילה', 'מעשנים', 'סיגריה', 'סיגריות'],
    
    "math": ['מתמטי' , 'פונקציה' , 'פונקציות' , 'אלגברה' , 'מטריצה' , 'דטרמיננטה' , 'גרף', 'גרפים', 'קודקוד'],
    
    "housework": ['דירה' , 'דייר' , 'השכרה', 'השכרת', 'דירות' , 'שוכר', 'משכיר', 'חשמל', 'מים', 'ארנונה', 'משכנתא', 'הוצאות', 'הכנסות', 'חסכונית', 'חשבון', 'חשבונות', 'דוח'],
    
    "design": ['עיצוב' , 'לעצב' , 'יעצב' , 'פילטר' , 'filter' ],
    
    "nature , navigation and driving": ['נהג' , 'צמיג' , 'רכב', 'מוסך' , 'נסיעות' , 'יעד' , 'ניווט' , 'waze' , 'לנסוע' ,'כביש' , 'דרך'  , 'דרכים' , 'הגה' , 'נהיגה' , 'נתיב', 'נוסע', 'נסיעה', 'מפה', 'מצפן', 'מיקום', 'מרחק', 'מסלול', 'טיול' , 'הליכה' , 'כלב' , 'סביבה'],
    
    "criminal and emergency": ['סכנות' ,'מסוכן', 'סכנה' , 'נזק' , 'שריפה', 'שריפות', 'להתריע' , 'התרעה', 'חירום', 'הצלה', 'לכוד', 'לכודים',  'מצוקה', 'בריונות' , 'אלימות' , 'אלימה' , 'אלים' , 'התעללות' ],
    
    "documents and text": ['מסמכים', 'טקסטים' , 'טקסט' , 'טקסטואליות', 'טקסטואלית', 'מסמך', 'תרגום','מילים','מילון', 'ביטוי', 'חילוץ', 'ביטויים', 'ארכיון', 'ארכיונים', 'קריאה'],
    
    "support for the disabled": ['כבדי שמיעה', 'כבד השמיעה' , 'לקות',  'שפת הסימנים', 'חירש' , 'בעלי מוגבלות' , 'לקויות' , 'עיוורים' , 'אוטיזם' , 'אוטיסט' , 'נויורולוגי' , 'נחייה', 'אילם', 'אילמים'],
    
    "software & hardware": ['קוד', 'שגיאה', 'זמן ריצה', 'פיתוח', 'מתכנת',  'stack overflow', 'אובייקט', 'תחזוקה',  'שרת', 'חומרה']
}

# Define the tree structure
tree = {
    'root': {
        'children': {}
    }
}

# Populate the tree with topics and keywords
for topic, keywords in keyword_dict.items():
    topic_node = {
        'count': 0,
        'children': {}
    }
    for keyword in keywords:
        keyword_node = {
            'children': {}
        }
        topic_node['children'][keyword] = keyword_node
    tree['root']['children'][topic] = topic_node

# Function to classify a new PDF file
def classify_pdf(file_path):
    # Extract text from the PDF file using Tika
    parsed_pdf = parser.from_file(file_path)
    print(parsed_pdf)
    text = parsed_pdf['content']
    
    # Update the counters in the tree based on the keywords in the text
    for topic_node in tree['root']['children'].values():
        for keyword in topic_node['children']:
            keyword_count = text.count(keyword)
            if keyword_count > 0:
                topic_node['count'] += keyword_count
    
    # Find the topic node with the highest count
    max_count = 0
    predicted_topic = ""
    for topic, topic_node in tree['root']['children'].items():
        if topic_node['count'] > max_count:
            max_count = topic_node['count']
            predicted_topic = topic
    
    return predicted_topic


# Example usage
pdf_file = "newFiles/trend_seeker.pdf"
predicted_topic = classify_pdf(pdf_file)
print(f"The predicted topic for the PDF file is: {predicted_topic}")


