#######################################################################################################################
# Author: Maxime Schmitt
# Mail: maxime.schmitt@telecom-bretagne.eu
# Overview: Module that combines all the other modules and provides a CLI.
#######################################################################################################################

import sys
import click
import os
import subprocess
import shutil
import time
import glob

sys.path.append('.')
import configManager
import bootstrapEB
import buildSwSets

import pkg_resources

#######################################################################################################################
# The resif group. Defines the name of the command. It is the "main" group.
@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--version', flag_value=True, help='Return the version of this script.')
def resif(ctx, version):
    """
    RESIF commandline interface.

    Choose the sub-command you want to execute.
    """
    if ctx.invoked_subcommand is None:
        if version:
            sys.stdout.write("This is RESIF version " + pkg_resources.require("resif")[0].version + "\n")
        else:
            subprocess.check_call(['resif', '--help'])
        
#######################################################################################################################


#######################################################################################################################
# The init, update and wipe subcommands, to initialize, update and reset the environment concerning RESIF

# Initialize the necessary directories
@resif.command(short_help='Initialize the git repository in the srcpath.')
@click.option('--git-architecture', 'git_architecture', envvar='RESIF_GIT_ARCHITECTURE', help='Defines an alternative git repository URL or absolute path to get the architecture from.')
@click.option('--srcpath', 'srcpath', envvar='RESIF_SRCPATH', help='Defines an alternative path to put the sources in.')
@click.option('--overwrite', 'overwrite', flag_value=True, envvar='RESIF_OVERWRITE', help='Set this flag if you want to overwrite any existing directories in the srcpath.')
def init(**kwargs):
    config = configManager.generateInitConfig(kwargs)
    if not os.path.isdir(config["srcpath"]) or config["overwrite"]:
        if config["overwrite"]:
            shutil.rmtree(config["srcpath"], True)
        subprocess.check_call(['git', 'clone', config['git_architecture'], config['srcpath']])
    else:
        sys.stdout.write("A repository already exist at your srcpath: " + config["srcpath"] +"\nPlease use the --overwrite flag if you want to overwrite this repository.\n" + "\033[93m" + "WARNING: This will remove everything at " + config["srcpath"] + "\033[0m\n")
        exit(50)

@resif.command(short_help='Update the git repository in the srcpath.')
@click.option('--srcpath', 'srcpath', envvar='RESIF_SRCPATH', help='Defines an alternative path to the repository.')
def update(**kwargs):
    config = configManager.generateUpdateConfig(kwargs)
    os.chdir(config['srcpath'])
    subprocess.check_call(['git', 'pull'])

@resif.command(short_help='Wipe all data in the srcpath.')
@click.option('--srcpath', 'srcpath', envvar='RESIF_SRCPATH', help='Defines an alternative path to the repository.')
@click.confirmation_option(prompt='You are going to remove everything in <srcpath> (default=$HOME/.resif/src), are you sure you want to continue ?', help='Use to not prompt confirmation message. (Check what you are trying to do before !)')
def wipe(**kwargs):
    config = configManager.generateWipeConfig(kwargs)
    try:
        shutil.rmtree(config['srcpath'])
    except OSError:
        sys.stdout.write("Nothing to remove at " + config['srcpath'] + "\n")

#######################################################################################################################


#######################################################################################################################
# The count and show subcommands which help getting informations such as
# "how many and which software have been compiled using X toolchain?"
# These functions need one of the "LOADME" files to be loaded.
# (At the very least, they require the module path to be set correctly to use the EasyBuild install and the RESIF_ROOTINSTALL variable to be set to the root of the EasyBuild install.)

