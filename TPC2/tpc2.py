import sys
import re

def special_format(text):
    text = re.sub(r"\*\*\*([^\*]+)\*\*\*",r"<em><strong>\1</strong></em>",text)
    text = re.sub(r"\*\*([^\*]+)\*\*",r"<strong>\1</strong>",text)
    return re.sub(r"\*([^\*]+)\*",r"<em>\1</em>",text)

# Heading tem de começar com # ou ter == -- por baixo
# Tem de ter linhas vazias vazias antes e depois se começar por #
# Se começar por # tem de ter um espaço a separar o titulo
# # tem prioridade a == e --
def heading(text):
    text = re.sub(r"([^\n]+)(?!#{1,6} )\n={1,}(?:(\n)|$)",r"<h1>\1</h1>\2",text)
    text = re.sub(r"([^\n]+)(?!#{1,6} )\n-{2,}(?:(\n)|$)",r"<h2>\1</h2>\2",text)
    i = 6
    while i != 0:
        text = re.sub(r"(?:^#{%d}|(\n)#{%d}) ([^\n]+)(\n|$)"%(i,i), r"\1<h%d>\2</h%d>\3"%(i,i) ,text)
        i-=1
    return text
    

def paragraph(text):
    text = re.sub(r"([^\n])(\n)(?!<h|- |<a|<img|\d+\. | )([^\n])",r"\1<br>\3",text)
    text = re.sub(r"(\n|^)(?!<h|- |<a|<img|\d+\. | )([^\n]+)(\n|$)", r"\1<p>\2</p>\3",text)
    return text

def ordered_list(text):
    text = re.sub(r"(([\t ]*)1\. )",r"\2<ol>\n\1",text)
    text = re.sub(r"\d+\. ([^\n]*)",r"<li>\1</li>",text)
    number = re.findall(r"<ol>",text)
    for i in number:
        text = re.sub(r"((?P<spaces>[\t ]*)<ol>\n(?>(?:(?P=spaces)[\t ]*<\w+>.*\n)*)(?!(?P=spaces)[\t ]*<\/ol>))",r"\1\2</ol>\n",text)
    return text

def hyperlink(text):
    return re.sub(r"(?<!!)\[(?P<Title>.*)\]\((?P<link>.*)\)",r'<a href="\2">\1</a>',text)

def image(text):
    return re.sub(r"!\[(?P<Title>.*)\]\((?P<link>.*)\)",r'<img src="\2" alt="\1"/>',text)


if sys.argv[1][-3:] != ".md":
    print("Not a MD file")
    exit

fileIn = open(sys.argv[1],"r")

text = fileIn.read()
text = heading(text)
text = image(text)
text = hyperlink(text)
text = special_format(text)
text = ordered_list(text)
text = paragraph(text)


print(text)

if len(sys.argv) == 2 or sys.argv[2][-5:] != ".html":
    fileOut = open(sys.argv[1][:-3] + ".html","w+")
else:
    fileOut = open(sys.argv[2])

fileOut.write(text)




