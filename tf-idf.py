import pprint
import graphviz




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

search_tree = {}

def print_search_tree(tree, indent=''):
    # Iterate over each key in the current level of the tree
    for key, value in tree.items():
        # Print the key (topic or character)
        print(indent + str(key))
        
        # Check if the value is a nested dictionary
        if isinstance(value, dict):
            # Recursively print the subtree with increased indentation
            print_search_tree(value, indent + '  ')
        elif key == 'keywords':
            # Print the associated keywords for leaf nodes
            print(indent + '  Keywords:', value)

# Call the function to print the search tree
print_search_tree(search_tree)


# Iterate over each topic and its associated keywords
for topic, keywords in keyword_dict.items():
    # Create a reference to the current level of the search tree
    current_level = search_tree
    
    # Iterate over each character in the topic
    for char in topic:
        # Check if the character is already a key in the current level
        if char not in current_level:
            # If not, create a new nested dictionary for the character
            current_level[char] = {}
        
        # Update the reference to the next level
        current_level = current_level[char]
    
    # Assign the keywords to the final level of the search tree
    current_level['keywords'] = keywords

    
# Call the function to print the search tree
print_search_tree(search_tree)
