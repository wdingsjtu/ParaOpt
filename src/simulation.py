#
#   simulation.py
#
# Created:  2016/Jan/29
# Purpose:  Deal with simulation, including post-processing.
# Notes:
#
# -------------------------------------------------------------------------- #

from __future__ import print_function

import fileinput
import os
import subprocess


# -------------------------------------------------------------------------- #

class Simulation(object):
    def __init__(self, simuPath, postScript=None):
        self.path = os.path.abspath(simuPath)
        self.script = postScript
        self.execpath = os.getcwd()
        if not os.path.exists(self.path):
            raise ValueError("Simulation path '%s' doesn't exist." %self.path)

    def run(self, command):
        """ Execute the input command (command).

        command: command to run the simulation;

        type_command: str
        rtype: None
        """
        os.chdir(self.path)
        logFile = open("log.screen", "wt")
        try:
            subprocess.check_call(command, stdout=logFile, shell=True)
            logFile.close()
        except subprocess.CalledProcessError:
            logFile.close()
            os.remove("log.screen")
            raise ValueError("Command fails to run: %s" % command)
        # TODO
        #      1) command on windows
        #      2) Be careful about 'shell-True'.
        os.chdir(self.execpath)

    def post_process(self, scriptFileName=None):
        # TODO why not return list??
        """ Post-process the simulation data by calling your script file.
        Return all properties' value as a list.

        scriptFileName: the post-processing script ('self.script' by default).
            It should process the data produced by the simulation, and save
            all targeted property values in a single line file, named as
            "res.postprocess" like this:
                "Q1 Q2 Q3 Q4 ...".

        type_scriptFileName: str
        rtype: str list
        """
        os.chdir(self.path)
        if not scriptFileName:
            scriptFileName = self.script
        if not scriptFileName:
            raise ValueError("Post-process file not provided.")
        if not os.path.exists(scriptFileName):
            raise ValueError("Post-processing Script '%s' doesn't exists." %s)

        print("Results being processed by: \"%s\" " % scriptFileName)
        subprocess.check_call(
            './%s' %scriptFileName,
            shell=True,
        )
        resFile = fileinput.FileInput(os.path.join(self.path, 'res.postprocess'))
        result = resFile.readline()
        print("Current properties:", result)
        os.chdir(self.execpath)
        return result.split()

        # TODO def back_up_simulation_files(self, anyFilesName, destination):
