import sqlite3 as sq
import pandas as pd
from xml.dom import minidom

con = sq.connect("C:/Users/matte/OneDrive/Desktop/Projects/VsCode/free-code/blog-wagtail/wagtail-test/theblog/db.sqlite3")
pointer=con.execute("select* from blog_blogpage")
for p in pointer:
    date = p[1]
    print("Date: ", date)
    print("Intro: ", p[2])
    print("Body: ", p[3])
    print("Author: ", p[4])
    print("")

df=pd.read_sql("select* from blog_blogpage",con)
print(df)

date = df['date']
intro = df['intro']
body = df['body']
author = df['author_id']

print('Date',date)
print('Intro',intro)
print('Body',body)
print('Author',author)

# csv
df.to_csv('database.csv', index=False, encoding='utf-8')

# XLSX
xlsx = df.to_excel(r'C:\Users\matte\OneDrive\Desktop\Projects\VsCode\free-code\wagtail-blog\export_dataframe.xlsx', index = False, header=True)

# XML
xml = df.to_xml()
print(xml)


def to_xml(df):
    def row_xml(row):
        xml = ['<item>']
        for i, col_name in enumerate(row.index):
            xml.append('  <{0}>{1}</{0}>'.format(col_name, row.iloc[i]))
        xml.append('</item>')
        return '\n'.join(xml)
    res = '\n'.join(df.apply(row_xml, axis=1))
    return(res)
to_xml(df)

with open('df.xml', 'w') as f:
    f.write(to_xml(df))


