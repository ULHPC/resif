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

#######################################################################################################################

# Installs the software sets.
def build(hashTable):
	# Assume that the MODULEPATH is already set to a correct value
    easybuild = hashTable['easybuild_module']
        
    stream = file(hashTable['swsets_config'], 'r')
    swsets = yaml.load(stream)

    # We define the options that are going to be passed to EasyBuild
    sharedOptions = defineSharedOptions(hashTable)

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
    	
        installed = False
    	# If it actually exist in the yaml file, we install the listed software.
    	if swset in swsets:
    	    for software in swsets[swset]:
                sys.stdout.write("Now starting to install " + software[:-3] + "\n")
                start = time.time()
    	        process.stdin.write('eb ' + software + installpath + sharedOptions + ' --robot\n')
    	        # Command to have at the end of the output the execution code of the last command
    	        process.stdin.write('echo $?\n')
    	        out = ""
    	        while True:
    	            out = process.stdout.readline()
                    if re.search("\(module found\)", out) == None:
                        installed = True
    	            try:
    	                i = int(out)
    	            except ValueError:
    	                i = -1
    	            if i < 0:
    	                sys.stdout.write(out)
    	            else:
    	                if i == 0:
                            if installed:
                                end = time.time()
                                duration = end - start
                                durationStr = writeTime(hashTable, software, duration)
                                sys.stdout.write('Successfully installed ' + software[:-3] + ' (duration of the build: ' + durationStr + ')\n')
                            else:
                                sys.stdout.write(software[:3] + " was already installed. Nothing to be done.")
    	                else:
    	                    sys.stdout.write('Failed to install ' + software[:-3] + '\n' + 'Operation failed with return code ' + out + '\n')
    	                    exit(out)
    	                break
    	
    	    sys.stdout.write("Finishing EasyBuild software installation step.\n")
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
    # An installpath has to be provided. If not we do not let the install continue 
    # (so that it doesn't install at an unknown location)
    if 'installdir' in hashTable:
        installpath = ' --installpath=' + os.path.join(hashTable['eb_installpath'], swset)
    elif 'rootinstall' in hashTable:
        installpath = ' --installpath=' + os.path.join(hashTable['rootinstall'], swset)
    else:
        try:
            os.environ['EASYBUILD_INSTALLPATH']
        except KeyError:
            sys.stdout.write("\
No information on where to install the softwares has been found. Please provide this information.\n\
To do so, either:\n\
- use the --rootinstall option to define the root directory of the EasyBuild install.\n\
- set the RESIF_ROOTINSTALL environement variable to define the same information.\n\
- set the rootinstall field in your configuration file if you are providing one. (using the --configfile option)\n\
- use the --installdir option to define an alternative place to install (modules will be installed in <eb-installpath>/<swset>/modules)\n\
- set the RESIF_INSTALLDIR environement variable to define the same information.\n\
- set the installdir field in your configuration file if you are providing one. (using the --configfile option)\n\
- set the EASYBUILD_INSTALLPATH environment variable to give the exact installpath in the meaning of EasyBuild.\n\
")
            exit(10)

    return installpath


# Take a duration and write it in the easyconfig file in the easyconfig repsitory.
def writeTime(hashTable, software, duration):
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    durationFormated = "%d:%d:%d" % (h, m, s)

    softwareDir = re.match("^[^⁻]*", software)

    # If no repositorypath was given, we should write at the default location for EasyBuild (find the location)
    if "eb_repositorypath" in hashTable:
        with open(os.path.join(os.path.join(os.path.abspath(os.path.expandvars(hashTable['eb_repositorypath'])), softwareDir), software), "a") as f:
            f.write("\n\nThis software build duration was: " + durationFormated + "\n")
            f.write("It was build on " + time.strftime("%c") + "\n")

    return durationFormated

#######################################################################################################################