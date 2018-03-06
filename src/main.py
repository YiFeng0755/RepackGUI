#-*-coding:utf8 -*-

import wx
import os
import sys
import repack

reload(sys)
sys.setdefaultencoding("utf-8")


class Repack(wx.Frame):
    def __init__(self, parent, title):
        super(Repack,self).__init__(parent, title=title, size=(900,620))
        self.InitUI()
        self.BindEvent()
        self.Centre()
        self.Show()
    def InitUI(self):
        panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(6, 5)
        txt_input = wx.StaticText(panel, label=u"apk路径:")
        self.sizer.Add(txt_input, pos=(0, 0), flag=wx.LEFT|wx.TOP, border=15)

        self.ctrl_input = wx.TextCtrl(panel)
        self.sizer.Add(self.ctrl_input, pos=(0, 1), span=(1, 4), flag=wx.TOP|wx.EXPAND, border=15)

        self.btn_file = wx.Button(panel, label=u'选择')
        self.sizer.Add(self.btn_file, pos=(0, 5), flag=wx.TOP, border=15)

        tex_output = wx.StaticText(panel, label=u"保存路径:")
        self.sizer.Add(tex_output, pos=(1, 0), flag=wx.LEFT|wx.TOP, border=15)

        self.ctrl_output = wx.TextCtrl(panel)
        self.sizer.Add(self.ctrl_output, pos=(1, 1), span=(1, 4), flag=wx.TOP|wx.EXPAND, border=5)

        self.btn_output = wx.Button(panel, label=u"选择")
        self.sizer.Add(self.btn_output, pos=(1, 5), flag=wx.TOP|wx.RIGHT, border=5)        

        sb_lua = wx.StaticBox(panel, label=u"引擎版本：")
        boxsizer_lua = wx.StaticBoxSizer(sb_lua, wx.HORIZONTAL)
        self.cbx_lua3_x = wx.CheckBox(panel, label=u"3.x")
        self.cbx_lua4_0 = wx.CheckBox(panel, label=u"4.0")
        self.cbx_lua3_x.SetValue(1)
        self.cbx_lua4_0.SetValue(0)
        boxsizer_lua.Add(self.cbx_lua3_x, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=15)
        boxsizer_lua.Add(self.cbx_lua4_0, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=15)
        self.sizer.Add(boxsizer_lua, pos=(2, 0), span=(1, 5),flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=15)

        
        sb = wx.StaticBox(panel, label=u"额外选项：")

        boxsizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        self.cbx_log = wx.CheckBox(panel, label=u"保存日志")
        self.cbx_medium_file = wx.CheckBox(panel, label=u"保存中间文件")

        self.cbx_log.SetValue(0)
        self.cbx_medium_file.SetValue(0)

        boxsizer.Add(self.cbx_log, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=15)
        boxsizer.Add(self.cbx_medium_file, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=15)

        self.sizer.Add(boxsizer, pos=(3, 0), span=(1, 5),flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=15)

        self.btn_launch = wx.Button(panel, label=u'运行')
        self.sizer.Add(self.btn_launch, pos=(5, 0), flag=wx.LEFT, border=15)

        self.btn_watch_result = wx.Button(panel, label=u'查看结果')
        self.sizer.Add(self.btn_watch_result, pos=(5, 1), flag=wx.LEFT, border=1)

        self.gauge = wx.Gauge(panel, -1, 100, size=(260,30), style=wx.GA_PROGRESSBAR)
        self.gauge.Hide()
        #self.sizer.Add(self.gauge, pos=(4, 2), flag=wx.LEFT, border=1)

        self.ctrl_process = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_NOHIDESEL)
        self.ctrl_process.SetEditable(False)
        #self.ctrl_process.Enable(False)
        self.sizer.Add(self.ctrl_process, pos=(6, 0), span=(1, 5),flag=wx.LEFT|wx.EXPAND, border=15)

        self.btn_quit = wx.Button(panel,label=u'退出')
        self.sizer.Add(self.btn_quit, pos=(7, 0), span=(1, 5),flag=wx.LEFT, border=15)

        self.sizer.Add(wx.StaticText(panel,label=''), pos=(8,0))

        #sizer.AddGrowableCol(1)
        self.sizer.AddGrowableCol(1)
        #sizer.AddGrowableCol(3)
        self.sizer.AddGrowableRow(6)

        panel.SetSizer(self.sizer)
        
        self.icon = wx.Icon('app.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        #=======================================================================
        # statusbar = self.CreateStatusBar()
        # statusbar.SetStatusText('....')
        #=======================================================================

    def BindEvent(self):
        self.btn_file.Bind(wx.EVT_BUTTON, self.OnFileLoad)
        self.btn_output.Bind(wx.EVT_BUTTON,self.OnDirectoryLoad)
        self.btn_launch.Bind(wx.EVT_BUTTON,self.OnLaunchClick)
        self.btn_watch_result.Bind(wx.EVT_BUTTON,self.OnWatchResultClick)
        self.btn_quit.Bind(wx.EVT_BUTTON,self.OnExit)

        self.cbx_lua3_x.Bind(wx.EVT_CHECKBOX, self.OnLuaVersionChecked)
        self.cbx_lua4_0.Bind(wx.EVT_CHECKBOX, self.OnLuaVersionChecked)
        
        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def OnFileLoad(self,event):
        self.ctrl_input.SetValue('')
        dialog = wx.FileDialog(self, "Open file...", os.getcwd(), style=wx.OPEN | wx.FD_MULTIPLE, wildcard="*.*")
        if dialog.ShowModal() == wx.ID_OK:
            for file in dialog.GetPaths():
                self.ctrl_input.AppendText(file)
                self.ctrl_input.AppendText(';')
            self.ctrl_input.SetValue(self.ctrl_input.GetValue()[:-1])
        dialog.Destroy()
    
    def OnDirectoryLoad(self,event):
        self.ctrl_output.SetValue('')
        dialog = wx.DirDialog(self, "Open directory...", os.getcwd(), style=wx.OPEN | wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.ctrl_output.SetValue(dialog.GetPath())
        dialog.Destroy()
        
    def OnResultFileLoad(self,event):
        self.ctrl_result.SetValue('')
        dialog = wx.FileDialog(self, "Open file...", os.getcwd(), style=wx.OPEN, wildcard="*.*")
        if dialog.ShowModal() == wx.ID_OK:
            self.ctrl_result.SetValue(dialog.GetPath())
        dialog.Destroy()

    def OnLaunchClick(self,event):
        apkFilePath = self.CheckInputFile()
        if None == apkFilePath:
            return
        targetDir = self.CheckOutputFile()
        self.ctrl_process.Clear()
        
        lua_version = '3.x' if self.cbx_lua3_x.GetValue() else '4.0'
        self.shade()
        
        self.repack_thread = repack.RepackThread(apkFilePath, targetDir,
                                                 save_log=self.cbx_log.GetValue(),
                                                 save_file=self.cbx_medium_file.GetValue(),
                                                 ctrl_process=self.ctrl_process,
                                                 lua_version=lua_version, cb=self.unshade)
        self.repack_thread.start()
        
        
    def CheckInputFile(self):
        apkFilePath = self.ctrl_input.GetValue().strip()
        if  apkFilePath == '':
            self.MessageBox(u'apk路径', u'apk路径是空的')
            return None
        else:
            if not os.path.exists(apkFilePath):
                self.MessageBox(u'apk路径', u'apk不存在')
                return None
            return apkFilePath

    def CheckOutputFile(self):
        outputFilePath = self.ctrl_output.GetValue().strip()
        if outputFilePath == '':
            return
        else:
            if not os.path.exists(outputFilePath):
                os.makedirs(outputFilePath)
        return os.path.realpath(outputFilePath)
        
    def OnWatchResultClick(self,event):
        result = self.ctrl_output.GetValue().strip()
        result = result.encode('gbk')
        if not result:
            self.MessageBox(u'保存路径', u'保存路径是空的')
            return
        if not os.path.exists(result):
            self.MessageBox(u'保存路径', result+u'不存在 ')
        else:
            #result = result.replace('\\','"\\"')
            #index = result.find('"')
            #result = result[:index] + result[index+1:]+'"'
            # os.system("start " + result)
            os.startfile(result)

    def OnLuaVersionChecked(self, event):
        cb = event.GetEventObject()
        if cb == self.cbx_lua3_x:
            self.cbx_lua4_0.SetValue(0 if self.cbx_lua3_x.GetValue() else 1)
        else:
            self.cbx_lua3_x.SetValue(0 if self.cbx_lua4_0.GetValue() else 1)
    
    def shade(self):
        self.ctrl_input.Disable()
        self.ctrl_output.Disable()
        self.btn_file.Disable()
        self.btn_output.Disable()
        self.btn_launch.Disable()
        self.cbx_lua3_x.Disable()
        self.cbx_lua4_0.Disable()
        self.cbx_log.Disable()
        self.cbx_medium_file.Disable()
        self.btn_launch.Disable()
        self.btn_quit.Disable()
    
    def unshade(self):
        self.ctrl_input.Enable()
        self.ctrl_output.Enable()
        self.btn_file.Enable()
        self.btn_output.Enable()
        self.btn_launch.Enable()
        self.cbx_lua3_x.Enable()
        self.cbx_lua4_0.Enable()
        self.cbx_log.Enable()
        self.cbx_medium_file.Enable()
        self.btn_launch.Enable()
        self.btn_quit.Enable()
        
    def MessageBox(self, title, text, style=wx.OK | wx.ICON_ERROR):
        message_dlg = wx.MessageDialog(None, text, title, style)
        message_dlg.ShowModal()
        message_dlg.Destroy()
    
    def OnExit(self, event):
        try:
            self.repack_thread.kill_subprocess()
        except:
            pass
        # use close instead destory
        self.Destroy()


    
app = wx.App()
Repack(None, title="Repack1.1")
app.MainLoop()
