#######################################################################################################################
# Author: Maxime Schmitt
# Mail: maxime.schmitt@telecom-bretagne.eu
# Overview: Module that take care of bootstraping EasyBuild.
#######################################################################################################################

import os
import re
import sys
import shutil
import subprocess

sys.path.append('.')
from configManager import getEasyBuildVersion

#######################################################################################################################
# Function that do the bootstrap using the other functions of this module and return the associated modulePath.
def bootstrap(hashTable):

	# We install all the necessary files of EasyBuild.
	easybuildFilesInstaller(hashTable)

	# We create the modulefile of EasyBuild.
	eb_version = getEasyBuildVersion(hashTable['rootinstall'])
	modulefileCreator(hashTable, "install-" + eb_version)

	# We create some files to source to rapidly start using the bootstrap module and the associated softwares.
	modulePath = sourcefileCreator(hashTable)

	return modulePath

#######################################################################################################################


#######################################################################################################################
# Functions that do the different important tasks of the bootstrap.

# Get and put at the right place all the EasyBuild files.
def easybuildFilesInstaller(hashTable):
	# We create the directory that we need to install the EasyBuild sources
	easyBuildDir = os.path.join(hashTable['rootinstall'], '.installRef')
	if not os.path.exists(easyBuildDir):
		os.makedirs(easyBuildDir)

	altSources = {}
	# If we were provided alternative sources for the EasyBuild files, we create the useful variables
	if any(True for x in ['gh_ebuser', 'git_ebframework', 'git_ebblocks', 'git_ebconfigs'] if x in hashTable):
		if 'gh_ebuser' in hashTable:
			altSources['easybuild-framework'] = ('https://github.com/' + hashTable['gh_ebuser'] + '/easybuild-framework.git', \
				hashTable['branch_ebframework'] if 'branch_ebframework' in hashTable else None)

			altSources['easybuild-easyblocks'] = ('https://github.com/' + hashTable['gh_ebuser'] + '/easybuild-easyblocks.git', \
				hashTable['branch_ebblocks'] if 'branch_ebblocks' in hashTable else None)

			altSources['easybuild-easyconfigs'] = ('https://github.com/' + hashTable['gh_ebuser'] + '/easybuild-easyconfigs.git', \
				hashTable['branch_ebconfigs'] if 'branch_ebconfigs' in hashTable else None)

		if 'git_ebframework' in hashTable:
			altSources['easybuild-framework'] = (hashTable['git_ebframework'], hashTable['branch_ebframework'] if 'branch_ebframework' in hashTable else None)
	
		for v in ['blocks', 'configs']:
			if 'git_eb'+v in hashTable:
				altSources['easybuild-easy'+v] = (hashTable['git_eb'+v], hashTable['branch_eb'+v] if 'branch_eb'+v in hashTable else None)

	# Import any alternative EasyBuild files from given sources
	for k,v in altSources.iteritems():
		if v[1] != None:
			subprocess.check_call(['git', 'clone', v[0], '-b', v[1], '--single-branch', os.path.join(os.path.join(hashTable['rootinstall'], '.installRef'), k)])
		else:
			subprocess.check_call(['git', 'clone', v[0], os.path.join(os.path.join(hashTable['rootinstall'], '.installRef'), k)])

	# Complete the EasyBuild files with the ones from the subtree if necessary
	if any(True for x in ['easybuild-framework', 'easybuild-easyblocks', 'easybuild-easyconfigs'] if not x in altSources):
		pwd = os.getcwd()
		os.chdir(hashTable['srcpath'])

		for k in ['easybuild-framework', 'easybuild-easyblocks', 'easybuild-easyconfigs']:
			if not k in altSources:
				originalBranch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])[:-1]
				if hashTable['release'] != 'HEAD':
					subprocess.check_call(['git', 'branch', k, hashTable['release']])
					subprocess.check_call(['git', 'checkout', k])
				elif 'branch' in hashTable:
					subprocess.check_call(['git', 'branch', k, hashTable['branch']])
					subprocess.check_call(['git', 'checkout', k])
				else:
					subprocess.check_call(['git', 'branch', k])
				subprocess.check_call(['git', 'filter-branch', '-f', '--subdirectory-filter', 'easybuild/'+k, k])
				subprocess.check_call(['git', 'clone', hashTable['srcpath'], '-b', k, '--single-branch', os.path.join(os.path.join(hashTable['rootinstall'], '.installRef'), k)])
				subprocess.check_call(['git', 'checkout', originalBranch])
				subprocess.check_call(['git', 'branch', '-D', k])

		os.chdir(pwd)

	# Adding vsc-base from the hpcugent git repository
	subprocess.check_call(['git', 'clone', 'https://github.com/hpcugent/vsc-base.git', os.path.join(os.path.join(hashTable['rootinstall'], '.installRef'), 'vsc-base')])


