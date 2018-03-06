#-*-coding:utf8 -*-

from threading import Thread
import entry
import sys
import log_utils
import os
import time
from config import ConfigParse
import signal

class RepackThread(Thread):
    def __init__(self, apk_path, output_path, save_log=False, save_file=False, ctrl_process=None, lua_version='3.x', cb=None):
        Thread.__init__(self)
        self.apk_path = apk_path
        self.output_path = output_path
        self.ctrl_process = ctrl_process
        
        self.lua_version = lua_version
        self.cb = cb
        
        self.save_log = save_log
        self.save_file = save_file
        self.old_stdout= sys.stdout
        self.old_stderr = sys.stderr
    
    def run(self):
        sys.stdout = self.ctrl_process
        sys.stderr = self.ctrl_process
        
        for h in log_utils.getLogger().handlers:
            log_utils.getLogger().removeHandler(h)
        
        ctrl_handler = log_utils.WxTextCtrlHandler(self.ctrl_process)
        log_utils.getLogger().addHandler(ctrl_handler)

        timestamp_str = str(time.time())
        if self.save_log:
            myFH = log_utils.MyFileHandler(filename=os.path.join(self.output_path, timestamp_str, 'repack.log'))
            # myFH.setLevel(log_utils.FILE_HANDLER_LEVEL)
            myFH.setFormatter(log_utils.formatter)
            log_utils.getLogger().addHandler(myFH)
        
        argjson = entry.windowsDebugJson(self.apk_path, self.output_path, self.save_log, self.save_file,
                                         timestamp=timestamp_str, lua_version=self.lua_version)
        entry.php_entry(argjson)
        self.ctrl_process.AppendText("Completed!\n\n\n")
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

        if self.cb:
            self.cb()
            
    def kill_subprocess(self):
        p = ConfigParse.shareInstance().getCurrentSubProcess()
        #=======================================================================
        # process = psutil.Process(p.pid)
        # for proc in process.get_children(recursive=True):
        #     proc.kill()
        # process.kill()
        #=======================================================================
        #os.system("taskkill /PID %s /F" % p.pid)
        os.kill(p.pid, signal.CTRL_C_EVENT)
