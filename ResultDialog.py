#coding:utf8
import wx
import wx.lib.agw.hyperlink as hl

class ResultDialog(wx.Dialog):
    def __init__(self,parent,ID,urlList,title=u"更新されたページ",size=(300,100),pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE,useMetal=False,):
        #wx.Dialog.__init__(parent,-1,title,size,pos,style)

        pre = wx.PreDialog()
        pre.Create(parent,ID,title,pos,size,style)
        self.PostCreate(pre)

        self.LinkList = []

        #put Widgets
        sizer = wx.BoxSizer(wx.VERTICAL)

        if len(urlList) == 0:
            label = wx.StaticText(self,-1,u"更新されたページはありませんでした")
            sizer.Add(label,0,wx.ALIGN_CENTER|wx.ALL,5)

        else:
            label = wx.StaticText(self,-1,u"以下のページが更新されています")
            sizer.Add(label,0,wx.ALIGN_CENTER|wx.ALL,5)

            for url in urlList:
                self.LinkList.append(hl.HyperLinkCtrl(self,-1,url,URL=url))
            for link in self.LinkList:
                sizer.Add(link,0,wx.ALIGN_CENTER|wx.ALL,5)


        self.SetSizer(sizer)
        sizer.Fit(self)