# Show the list of softwares which easyconfig file contains the "content" string
@resif.command(short_help="Show all the easyconfigs which name contains the given pattern.")
@click.option('--rootinstall', envvar='RESIF_ROOTINSTALL', help='Path to the root of the EasyBuild installation (contains the various software sets deployed and the EasyBuild files).')
@click.option('--mns', envvar='EASYBUILD_MODULE_NAMING_SCHEME', type=click.Choice(['EasyBuildMNS', 'E', 'HierarchicalMNS', 'H', 'ThematicMNS', 'T']), help='Module Naming Scheme to be used.')
@click.option('--show-path', 'show_path', flag_value=True, envvar='RESIF_SHOW_PATH', help='Make the command to show the full path to the files listed.')
@click.argument('content')
def search(**kwargs):
    """
    [CONTENT] TEXT                  Text to look for in the names of
                                    the installed softwares.
    """
    try:
        if kwargs['mns'] == 'ThematicMNS' or kwargs['mns'] == 'T':
            easybuild_module = "base/EasyBuild/install-" + configManager.getEasyBuildVersion(os.path.expandvars(os.path.abspath(os.environ['RESIF_ROOTINSTALL'])))
        else:
            easybuild_module = 'EasyBuild/install-' + configManager.getEasyBuildVersion(os.path.expandvars(os.path.abspath(os.environ['RESIF_ROOTINSTALL'])))
    except Exception:
        sys.stdout.write("Please set the RESIF_ROOTINSTALL environment variable or the --rootinstall option to the root of the EasyBuild installation.\n")
        exit(1)
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.stdin.write('module load ' + easybuild_module + '\n')
    if kwargs['show_path']:
        process.stdin.write('eb -S ' + kwargs['content'] + " | grep '^[^=]' | sed 's#^ \* ##'\n")
    else:
        process.stdin.write('eb -S ' + kwargs['content'] + " | grep '^ \* ' | sed 's#.*/##'\n")
    process.stdin.write('echo $?\n')
    out = ""
    while True:
        out = process.stdout.readline()
        try:
            i = int(out)
        except ValueError:
            i = -1
        if i < 0:
            sys.stdout.write(out)
        else:
            break

#Count the number of easyconfig files that contain the given pattern in their name.
@resif.command(short_help="Count the number of easyconfig files that contain the given pattern in their name.")
@click.option('--rootinstall', envvar='RESIF_ROOTINSTALL', help='Path to the root of the EasyBuild installation (contains the various software sets deployed and the EasyBuild files).')
@click.option('--mns', envvar='EASYBUILD_MODULE_NAMING_SCHEME', type=click.Choice(['EasyBuildMNS', 'E', 'HierarchicalMNS', 'H', 'ThematicMNS', 'T']), help='Module Naming Scheme to be used.')
@click.argument('content')
def count(**kwargs):
    """
    \b
    [CONTENT] TEXT                  Text to look for in the names of
                                    the easyconfig files.
    """
    try:
        if kwargs['mns'] == 'ThematicMNS' or kwargs['mns'] == 'T':
            easybuild_module = "base/EasyBuild/install-" + configManager.getEasyBuildVersion(os.path.expandvars(os.path.abspath(kwargs['rootinstall'])))
        else:
            easybuild_module = 'EasyBuild/install-' + configManager.getEasyBuildVersion(os.path.expandvars(os.path.abspath(kwargs['rootinstall'])))
    except Exception:
        sys.stdout.write("Please set the RESIF_ROOTINSTALL environment variable or the --rootinstall option to the root of the EasyBuild installation.\n")
        exit(1)
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.stdin.write('module load ' + easybuild_module + '\n')
    process.stdin.write('eb -S ' + kwargs['content'] + ' | grep "^ \* " | wc -l' + '\n')
    sys.stdout.write(process.stdout.readline())


