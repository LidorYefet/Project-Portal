from tika import parser
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# your data
data ={
    "root": 
    {
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
}    

# DFS function to traverse words and increment node counter
def DFS(G, node, words):
    for word in words:
        if word in G[node]:
            G.nodes[node]['count'] += 1
            DFS(G, word, words)

# BFS function to find category with highest count
def BFS(G, root):
    visited = set()
    queue = deque([root])
    max_count = 0
    max_count_node = ''

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            count = G.nodes[node]['count']

            if count > max_count:
                max_count = count
                max_count_node = node
            
            for neighbour in G.neighbors(node):
                if neighbour not in visited:
                    queue.append(neighbour)

    return max_count_node

# Function to classify a file
def classify_file(file_content, G):
    # Parsing file content into words
    words = file_content.split()
    
    # Resetting counts
    for node in G.nodes():
        G.nodes[node]['count'] = 0
    
    # Running DFS for each word in file
    for word in words:
        if word in G['root']:
            DFS(G, word, words)
    
    # Running BFS to find category with highest count
    category = BFS(G, 'root')
    
    return category

# create directed graph
G = nx.DiGraph()

# add edges to the graph
for parent, children in data.items():
    for child in children:
        G.add_edge(parent, child)

# initialize node counter
for node in G.nodes():
    G.nodes[node]['count'] = 0

for edge in G.edges:
    print(edge)

file_path = "C:/Users/lidor/Documents/Lidor/Lidor Study/Project Portal/newFiles/VioREACH.pdf"

parsed_pdf = parser.from_file(file_path)
text = parsed_pdf['content']

category = classify_file(text, G)
# print('The text file has been classified as:', category)
