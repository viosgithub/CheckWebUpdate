#coding:utf8
import urllib2,hashlib,sqlite3,os.path

WEB_DB_NAME = "web.db"

def getWebHash(url):
    try:
        content = urllib2.urlopen(url)
    except (urllib2.URLError,ValueError):
        return False
    return hashlib.md5(content.read()).hexdigest()

def updateWebDB(url):
    if not os.path.exists(WEB_DB_NAME):
        makeTable()
    hash = getWebHash(url)
    if hash == False:
        print u"入力されたURLは恐らく無効なURLです"
        print u"処理を中断します..."
        return

    con = sqlite3.connect(WEB_DB_NAME,isolation_level=None)
    c = con.cursor()
    c.execute("select * from webpage where url='%s'" % url)
    if c.fetchone():
        print "this url have already registered"
        con.execute("update webpage set hash='%s' where url='%s'" % (hash,url))
        con.close()
    else:
        sql = u"insert into webpage values (?,?)"
        con.execute(sql,(url,hash))
        con.close()

def dumpDB():
    con = sqlite3.connect(WEB_DB_NAME)
    c = con.cursor()
    c.execute("select * from webpage")
    for row in c:
        print "url: %s\nhash: %s\n" % (row[0],row[1])
    con.close()

def getUrlList():
    if not os.path.exists(WEB_DB_NAME):
        return []

    urlList = []
    con = sqlite3.connect(WEB_DB_NAME)
    c = con.cursor()
    c.execute("select * from webpage")
    for row in c:
        urlList.append(row[0])
    con.close()
    return urlList

def delUrl(url):
    con = sqlite3.connect(WEB_DB_NAME,isolation_level=None)
    con.execute("delete from webpage where url='%s'" % url)
    con.close()


def isUpdate(url):
    con = sqlite3.connect(WEB_DB_NAME,isolation_level=None)
    c = con.cursor()
    c.execute("select * from webpage where url='%s'" % url)
    row = c.fetchone()
    if row:
        oldHash = row[1]
        print "oldHash=%s" % oldHash
        newHash = getWebHash(url)
        print "newHash=%s" % newHash
        if oldHash != newHash:
            con.execute("update webpage set hash='%s' where url='%s'" % (newHash,url))
            con.close()
            print "update!!"
            return True
        else:
            print "not update"
            return False
    else:
        print "Error:this url is not registered"
        con.close()
        return False


def makeTable():
    #not auto commit?
    print u"データベースファイルが見つからないため初期処理を行ないます"
    print u"テーブル作成実行..."
    con = sqlite3.connect(WEB_DB_NAME)
    sql = """
    create table webpage(
    url varchar(512),
    hash varchar(32)
    );
    """
    con.execute(sql)
    con.close()
    print u"テーブル作成完了"
    

if __name__ == "__main__":
    dumpDB()