# Print the build duration of all the softwares in the given software set.
@resif.command(short_help="Print the build times of all the installed software of a given software set.")
@click.option('--rootinstall', envvar='RESIF_ROOTINSTALL', help='Path to the root of the EasyBuild installation (contains the various software sets deployed and the EasyBuild files).')
@click.option('--seconds', flag_value=True, envvar='RESIF_SECONDS', help='Set this flag if you want the software build time output to be in seconds (not formated).')
@click.argument('swset')
def buildTimeSwSet(**kwargs):
    """
    [SWSET] TEXT        Software set to consider.
    """
    files = glob.glob(kwargs['rootinstall']+'/'+kwargs['swset']+'/software/*/*/*/easybuild/*log')
    coreTime = 0
    if files != []:
        for logfile in files:
            software, softwareDuration = buildSwSets.getSoftwareBuildTimes(logfile)
            coreTime += softwareDuration
            if kwargs['seconds']:
                sys.stdout.write(software + "\t" + str(softwareDuration) + "\n")
            else:
                m, s = divmod(softwareDuration, 60)
                h, m = divmod(m, 60)
                softwareDurationFormated = "%d:%d:%d" % (h, m, s)
                sys.stdout.write(software + "\t" + softwareDurationFormated + "\n")
        # Output the build time of the whole software set.
        if kwargs['seconds']:
            sys.stdout.write("core software set\t" + str(coreTime) + "\n")
        else:
            m, s = divmod(coreTime, 60)
            h, m = divmod(m, 60)
            coreTimeStr = "%d:%d:%d" % (h, m, s)
            sys.stdout.write("core software set\t" + coreTimeStr + "\n")
    else:
        sys.stdout.write("No software found.\n")
        exit(80)


# Print the build durations of all the versions of the given software if it is found.
@resif.command(short_help="Print the build time of of a given installed software from a specific software set.")
@click.option('--rootinstall', envvar='RESIF_ROOTINSTALL', help='Path to the root of the EasyBuild installation (contains the various software sets deployed and the EasyBuild files).')
@click.option('--seconds', flag_value=True, envvar='RESIF_SECONDS', help='Set this flag if you want the software build time output to be in seconds (not formated).')
@click.argument('swset')
@click.argument('software')
def buildTimeSoftware(**kwargs):
    """
    \b
    [SWSET] TEXT        Software set to consider.
    [SOFTWARE] TEXT     Software name to consider.
    """
    softwareFound = False
    files = glob.glob(kwargs['rootinstall']+'/'+kwargs['swset']+'/software/*/*/*/easybuild/*log')
    for logfile in files:
        software, softwareDuration = buildSwSets.getSoftwareBuildTimes(logfile)
        if software.lower() == kwargs['software'].lower():
            softwareFound = True
            if kwargs['seconds']:
                sys.stdout.write(software + "\t" + str(softwareDuration) + "\n")
            else:
                m, s = divmod(softwareDuration, 60)
                h, m = divmod(m, 60)
                softwareDurationFormated = "%d:%d:%d" % (h, m, s)
                sys.stdout.write(software + "\t" + softwareDurationFormated + "\n")
            # We do not exit() since there may be multiple version of the same software.
    if not softwareFound:
        sys.stdout.write("The software you asked for has not been found. This software is either not installed or in another software set.\n")
        exit(90)

#######################################################################################################################


#######################################################################################################################
# The subcommands bootstrap, build and cleaninstall.