# Create the EasyBuild module file and the associated symlink and put them at the right places.
# If the ThematicMNS module naming scheme is used, it is also installed.
def modulefileCreator(hashTable, moduleName):
	modulesDirPath = os.path.join(os.path.join(hashTable['rootinstall'], 'core'), 'modules')
	# Adapt the location of the modulfile to the chosen MNS
	if hashTable['mns'] == "ThematicMNS":
		# We create the directories we need to install EasyBuild
		EBmoduleDir = os.path.join('base', 'EasyBuild')
		easybuildPath = os.path.join(os.path.join(modulesDirPath, 'all'), EBmoduleDir)
		if not os.path.exists(easybuildPath):
			os.makedirs(easybuildPath)
		easybuildPath = os.path.join(os.path.join(modulesDirPath, 'base'), EBmoduleDir)
		if not os.path.exists(easybuildPath):
			os.makedirs(easybuildPath)
		# We install the ThematicMNS
		setThematicMNS(hashTable)

	else:
		# We create the directories we need to install EasyBuild
		EBmoduleDir = 'EasyBuild'
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
	puts stderr {   EasyBuild is a software build and installation framework\n\
written in Python that allows you to install software in a structured,\n\
repeatable and robust way. - Homepage: http://hpcugent.github.com/easybuild/\n\
This module provides the development version of EasyBuild.\n\
}\n\
}\n\
module-whatis {EasyBuild is a software build and installation framework\n\
written in Python that allows you to install software in a structured,\n\
repeatable and robust way. - Homepage: http://hpcugent.github.com/easybuild/\n\
This module provides the development version of EasyBuild.\n\
}\n\
set root    " + os.path.join(hashTable['rootinstall'], '.installRef') + "\n\
conflict    EasyBuild\n\
prepend-path    PATH            \"$root/easybuild-framework\"\n" \
+ ("\nprepend-path    PYTHONPATH      \"$root/MNS\"\n" if hashTable['mns'] == 'ThematicMNS' else "\n") + \
"prepend-path    PYTHONPATH      \"$root/easybuild-framework\"\n\
prepend-path    PYTHONPATH      \"$root/easybuild-easyblocks\"\n\
prepend-path    PYTHONPATH      \"$root/easybuild-easyconfigs\"\n\
prepend-path    PYTHONPATH      \"$root/vsc-base/lib\"\n\
")
	
	# Path to the symlink to the module file.
	symlinkPath = os.path.join(os.path.join(os.path.join(modulesDirPath, 'base'), EBmoduleDir), moduleName)
	os.symlink(moduleFilePath, symlinkPath)


# Install the ThematicMNS module naming scheme.
def setThematicMNS(hashTable):
	mnsroot = os.path.join(os.path.join('.installRef', 'MNS'), 'easybuild')
	
	# Extends the Python path in such a way that we included this architecture in the easybuild namespace.
	mnsPath = os.path.join(hashTable['rootinstall'], os.path.join(os.path.join(mnsroot, 'tools'), 'module_naming_scheme'))
	if not os.path.exists(mnsPath):
		os.makedirs(mnsPath)
	with open(os.path.join(mnsPath, '__init__.py'), "w") as f:
		f.write("\
from pkgutil import extend_path\n\
__path__ = extend_path(__path__, __name__)\n\
")
	shutil.copyfile(os.path.join(mnsPath, '__init__.py'), \
		os.path.join(os.path.join(os.path.join(hashTable['rootinstall'] ,mnsroot), 'tools'), '__init__.py'))
	shutil.copyfile(os.path.join(mnsPath, '__init__.py'), \
		os.path.join(os.path.join(hashTable['rootinstall'], mnsroot), '__init__.py'))

	# Import the module naming scheme
	thematicStr = hashTable['git_tree']['bin/ThematicMNS.py'].data_stream.read()
	with open(os.path.join(mnsPath, 'ThematicMNS.py'), 'w') as f:
		f.write(thematicStr)


# Create some files to source to easily start using the EasyBuild module and the associated softwares.
# These files are put in the <rootinstall> directory.
def sourcefileCreator(hashTable):
	trueVersion = os.path.basename(hashTable['rootinstall'])
	# Variable containing all the required path for the MODULEPATH
	modulePath = ""
	moduleClasses = ['bio', 'cae', 'chem', 'compiler', 'data', 'debugger', 'devel', 'geo', 'lang', 'lib', 'math', \
	'mpi', 'numlib', 'perf', 'phys', 'system', 'toolchain', 'tools', 'vis', 'base']
	for moduleclass in moduleClasses:
		modulePath += os.path.join(os.path.join(os.path.join('$RESIF_ROOTINSTALL', 'core'), 'modules'), moduleclass) + ":"

	prependModulepath = (hashTable['prepend_modulepath'] + ":") if 'prepend_modulepath' in hashTable else ""
	appendModulepath = hashTable['append_modulepath'] if 'append_modulepath' in hashTable else ""
	modulePath = prependModulepath + modulePath + appendModulepath

	# We create the files to source to use the infrastructure.
	# The admin file is there to easily add software in the ulhpc swset without any manual changes to the config.
	with open(os.path.join(hashTable['rootinstall'], "LOADME-" + trueVersion + ".sh"), "w") as f:
		modulevar = "export EASYBUILD_MODULES_TOOL=Lmod" if hashTable["module_cmd"] == "lmod" else "#export EASYBUILD_MODULES_TOOL=Lmod"
		f.write("\
export RESIF_ROOTINSTALL=" + hashTable['rootinstall'] + "\n\
export MODULEPATH=" + modulePath + "\n\
" + modulevar + "\n\
export EASYBUILD_MODULE_NAMING_SCHEME=" + hashTable['mns'] + "\n\
export RESIF_OUT_PLACE=False\n\
")
	# The user file is there to easily add software locally without any manual change to the config.
	with open(os.path.join(hashTable['rootinstall'], "LOADME-" + trueVersion + "-out-place.sh"), "w") as f:
		modulevar = "export EASYBUILD_MODULES_TOOL=Lmod" if hashTable["module_cmd"] == "lmod" else "#export EASYBUILD_MODULES_TOOL=Lmod"
		f.write("\
export RESIF_ROOTINSTALL=" + hashTable['rootinstall'] + "\n\
export MODULEPATH=" + modulePath + "\n\
" + modulevar + "\n\
export EASYBUILD_MODULE_NAMING_SCHEME=" + hashTable['mns'] + "\n\
export RESIF_OUT_PLACE=True\n\
")
	
	return modulePath

#######################################################################################################################