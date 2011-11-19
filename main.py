#coding:utf-8
import wx
import os
import glob,shutil

import webdb
import ResultDialog


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        global urlListBox

        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title=title, size=(200,-1))
        #self.urlListBox = wx.ListBox(self,26,wx.DefaultPosition,(370,500),flist,wx.LB_SINGLE)
        self.urlListBox = wx.ListBox(self,26,wx.DefaultPosition,(370,500),webdb.getUrlList(),wx.LB_SINGLE)
        urlListBox = self.urlListBox
        self.urlListBox.Bind(wx.EVT_LISTBOX_DCLICK,self.dclickList)
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        # Setting up the menu.
        filemenu= wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open\tCtrl+O"," Open a file to edit")
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Events.
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        """
        dropTarget = dragdrop.FileDropTarget(self.urlListBox,self)
        self.urlListBox.SetDropTarget(dropTarget)
        """


        # Use some sizers to see layout options

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.btAddUrl = wx.Button(self,label=u"URLの追加")
        self.btDelUrl = wx.Button(self,label=u"URLの削除")
        self.btCheck = wx.Button(self,label=u"更新確認")
        #self.buttonDelete = wx.Button(self,label=u"削除")
        self.sizer2.Add(self.btAddUrl,1,wx.EXPAND)
        self.sizer2.Add(self.btDelUrl,1,wx.EXPAND)
        self.sizer3.Add(self.btCheck,1,wx.EXPAND)
        #self.sizer3.Add(self.buttonDelete,1,wx.EXPAND)
        self.btAddUrl.Bind(wx.EVT_BUTTON,self.selectAddUrl)
        self.btDelUrl.Bind(wx.EVT_BUTTON,self.selectDelUrl)
        self.btCheck.Bind(wx.EVT_BUTTON,self.selectCheck)
        #self.buttonDelete.Bind(wx.EVT_BUTTON,self.selectDelete)


        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.urlListBox, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)
        self.sizer.Add(self.sizer3, 0, wx.EXPAND)

        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Centre()
        self.Show()

    def decodeStr(self,list):
        ret = []
        for name in list:
            ret.append(name.decode("cp932"))
        return ret

    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, u"ホームページの更新確認プログラム", u"About", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.


    """
    def setDropedList(self,path):
        global dirPath,flist,startPath,endPath
        if not os.path.isdir(path):
            print "this is not direcotry!!"
            return

        dirPath = path
        print dirPath
        #os.chdir(dirPath)
        flist = glob.glob(os.path.join(dirPath,"*"))
        basenames = []
        for name in flist:
            basenames.append(os.path.basename(name))
        urlListBox.Set(basenames)
        startPath = None
        endPath = None
    """


    def selectAddUrl(self,e):
        dlg = wx.TextEntryDialog(self,u"追加するURLを入力してください")
        if dlg.ShowModal() == wx.ID_OK:
            webdb.updateWebDB(dlg.GetValue())
            urlListBox.Set(webdb.getUrlList())

    def selectDelUrl(self,e):
        delUrl = urlListBox.GetString(urlListBox.GetSelections()[0])
        webdb.delUrl(delUrl)
        urlListBox.Set(webdb.getUrlList())

    def dclickList(self,e):
        print urlListBox.GetSelections()[0]
        self.urlListBox.SetItemBackgroundColour(urlListBox.GetSelections()[0],wx.Colour(0,255,0))
        self.urlListBox.Refresh()
        print "dclicked"

    def selectCheck(self,e):
        urlList = webdb.getUrlList()
        updateUrlList = []
        max = len(urlList)
        dlg = wx.ProgressDialog(u"更新確認中...",u"進捗",maximum=max,parent=self,style=wx.PD_APP_MODAL
                | wx.PD_REMAINING_TIME
                )
        keepGoing = True
        count = 0
        for url in urlList:
            if webdb.isUpdate(url):
                updateUrlList.append(url)
            count +=1
            keepGoing,skip = dlg.Update(count)

        dlg.Close()
        dlg.Destroy()
        
        dlg2 = ResultDialog.ResultDialog(self,-1,updateUrlList)
        dlg2.Show()
    """



    def selectDelete(self,e):
        global dirPath
        if dirPath is None : 
            return
        dlg = wx.MessageDialog(self,dirPath+u"\n\nを本当に削除しますか？",u"確認",wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        if result == wx.ID_OK :
            print "run"
            shutil.rmtree(dirPath)
            dirPath = None
            urlListBox.Set([""])
        else:
            print "canceled"
    """



urlListBox = None
app = wx.App(False)
frame = MainWindow(None, u"ホームページ更新確認プログラム")
app.MainLoop()
