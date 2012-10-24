import sublime
import sublime_plugin

import os
import re


def get_makefile(filename):
    dirname = os.path.dirname(filename)
    while dirname != "/":
        mf = os.path.join(dirname, "Makefile")
        print "Checking %s" % mf
        if os.path.exists(mf):
            if os.path.isfile(mf):
                return mf
        dirname = os.path.dirname(dirname)
    raise Exception("No Makefile found")


def get_targets(mf):
    targets = []
    targetp = re.compile("^([^=% ]*) *:.*")
    for line in open(mf):
        m = targetp.match(line)
        if m != None:
            targets.append(m.group(1))
    return targets


class DynMakeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.edit = edit

        self.makefile = get_makefile(self.view.file_name())
        self.targets = get_targets(self.makefile)

        self.view.window().show_quick_panel(self.targets, self.done)

    def done(self, picked):
        if picked == -1:
            return
            #self.view.insert(self.edit, 0, "canceled")

        #self.view.insert(self.edit, 0, self.targets[picked])
        self.view.window().run_command("exec", {"cmd": ["make", self.targets[picked]], 
                                                "working_dir": os.path.dirname(self.makefile)})
