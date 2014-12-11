#######################################################################################################################
# Author: Maxime Schmitt
# Mail: maxime.schmitt@telecom-bretagne.eu
# Overview: Module that combines all the other modules and provides a CLI.
#######################################################################################################################

import sys
import click
import os

sys.path.append('.')
import configManager
import bootstrapEB
import buildSwSets

#######################################################################################################################
# The resif group. Defines the name of the command. It is the "main" group.
@click.group()
def resif():
    """
    RESIF commandline interface.

    Choose the sub-command you want to execute.
    """
    pass

#######################################################################################################################
# The subcommands bootstrap, build and cleaninstall.

# Make a new install of EasyBuild.
@resif.command()
# Path to the source directory
@click.option('--srcpath', envvar='RESIF_SRCPATH', help='Source path to the RESIF directory.')
# Configuration files provisioning
@click.option('--configfile', envvar='RESIF_CONFIGFILE', help='Specify path to a config file to load.')
# git variables
@click.option('--gh-ebuser', 'gh_ebuser', envvar='RESIF_GH_EBUSER', help='Specify a GitHub user that has the EasyBuild repositories you want to use instead of the one provided by ULHPC.')
@click.option('--git-ebframework', 'git_ebframework', envvar='RESIF_GIT_EBFRAMEWORK', help='URL or path to EasyBuild framework Git repository.')
@click.option('--git-ebblocks', 'git_ebblocks', envvar='RESIF_GIT_EBBLOCKS', help='URL or path for EasyBuild easyblocks Git repository.')
@click.option('--git-ebconfigs', 'git_ebconfigs', envvar='RESIF_GIT_EBCONFIGS', help='URL or path for EasyBuild easyconfigs Git repository.')
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
# Module Naming Scheme choice
@click.option('--mns', envvar='EASYBUILD_MODULE_NAMING_SCHEME', type=click.Choice(['EasyBuildMNS', 'E', 'HierarchicalMNS', 'H', 'ThematicMNS', 'T']), help='Module Naming Scheme to be used.')
def bootstrap(**kwargs):
    # Generate the configuration for the bootstrap.
    config = configManager.generateBootstrapConfig(kwargs)
    # Bootstrap EasyBuild.
    click.echo("Bootstrapping EasyBuild.")
    bootstrapEB.bootstrap(config)
    click.echo("Bootstrapping ended successfully.")


# Build a (or multiple) software set(s) (Adding new software to an existing EasyBuild install.)
@resif.command()
# Path to the source directory
@click.option('--srcpath', envvar='RESIF_SRCPATH', help='Source path to the RESIF directory.')
# Configuration files provisioning
@click.option('--configfile', envvar='RESIF_CONFIGFILE', help='Specify path to a config file to load.')
# Software building variables
@click.option('--rootinstall', envvar='RESIF_ROOTINSTALL', help='Path to the root of an EasyBuild installation (contains the various software sets deployed and the EasyBuild files). Softwares will be installed in <rootinstall>/<swset>/modules')
@click.option('--installdir', 'installdir', envvar='RESIF_INSTALLDIR', help="Use if you don't want to deploy the software inside the <rootinstall>. Softwares will then be deployed in <installdir>/<swset>/modules")
#@click.option('--eb-installpath', 'eb_installpath', envvar='EASYBUILD_INSTALLPATH', help='EasyBuild installpath.')
@click.option('--eb-sourcepath', 'eb_sourcepath', envvar='EASYBUILD_SOURCEPATH', help='EasyBuild sourcepath.')
@click.option('--eb-buildpath', 'eb_buildpath', envvar='EASYBUILD_BUILDPATH', help='EasyBuild buildpath.')
@click.option('--eb-repository', 'eb_repository', envvar='EASYBUILD_REPOSITORY', help='EasyBuild repository type for successfully installed easyconfig files.')
@click.option('--eb-repositorypath', 'eb_repositorypath', envvar='EASYBUILD_REPOSITORYPATH', help='EasyBuild path to the repository for successuflly installed easyconfig files.')
@click.option('--buildmode', envvar='RESIF_BUILDMODE', type=click.Choice(['local', 'job']), help='Mode to build the software: either building locally or in a job.')
@click.option('--mns', envvar='EASYBUILD_MODULE_NAMING_SCHEME', type=click.Choice(['EasyBuildMNS', 'E', 'HierarchicalMNS', 'H', 'ThematicMNS', 'T']), help='Module Naming Scheme to be used.')
@click.option('--out-place', 'out_place', flag_value=True, envvar='RESIF_ON_PLACE', help='Set this option if you want all the files (sources, build, repository) to be put outside the rootinstall (in an associated subdirectory in $HOME/.resif).')
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
    buildSwSets.build(config)
    click.echo("Software sets successfully built.")


# Full install (Correspond to making a new release)
@resif.command()
# Path to the source directory
@click.option('--srcpath', envvar='RESIF_SRCPATH', help='Source path to the RESIF directory.')
# Configuration files provisioning
@click.option('--configfile', envvar='RESIF_CONFIGFILE', help='Specify path to a config file to load.')
# git variables
@click.option('--gh-ebuser', 'gh_ebuser', envvar='RESIF_GH_EBUSER', help='Specify a GitHub user that has the EasyBuild repositories you want to use instead of the one provided by ULHPC.')
@click.option('--git-ebframework', 'git_ebframework', envvar='RESIF_GIT_EBFRAMEWORK', help='URL or path to EasyBuild framework Git repository.')
@click.option('--git-ebblocks', 'git_ebblocks', envvar='RESIF_GIT_EBBLOCKS', help='URL or path for EasyBuild easyblocks Git repository.')
@click.option('--git-ebconfigs', 'git_ebconfigs', envvar='RESIF_GIT_EBCONFIGS', help='URL or path for EasyBuild easyconfigs Git repository.')
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
# Module Naming Scheme choice
@click.option('--mns', envvar='EASYBUILD_MODULE_NAMING_SCHEME', type=click.Choice(['EasyBuildMNS', 'E', 'HierarchicalMNS', 'H', 'ThematicMNS', 'T']), help='Module Naming Scheme to be used.')
# Software building variables
@click.option('--buildmode', envvar='RESIF_BUILDMODE', type=click.Choice(['local', 'job']), help='Mode to build the software: either building locally or in a job.')
@click.option('--swsets-config', 'swsets_config', envvar='RESIF_SWSETS_CONFIG', help='Path to a file defining the software sets.')
@click.argument('swsets', nargs=-1)
def cleaninstall(**kwargs):
    """
    [SWSETS] TEXT...                Software set to deploy.
    """
    # Generate the configuration for the full installation
    config = configManager.generateCleaninstallConfig(kwargs)
    click.echo("Starting full installation.")
    # Bootstrap EasyBuild.
    click.echo("Bootstrapping EasyBuild.")
    modulePath = bootstrapEB.bootstrap(config)
    click.echo("Bootstrapping ended successfully.")
    # Build the software sets.
    click.echo("Building the software sets.")
    # Setting the correct MODULEPATH and EasyBuild variables.
    # (Necessary for the behavior to not be modified by external environment variables)
    os.environ['MODULEPATH'] = modulePath
    configManager.setEasyBuildVariables(config)
    config['easybuild_module'] = configManager.getEasyBuildModule(config)
    buildSwSets.build(config)
    click.echo("Software sets successfully built.")
    click.echo("Full installation ended successfully.")


#######################################################################################################################