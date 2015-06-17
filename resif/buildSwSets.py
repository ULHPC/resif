#######################################################################################################################
# Author: Maxime Schmitt
# Mail: maxime.schmitt@telecom-bretagne.eu
# Overview: Module that take care of installing a given software set using a given EasyBuild module.
#######################################################################################################################

import os
import sys
import subprocess
import yaml
import time
import re
import glob

#######################################################################################################################

# Installs the software sets.
def build(hashTable):
	# Assume that the MODULEPATH is already set to a correct value
    easybuild = hashTable['easybuild_module']
    
    if "swsets_config" in hashTable:
        stream = file(hashTable['swsets_config'], 'r')
    else:
        stream = hashTable["git_tree"]['config/swsets.yaml'].data_stream.read()

    swsets = yaml.load(stream)

    # We define the options that are going to be passed to EasyBuild
    sharedOptions = defineSharedOptions(hashTable)

    # We use the additional options if any
    if 'eb_options' in hashTable:
        additionalOptions = " " + hashTable["eb_options"]
    else:
        additionalOptions = ""

    for swset in hashTable['swsets']:
        # We set the installpath. If there is no installpath given, we stop the execution.
        installpath = setInstallpath(hashTable, swset)

        # We add the place where the software will be installed to the MODULEPATH for the duration of the installation
        # so that EasyBuild will not instantly forget that it has installed them after it is done (problematic for dependency resolution)
        # Part for environment-modules (come later for Lmod)
        if hashTable["module_cmd"] == "modulecmd":
            try:
                os.environ['MODULEPATH'] = ':'.join([os.environ['MODULEPATH'], os.path.join(os.path.join(installpath[15:], 'modules'), 'all')])
            except KeyError:
                os.environ['MODULEPATH'] = os.path.join(os.path.join(installpath, 'modules'), 'all')
    	
    	process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    	process.stdin.write('module load ' + easybuild + '\n')

        # Lmod part for MODULEPATH management
        if hashTable["module_cmd"] == "lmod":
            process.stdin.write("module use " + os.path.join(os.path.join(installpath[15:], 'modules'), 'all') + "\n")
    	
        alreadyInstalled = False
    	# If it actually exist in the yaml file, we install the listed software.
    	if swset in swsets:
            swsetStart= time.time()
    	    for software in swsets[swset]:
                sys.stdout.write("Now starting to install " + software[:-3] + "\n")
    	        process.stdin.write('eb ' + software + installpath + sharedOptions + additionalOptions + ' --robot\n')
    	        # Command to have at the end of the output the execution code of the last command
    	        process.stdin.write('echo $?\n')
    	        out = ""
    	        while True:
    	            out = process.stdout.readline()
                    if re.search("\(module found\)", out) != None:
                        alreadyInstalled = True
    	            try:
    	                i = int(out)
    	            except ValueError:
    	                i = -1
    	            if i < 0:
    	                sys.stdout.write(out)
    	            else:
    	                if i == 0:
                            if alreadyInstalled:
                                sys.stdout.write(software[:-3] + " was already installed. Nothing to be done.\n")
                                alreadyInstalled = False
                            else:
                                sys.stdout.write('Successfully installed ' + software[:-3] + '.\n')
    	                else:
    	                    sys.stdout.write('Failed to install ' + software[:-3] + '\n' + 'Operation failed with return code ' + out + '\n')
    	                    exit(out)
    	                break
            if swset != 'core':
                swsetModulefileCreator(hashTable, installpath[15:], swset)
            swsetEnd = time.time()
            swsetDuration = swsetEnd - swsetStart
            m, s = divmod(swsetDuration, 60)
            h, m = divmod(m, 60)
            swsetDurationStr = "%d:%d:%d" % (h, m, s)
    	    sys.stdout.write("Software set " + swset + " Successfully installed. Build duration: " + swsetDurationStr + ".\n")
    	# If it doesn't, we print an error message as well as an help to use the script.
    	else:
    	    sys.stdout.write("Error: Invalid set of software.\nYou asked for the software set named " + swset  + \
    	    	" to be installed but it wasn't found in your software set configuration file.\n")
    	    sys.stdout.write("The configuration file location is: " + os.path.abspath(hashTable['swsets_config']) + \
    	    	" and the software sets found in it are:\n")
    	    for k in swsets.iteritems():
    	        sys.stdout.write("- " + k[0] + "\n")
    	    exit(20)