# Make a new install of EasyBuild.
@resif.command(short_help='Deploy a fresh EasyBuild install.')
# Path to the source directory
@click.option('--srcpath', envvar='RESIF_SRCPATH', help='Source path to the RESIF directory.')
# Configuration files provisioning
@click.option('--configfile', envvar='RESIF_CONFIGFILE', help='Specify path to a config file to load.')
# git variables
@click.option('--gh-ebuser', 'gh_ebuser', envvar='RESIF_GH_EBUSER', help='Specify a GitHub user that has the EasyBuild repositories you want to use instead of the one provided by ULHPC.')
@click.option('--git-ebframework', 'git_ebframework', envvar='RESIF_GIT_EBFRAMEWORK', help='URL or absolute path to EasyBuild framework Git repository.')
@click.option('--git-ebblocks', 'git_ebblocks', envvar='RESIF_GIT_EBBLOCKS', help='URL or absolute path for EasyBuild easyblocks Git repository.')
@click.option('--git-ebconfigs', 'git_ebconfigs', envvar='RESIF_GIT_EBCONFIGS', help='URL or absolute path for EasyBuild easyconfigs Git repository.')
@click.option('--branch-ebframework', 'branch_ebframework', envvar='RESIF_BRANCH_EBFRAMEWORK', help='Git branch for EasyBuild framework.')
@click.option('--branch-ebblocks', 'branch_ebblocks', envvar='RESIF_BRANCH_EBBLOCKS', help='Git branch for EasyBuild easyblocks.')
@click.option('--branch-ebconfigs', 'branch_ebconfigs', envvar='RESIF_BRANCH_EBCONFIGS', help='Git branch for EasyBuild easyconfigs.')
# Bootstrap application variables
@click.option('--apps-root', 'apps_root', envvar='RESIF_APPS_ROOT', help='Path to the root directory for apps (contains all the architecture correspondig to RESIF).')
@click.option('--production', 'branch', flag_value='production', envvar='RESIF_BRANCH', help='Set this variable if you want to work with the production branch of the RESIF repository. (By default, work with the production branch). Do not use with --devel or --branch !')
@click.option('--devel', 'branch', flag_value='devel', envvar='RESIF_BRANCH', help='Set this variable if you want to work with the devel branch of the RESIF repository. (By default, work with the production branch). Do not use with --production or --branch !')
@click.option('--branch', 'branch', envvar='RESIF_BRANCH', help='Set this variable if you want to work with the devel branch of the RESIF repository. (By default, work with the production branch). Do not use with --production or --branch !')
@click.option('--release', envvar='RESIF_RELEASE', help='Release tag or commit of the RESIF repository to deploy.')
@click.option('--releasedir', envvar='RESIF_RELEASEDIR', help='Directory in which to install the release (Relative path from the <apps-root>). Default: <branch>/v<release>-<date>')
@click.option('--rootinstall', envvar='RESIF_ROOTINSTALL', help='Path to the root of the EasyBuild installation (contains the various software sets deployed and the EasyBuild files). Default: <apps-root>/<releasedir>')
@click.option('--append-modulepath', 'append_modulepath', envvar='RESIF_APPEND_MODULEPATH', help='Paths to append to the modulepath in the LOADME files.')
@click.option('--prepend-modulepath', 'prepend_modulepath', envvar='RESIF_PREPEND_MODULEPATH', help='Paths to prepend to the modulepath in the LOADME files.')
# Module Naming Scheme choice
@click.option('--mns', envvar='EASYBUILD_MODULE_NAMING_SCHEME', type=click.Choice(['EasyBuildMNS', 'E', 'HierarchicalMNS', 'H', 'ThematicMNS', 'T']), help='Module Naming Scheme to be used.')
@click.option('--overwrite', 'overwrite', flag_value=True, envvar='RESIF_OVERWRITE', help='Set this flag if you want to overwrite any existing previous installation at --apps-root.')
def bootstrap(**kwargs):
    # Generate the configuration for the bootstrap.
    config = configManager.generateBootstrapConfig(kwargs)
    # Bootstrap EasyBuild.
    if not os.path.isdir(config["rootinstall"]) or config["overwrite"]:
        if config["overwrite"]:
            shutil.rmtree(config["rootinstall"], True)
        click.echo("Bootstrapping EasyBuild.")
        bootstrapEB.bootstrap(config)
        click.echo("Bootstrapping ended successfully.")
        sourcemePath = os.path.join(config['rootinstall'], 'LOADME-'+os.path.basename(config['rootinstall'])+'.sh')
        click.echo("\nTo start using this installation, source the following file:\n" + sourcemePath)
    else:
        sys.stdout.write("An installation is already present at your rootinstall: " + config["rootinstall"] + "\nPlease use the --overwrite flag if you want to overwrite this installation.\n" + "\033[93m" + "WARNING: This will remove everything at " + config["rootinstall"] + "\033[0m\n")
        exit(50)


