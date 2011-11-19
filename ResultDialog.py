#coding:utf8
import wx

class ResultDialog(wx.Dialog):
    def __init__(self,parent,ID,title=u"更新されたページ",size=wx.DefaultSize,pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE,useMetal=False,):
        #wx.Dialog.__init__(parent,-1,title,size,pos,style)

        pre = wx.PreDialog()
        pre.Create(parent,ID,title,pos,size,style)
        self.PostCreate(pre)

        #put Widgets
        sizer = wx.BoxSizer(wx.VERTICAL)

        testST = wx.StaticText(self,-1,"test label")
        sizer.Add(testST,0,wx.ALIGN_CENTER|wx.ALL,5)

        self.SetSizer(sizer)
        sizer.Fit(self)