# Defines options to pass to EasyBuild and return them in a string.
def defineSharedOptions(hashTable):
    options = ""

    if 'eb_sourcepath' in hashTable:
        options += ' --sourcepath=' + os.path.abspath(os.path.expandvars(hashTable['eb_sourcepath']))
    if 'eb_buildpath' in hashTable:
        options += ' --buildpath=' + os.path.abspath(os.path.expandvars(hashTable['eb_buildpath']))
    if 'eb_repository' in hashTable:
        options += ' --repository=' + hashTable['eb_repository']
    if 'eb_repositorypath' in hashTable:
        options += ' --repositorypath=' + os.path.abspath(os.path.expandvars(hashTable['eb_repositorypath']))
    if 'mns' in hashTable:
        options += ' --module-naming-scheme=' + hashTable['mns']

    # If this file doesn't exist, it wont crash, EasyBuild will just ignore it and use other sources for the 
    # options (default config file and so on).
    if 'out_place' in hashTable and hashTable['out_place']:
        easybuild_config = os.path.join(os.path.join(hashTable['srcpath'], 'config'), 'easybuild-out-place.cfg')
    else:
        easybuild_config = os.path.join(os.path.join(hashTable['srcpath'], 'config'), 'easybuild.cfg')
    options += ' --configfile=' + easybuild_config

    return options


# Return the installpath for the given swset.
def setInstallpath(hashTable, swset):
    installpath = ""
    # An installpath has to be provided, if not explicitely specified we use the rootinstall.
    if 'installdir' in hashTable:
        installpath = ' --installpath=' + os.path.join(hashTable['installdir'], swset)
    elif 'rootinstall' in hashTable:
        installpath = ' --installpath=' + os.path.join(hashTable['rootinstall'], swset)
    else:
        sys.stdout.write("\
No information on where to install the softwares has been found. Please provide this information.\n\
To do so, either:\n\
- use the --rootinstall option to define the root directory of the EasyBuild install.\n\
- set the RESIF_ROOTINSTALL environement variable to define the same information.\n\
- set the rootinstall field in your configuration file if you are providing one. (using the --configfile option)\n\
- use the --installdir option to define an alternative place to install (modules will be installed in <eb-installpath>/<swset>/modules)\n\
- set the RESIF_INSTALLDIR environement variable to define the same information.\n\
- set the installdir field in your configuration file if you are providing one. (using the --configfile option)\n\
")
        exit(10)

    return installpath

# For a given logfile we get the name of the software, the start and end dates of the build and convert them to timestamp and then determine the duration of the build.
def getSoftwareBuildTimes(logfile):
    logfileReduced = re.search("[^/]*$", logfile).group(0)
    software = re.findall("-.*-", logfileReduced)[0][1:-1]
    with open(logfile, "r") as log:
        raw = log.readlines()
        stime = "%s %s"%(raw[0].split()[1],raw[0].split()[2])
        stime = time.mktime(time.strptime(stime[:-4], "%Y-%m-%d %H:%M:%S"))
        etime = "%s %s"%(raw[-1].split()[1],raw[-1].split()[2])
        etime = time.mktime(time.strptime(etime[:-4], "%Y-%m-%d %H:%M:%S"))
        softwareDuration = etime - stime
        
    return (software, softwareDuration)

# Create a module file and the associated symlink (if not already existing) to load the software set and put them at the right places.
def swsetModulefileCreator(hashTable, installpath, moduleName):
    if 'installdir' in hashTable:
        modulesDirPath = os.path.join(os.path.join(hashTable['installdir'], 'core'), 'modules')
    else:
        modulesDirPath = os.path.join(os.path.join(hashTable['rootinstall'], 'core'), 'modules')
    # Adapt the location of the modulfile to the chosen MNS
    if hashTable['mns'] == "ThematicMNS":
        # We create the directories we need to install EasyBuild
        EBmoduleDir = os.path.join('base', 'swsets')
        easybuildPath = os.path.join(os.path.join(modulesDirPath, 'all'), EBmoduleDir)
        if not os.path.exists(easybuildPath):
            os.makedirs(easybuildPath)
        easybuildPath = os.path.join(os.path.join(modulesDirPath, 'base'), EBmoduleDir)
        if not os.path.exists(easybuildPath):
            os.makedirs(easybuildPath)

    else:
        # We create the directories we need to install EasyBuild
        EBmoduleDir = 'swsets'
        easybuildPath = os.path.join(os.path.join(modulesDirPath, 'all'), EBmoduleDir)
        if not os.path.exists(easybuildPath):
            os.makedirs(easybuildPath)
        easybuildPath = os.path.join(os.path.join(modulesDirPath, 'base'), EBmoduleDir)
        if not os.path.exists(easybuildPath):
            os.makedirs(easybuildPath)

    # Path to the actual module file
    moduleFilePath = os.path.join(os.path.join(os.path.join(modulesDirPath, 'all'), EBmoduleDir), moduleName)

    with open(moduleFilePath, "w") as f:
        f.write("\
#%Module\n\
\n\
proc ModulesHelp { } {\n\
    puts stderr {   " + moduleName + " software set.\n\
}\n\
}\n\
module-whatis {" + moduleName + " software set.\n\
}\n\
set root        " + installpath + "\n\
prepend-path    MODULEPATH      \"$root/modules/all\"\n\
")
    
    # Path to the symlink to the module file.
    symlinkPath = os.path.join(os.path.join(os.path.join(modulesDirPath, 'base'), EBmoduleDir), moduleName)
    if not os.path.exists(symlinkPath):
        os.symlink(moduleFilePath, symlinkPath)

#######################################################################################################################