# Build a (or multiple) software set(s) (Adding new software to an existing EasyBuild install.)
@resif.command(short_help='Deploy software sets on an existing installatation.')
# Path to the source directory
@click.option('--srcpath', envvar='RESIF_SRCPATH', help='Source path to the RESIF directory.')
# Configuration files provisioning
@click.option('--configfile', envvar='RESIF_CONFIGFILE', help='Specify path to a config file to load.')
# Software building variables
@click.option('--rootinstall', envvar='RESIF_ROOTINSTALL', help='Path to the root of an EasyBuild installation (contains the various software sets deployed and the EasyBuild files). Softwares will be installed in <rootinstall>/<swset>/modules')
@click.option('--production', 'branch', flag_value='production', envvar='RESIF_BRANCH', help='Set this variable if you want to work with the production branch of the RESIF repository. (By default, work with the production branch). Do not use with --devel or --branch !')
@click.option('--devel', 'branch', flag_value='devel', envvar='RESIF_BRANCH', help='Set this variable if you want to work with the devel branch of the RESIF repository. (By default, work with the production branch). Do not use with --production or --branch !')
@click.option('--branch', 'branch', envvar='RESIF_BRANCH', help='Set this variable if you want to work with the devel branch of the RESIF repository. (By default, work with the production branch). Do not use with --production or --branch !')
@click.option('--release', envvar='RESIF_RELEASE', help='Release tag or commit of the RESIF repository to use.')
@click.option('--force', 'force', flag_value=True, envvar='RESIF_FORCE', help='Set this flag if you want to force build even if release or branch of the existing stack doesn\'t match given ones.')
@click.option('--installdir', 'installdir', envvar='RESIF_INSTALLDIR', help="Use if you don't want to deploy the software inside the <rootinstall>. Softwares will then be deployed in <installdir>/<swset>/modules")
@click.option('--eb-sourcepath', 'eb_sourcepath', envvar='EASYBUILD_SOURCEPATH', help='EasyBuild sourcepath.')
@click.option('--eb-buildpath', 'eb_buildpath', envvar='EASYBUILD_BUILDPATH', help='EasyBuild buildpath.')
@click.option('--eb-repository', 'eb_repository', envvar='EASYBUILD_REPOSITORY', help='EasyBuild repository type for successfully installed easyconfig files.')
@click.option('--eb-repositorypath', 'eb_repositorypath', envvar='EASYBUILD_REPOSITORYPATH', help='EasyBuild path to the repository for successuflly installed easyconfig files.')
@click.option('--eb-options', 'eb_options', envvar='RESIF_EB_OPTIONS', help='Any command line options to pass to EasyBuild for the build.')
@click.option('--buildmode', envvar='RESIF_BUILDMODE', type=click.Choice(['local', 'job']), help='Mode to build the software: either building locally or in a job.')
@click.option('--mns', envvar='EASYBUILD_MODULE_NAMING_SCHEME', type=click.Choice(['EasyBuildMNS', 'E', 'HierarchicalMNS', 'H', 'ThematicMNS', 'T']), help='Module Naming Scheme to be used.')
@click.option('--out-place', 'out_place', flag_value=True, envvar='RESIF_OUT_PLACE', help='Set this option if you want all the files (sources, build, repository) to be put outside the rootinstall (in an associated subdirectory in $HOME/.resif).')
@click.option('--swsets-config', 'swsets_config', envvar='RESIF_SWSETS_CONFIG', help='Path to a file defining the software sets.')
@click.argument('swsets', nargs=-1)
def build(**kwargs):
    """
    \b
    [SWSETS] TEXT...                Software sets to deploy.
    """
    # Generate the configuration for the bootstrap
    config = configManager.generateBuildConfig(kwargs)
    # Build the software sets.
    click.echo("Building the software sets.")
    config['easybuild_module'] = configManager.getEasyBuildModule(config)
    start = time.time()
    buildSwSets.build(config)
    end = time.time()
    duration = end - start
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    durationFormated = "%dh%dm%ds" % (h, m, s)
    click.echo("Software sets successfully built. The build duration was of " + durationFormated)
    # We return a list of modulepaths and modules to load to start using the new software sets
    modulepaths = ""
    swsetsModulesList = ""
    for swset in config['swsets']:
        if swset != 'core':
            swsetsModulesList += "base/swsets/" + swset + " "
        if 'installdir' in config:
            modulepaths += os.path.join(os.path.join(os.path.join(config['installdir'], swset), 'modules'), 'all') + ':'
        else:
            modulepaths += os.path.join(os.path.join(os.path.join(config['rootinstall'], swset), 'modules'), 'all') + ':'
    if swsetsModulesList != "":
        sys.stdout.write("\nTo make the software sets available, add the following paths to your MODULEPATH environment variable:\n" + modulepaths + "\nOr load the following modules:\n" + swsetsModulesList + "\n")
    else:
        sys.stdout.write("\nTo make the software sets available, add the following paths to your MODULEPATH environment variable:\n" + modulepaths + "\n")


