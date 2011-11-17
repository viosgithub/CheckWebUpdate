#coding:utf8
import urllib2,hashlib,sqlite3,os.path

WEB_DB_NAME = "web.db"

def getWebHash(url):
    content = urllib2.urlopen(url)
    return hashlib.md5(content.read()).hexdigest()

def updateWebDB(url):
    if not os.path.exists(WEB_DB_NAME):
        makeTable()
    hash = getWebHash(url)
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
            print "update!!"
        else:
            print "not update"
    else:
        print "Error:this url is not registered"
    con.close()


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
    updateWebDB("http://google.co.jp")
    dumpDB()
    isUpdate("http://google.co.jp")
