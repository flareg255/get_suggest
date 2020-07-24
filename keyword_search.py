import requests, bs4, os, pathlib

listItems = []

def main ():
    global listItems

    filePath = 'keywords.txt'
    filePath = pathlib.Path(filePath)
    keywordFileRead(filePath)

    resultListItems = []
    for item in listItems:
        resultListItems.extend(rqApi (item))

    print(resultListItems)

    listItems = set(resultListItems)

    fileWrite(filePath, listItems)


def keywordFileRead (path):
    global listItems

    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8', newline=None) as fileItem:
            listItems = fileItem.readlines()


def rqApi (rqKeyword):
    keywordList = []
    # エンドポイント
    url = 'http://suggestqueries.google.com/complete/search?output=toolbar&hl=en&q=' + rqKeyword
    # # リクエスト
    res = requests.get(url)

    bs4Obj = bs4.BeautifulSoup(res.text, 'lxml')

    for item in bs4Obj.find_all("suggestion"):
        if ' ' in item.get('data'):
            for splitItem in item.get('data').split():
                keywordList.append(splitItem)
        else:
            keywordList.append(item.get('data'))

    return keywordList


def fileWrite (path, str):
    modeType = 'a'
    print(str)
    # if not os.path.isfile(path):
    #     modeType = 'w'

    with open(path, 'w', encoding='utf-8', newline='\n') as fileItem:
        fileItem.write('\n'.join(str))



main();