# Full install (Correspond to making a new release)
@resif.command(short_help='Deploy a full environment: bootstrap EasyBuild and use it to install the software sets.')
# Path to the source directory
@click.option('--srcpath', envvar='RESIF_SRCPATH', help='Source path to the RESIF directory.')
# Configuration files provisioning
@click.option('--configfile', envvar='RESIF_CONFIGFILE', help='Specify path to a config file to load.')
# git variables
@click.option('--gh-ebuser', 'gh_ebuser', envvar='RESIF_GH_EBUSER', help='Specify a GitHub user that has the EasyBuild repositories you want to use instead of the one provided by ULHPC.')
@click.option('--git-ebframework', 'git_ebframework', envvar='RESIF_GIT_EBFRAMEWORK', help='URL or absolute path to EasyBuild framework Git repository.')
@click.option('--git-ebblocks', 'git_ebblocks', envvar='RESIF_GIT_EBBLOCKS', help='URL or absolute path for EasyBuild easyblocks Git repository.')
@click.option('--git-ebconfigs', 'git_ebconfigs', envvar='RESIF_GIT_EBCONFIGS', help='URL or absolute path for EasyBuild easyconfigs Git repository.')
@click.option('--branch-ebframework', 'branch_ebframework', envvar='RESIF_BRANCH_EBFRAMEWORK', help='Git branch for EasyBuild framework.')
@click.option('--branch-ebblocks', 'branch_ebblocks', envvar='RESIF_BRANCH_EBBLOCKS', help='Git branch for EasyBuild easyblocks.')
@click.option('--branch-ebconfigs', 'branch_ebconfigs', envvar='RESIF_BRANCH_EBCONFIGS', help='Git branch for EasyBuild easyconfigs.')
# Bootstrap application variables
@click.option('--apps-root', 'apps_root', envvar='RESIF_APPS_ROOT', help='Path to the root directory for apps (contains all the architecture correspondig to RESIF).')
@click.option('--production', 'branch', flag_value='production', envvar='RESIF_BRANCH', help='Set this variable if you want to work with the production branch of the RESIF repository. (By default, work with the production branch). Do not use with --devel or --branch !')
@click.option('--devel', 'branch', flag_value='devel', envvar='RESIF_BRANCH', help='Set this variable if you want to work with the devel branch of the RESIF repository. (By default, work with the production branch). Do not use with --production or --branch !')
@click.option('--branch', 'branch', envvar='RESIF_BRANCH', help='Set this variable if you want to work with the devel branch of the RESIF repository. (By default, work with the production branch). Do not use with --production or --branch !')
@click.option('--release', envvar='RESIF_RELEASE', help='Release tag or commit of the RESIF repository to deploy.')
@click.option('--releasedir', envvar='RESIF_RELEASEDIR', help='Directory in which to install the release (Relative path from the <apps-root>). Default: <branch>/v<release>-<date>')
@click.option('--rootinstall', envvar='RESIF_ROOTINSTALL', help='Path to the root of the EasyBuild installation (contains the various software sets deployed and the EasyBuild files). Default: <apps-root>/<releasedir>')
@click.option('--eb-sourcepath', 'eb_sourcepath', envvar='EASYBUILD_SOURCEPATH', help='EasyBuild sourcepath.')
@click.option('--eb-buildpath', 'eb_buildpath', envvar='EASYBUILD_BUILDPATH', help='EasyBuild buildpath.')
@click.option('--eb-repository', 'eb_repository', envvar='EASYBUILD_REPOSITORY', help='EasyBuild repository type for successfully installed easyconfig files.')
@click.option('--eb-repositorypath', 'eb_repositorypath', envvar='EASYBUILD_REPOSITORYPATH', help='EasyBuild path to the repository for successuflly installed easyconfig files.')
@click.option('--eb-options', 'eb_options', envvar='RESIF_EB_OPTIONS', help='Any command line options to pass to EasyBuild for the build.')
@click.option('--append-modulepath', 'append_modulepath', envvar='RESIF_APPEND_MODULEPATH', help='Paths to append to the modulepath in the LOADME files. Also won\'t reinstall software found at these paths.')
@click.option('--prepend-modulepath', 'prepend_modulepath', envvar='RESIF_PREPEND_MODULEPATH', help='Paths to prepend to the modulepath in the LOADME files. Also won\'t reinstall software found at these paths.')
# Module Naming Scheme choice
@click.option('--mns', envvar='EASYBUILD_MODULE_NAMING_SCHEME', type=click.Choice(['EasyBuildMNS', 'E', 'HierarchicalMNS', 'H', 'ThematicMNS', 'T']), help='Module Naming Scheme to be used.')
# Software building variables
@click.option('--buildmode', envvar='RESIF_BUILDMODE', type=click.Choice(['local', 'job']), help='Mode to build the software: either building locally or in a job.')
@click.option('--swsets-config', 'swsets_config', envvar='RESIF_SWSETS_CONFIG', help='Path to a file defining the software sets.')
@click.option('--overwrite', 'overwrite', flag_value=True, envvar='RESIF_OVERWRITE', help='Set this flag if you want to overwrite any existing previous installation at --apps-root.')
@click.argument('swsets', nargs=-1)
def cleaninstall(**kwargs):
    """
    [SWSETS] TEXT...                Software set to deploy.
    """
    # Generate the configuration for the full installation
    config = configManager.generateCleaninstallConfig(kwargs)
    click.echo("Starting full installation.")
    # Bootstrap EasyBuild.
    if not os.path.isdir(config["rootinstall"]) or config["overwrite"]:
        if config["overwrite"]:
            shutil.rmtree(config["rootinstall"], True)
        click.echo("Bootstrapping EasyBuild.")
        modulePath = bootstrapEB.bootstrap(config)
    else:
        sys.stdout.write("An installation is already present at your rootinstall: " + config["rootinstall"] + "\nPlease use the --overwrite flag if you want to overwrite this installation.\n" + "\033[93m" + "WARNING: This will remove everything at " + config["rootinstall"] + "\033[0m\n")
        exit(50)
    click.echo("Bootstrapping ended successfully.")
    # Build the software sets.
    click.echo("Building the software sets.")
    # Setting the correct MODULEPATH and EasyBuild variables.
    # (Necessary for the behavior to not be modified by external environment variables)
    if config["module_cmd"] == "lmod":
        os.environ["EASYBUILD_MODULES_TOOL"] = "Lmod"
        subprocess.Popen(["bash", "-c", "module unuse $MODULEPATH"])
    os.environ['MODULEPATH'] = modulePath
    configManager.setEasyBuildVariables(config)
    config['easybuild_module'] = configManager.getEasyBuildModule(config)
    start = time.time()
    buildSwSets.build(config)
    end = time.time()
    duration = end - start
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    durationFormated = "%dh%dm%ds" % (h, m, s)
    click.echo("Software sets successfully built. The build duration was of " + durationFormated)
    click.echo("Full installation ended successfully.")
    sourcemePath = os.path.join(config['rootinstall'], 'LOADME-'+os.path.basename(config['rootinstall'])+'.sh')
    click.echo("\nTo start using this installation, source the following file:\n" + sourcemePath)


#######################################################################################################################