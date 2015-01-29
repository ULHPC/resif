# RESIF command line interface

## Overview

This page explains in a first part how to [install the resif script](#installation-of-the-command-line-interface-cli), in a second part [how to use this script](#usage-of-the-cli) and in a third part exposes [some alternative methods to change the configuration](#alternative-configuration-methods).

## Installation of the Command Line Interface (CLI)

**Prerequisites:**

To install this script, you need to have some required packages installed on your computer:  
- python 2.6 or above
- git
- a YAML parser for python (PyYaml works fine. On Ubuntu, simply install the `python-yaml` package.)
- pip to install and uninstall the script (On Ubuntu, simply install the `python-pip` package.)

That is enough to install and launch the script itself, but you still need to have the prerequisites for EasyBuild itself, in particular you will need a module tool (either environment-modules or Lmod).  
See the other pages of this documentation for [more details about these tools](https://gitlab.uni.lu/modules/infrastructure/wikis/overview) and the [installation instructions for Lmod](https://gitlab.uni.lu/modules/infrastructure/wikis/Lmod-install).

### Installation with root permissions

After having cloned the repository, go to the `bin` directory and type the following command to install the script:  
`pip install .`

Then, for more comfort, activate the bash auto-completion for the module:  
`source resif-complete.sh`  
(This step has to be done each time you create a new shell)

### Installation without root permissions

After having cloned the repository, go to the `bin` directory and type the following command to install the script:  
`pip install --install-option="--prefix=$HOME/local" .`  
Note that you can replace `$HOME/local` by anything you want as long as you have all the right for this location, just modify the following commands accordingly.

Add then `$HOME/local/bin` to you path:  
`export PATH=$PATH:$HOME/local/bin`  
and `$HOME/local/lib/python2.7/site-packages` to your pythonpath:  
`export PYTHONPATH=$PYTHONPATH:$HOME/local/lib/python2.7/site-packages`  
Note that in this last path, the part `python2.7` may change depending on the python version you use on your computer. Just modify the previous path accordingly to what is actually present in your tree at this point.

Then, for more comfort, activate the bash auto-completion for the module:  
`source resif-complete.sh`  
(This step has to be done each time you create a new shell)

### Check the installation

Let's just check that the installation has been done properly, try this command:  
`resif`  
The output should be an help message looking like that:  
```
Usage: resif [OPTIONS] COMMAND [ARGS]...

  RESIF commandline interface.

  To use this software, first choose between the 'admin' or the 'user'
  command, depending on your role and what you want to do.

Options:
  --help  Show this message and exit.

Commands:
  admin  Commands for the clusters administrators.
  user   Commands for the clusters users.
```

If you have that, then you're all set, continue to learn how to actually use this tool.  

## Usage of the CLI

The resif command is divided in two main usages:  
- the `admin` one which is meant to be used by the cluster sysadmins to deploy the softwares.
- the `user` one which is meant for the users of the cluster that would want to replicate the installation of the clusters or add some missing software for themselves.

The differences between those two modes are minor, as they lie on the default values for the options. (see the [variables page](https://gitlab.uni.lu/modules/infrastructure/wikis/variables) for more details)  
Considering that fact, this documentation page will refer to the `admin` usage and add a note when some precautions have to be taken when using the `user` usage. If no such note is present, just consider that replacing `admin` with `user` in the command line will work properly.

Note that if at some point when using the command line interface you want to get some help, use the `--help` option which is implemented for all the commands and that will show you an help message for the current command (ex: `resif admin bootstrap --help`).

This documentation is divided in three parts, corresponding to the three main commands of the resif script:  
- [bootstrap](#bootstrap)
- [build](#build)
- [cleaninstall](#cleaninstall)

### Bootstrap

Usage: `resif admin bootstrap [OPTIONS]`

Options:
```
  --srcpath TEXT                  Source path to the RESIF directory.
  --configfile TEXT               Specify path to a config file to load.
  --gh-ebuser TEXT                Specify a GitHub user that has the EasyBuild
                                  repositories you want to use instead of the
                                  one provided by ULHPC.
  --git-ebframework TEXT          URL or path to EasyBuild framework Git
                                  repository.
  --git-ebblocks TEXT             URL or path for EasyBuild easyblocks Git
                                  repository.
  --git-ebconfigs TEXT            URL or path for EasyBuild easyconfigs Git
                                  repository.
  --branch-ebframework TEXT       Git branch for EasyBuild framework.
  --branch-ebblocks TEXT          Git branch for EasyBuild easyblocks.
  --branch-ebconfigs TEXT         Git branch for EasyBuild easyconfigs.
  --apps-root TEXT                Path to the root directory for apps
                                  (contains all the architecture correspondig
                                  to RESIF).
  --production                    Set this variable if you want to work with
                                  the production branch of the RESIF
                                  repository. (By default, work with the
                                  current branch). Do not use with --devel or
                                  --branch !
  --devel                         Set this variable if you want to work with
                                  the devel branch of the RESIF repository.
                                  (By default, work with the current branch).
                                  Do not use with --production or --branch !
  --branch TEXT                   Set this variable if you want to work with
                                  the devel branch of the RESIF repository.
                                  (By default, work with the current branch).
                                  Do not use with --production or --branch !
  --release TEXT                  Release tag or commit of the RESIF
                                  repository to deploy.
  --releasedir TEXT               Directory in which to install the release.
  --rootinstall TEXT              Path to the root of the EasyBuild
                                  installation (contains the various software
                                  sets deployed and the EasyBuild files).
  --mns [EasyBuildMNS|HierarchicalMNS|ThematicMNS]
                                  Module Naming Scheme to be used.
  --help                          Show this message and exit.
```


### Build

Usage: `resif admin build [OPTIONS] EASYBUILD_MODULE [SWSETS]...`

    EASYBUILD_MODULE TEXT...  
        EasyBuild module to use to build the software sets. The given EasyBuild module must already be in your MODULEPATH.
    [SWSETS] TEXT...  
        Software sets to deploy.

Options:
```
  --srcpath TEXT                  Source path to the RESIF directory.
  --configfile TEXT               Specify path to a config file to load.
  --rootinstall TEXT              Path to the root of an EasyBuild
                                  installation (contains the various software
                                  sets deployed and the EasyBuild files).
  --eb-sourcepath TEXT            EasyBuild sourcepath.
  --eb-buildpath TEXT             EasyBuild buildpath.
  --eb-repository TEXT            EasyBuild repository type for successfully
                                  installed easyconfig files.
  --eb-repositorypath TEXT        EasyBuild path to the repository for
                                  successuflly installed easyconfig files.
  --buildmode [local|job]         Mode to build the software: either building
                                  locally or in a job.
  --mns [EasyBuildMNS|HierarchicalMNS|ThematicMNS]
                                  Module Naming Scheme to be used.
  --swsets-config TEXT            Path to a file defining the software sets.
  --help                          Show this message and exit.
```

### Cleaninstall

Usage: `resif admin cleaninstall [OPTIONS] [SWSETS]...`

    [SWSETS] TEXT...                Software set to deploy.

Options:
```
  --srcpath TEXT                  Source path to the RESIF directory.
  --configfile TEXT               Specify path to a config file to load.
  --gh-ebuser TEXT                Specify a GitHub user that has the EasyBuild
                                  repositories you want to use instead of the
                                  one provided by ULHPC.
  --git-ebframework TEXT          URL or path to EasyBuild framework Git
                                  repository.
  --git-ebblocks TEXT             URL or path for EasyBuild easyblocks Git
                                  repository.
  --git-ebconfigs TEXT            URL or path for EasyBuild easyconfigs Git
                                  repository.
  --branch-ebframework TEXT       Git branch for EasyBuild framework.
  --branch-ebblocks TEXT          Git branch for EasyBuild easyblocks.
  --branch-ebconfigs TEXT         Git branch for EasyBuild easyconfigs.
  --apps-root TEXT                Path to the root directory for apps
                                  (contains all the architecture correspondig
                                  to RESIF).
  --production                    Set this variable if you want to work with
                                  the production branch of the RESIF
                                  repository. (By default, work with the
                                  current branch). Do not use with --devel or
                                  --branch !
  --devel                         Set this variable if you want to work with
                                  the devel branch of the RESIF repository.
                                  (By default, work with the current branch).
                                  Do not use with --production or --branch !
  --branch TEXT                   Set this variable if you want to work with
                                  the devel branch of the RESIF repository.
                                  (By default, work with the current branch).
                                  Do not use with --production or --branch !
  --release TEXT                  Release tag or commit of the RESIF
                                  repository to deploy.
  --releasedir TEXT               Directory in which to install the release.
  --rootinstall TEXT              Path to the root of the EasyBuild
                                  installation (contains the various software
                                  sets deployed and the EasyBuild files).
  --mns [EasyBuildMNS|HierarchicalMNS|ThematicMNS]
                                  Module Naming Scheme to be used.
  --buildmode [local|job]         Mode to build the software: either building
                                  locally or in a job.
  --swsets-config TEXT            Path to a file defining the software sets.
  --help                          Show this message and exit.
```

## Alternative configuration methods

As of now, we have only seen one way to modify the configuration of the script: the command line options. But there are 2 other ways to do it:  
- through the environment variables
- through a configuration file

However before going any further, it is important to understand the order of priority between the differents sources of configuration. The order of preference for the different configuration types follow the following rules:  
- entries in a configuration file override the corresponding default values
- environment variables override corresponding entries in the configuration file and default values
- command line options override corresponding environment variables, entries in the configuration file and default values.

### Environment variables

Any option available through the command line can be set using an environment variable.  
The environment variable associated to an option is named by taking the option name in capital letters without the `--` prefix, replacing the dashes (`-`) with underscores (`_`) and prefixing it by `$RESIF_`.

For example, the `--apps-root` option associated environment variable is `$RESIF_APPS_ROOT`.

**The only exceptions are the EasyBuild-related options.** Those are the options that are prexied with `eb-` (such as `--eb-sourcepath`) and the `--mns` options.  
The ones prefixed with `eb-` follow the same rules except that the prefix is `$EASYBUILD_` instead of `$RESIF_` (ie `--eb-sourcepath` is associated to `$EASYBUILD_SOURCEPATH`).  
The `--mns` option associated environment variable is `$EASYBUILD_MODULE_NAMING_SCHEME`.

### Configuration file

Any option available through the command line can be set using an entry in a configuration file.  
The entry associated to an option is named by taking the option name without the `--` prefix and replacing the dashes (`-`) with underscores (`_`).

For example, the `--apps-root` option associated entry is `apps_root`.

As for the syntax of the configuration file, it is written in YAML and is the following:   
```yaml
option_name: option_value
```

### Particular cases of `$easybuild_module` and `$swsets`

Those variables are different from the others as they have no option associated (of the form `--something`) and they have no associated environment variables either, so we give here the alternative methods to set them.

#### `$easybuild_module`

The associated configuration file entry is `easybuild_module`.

#### `$swsets`

The associated configuration file entry is `swsets`.  
Moreover, this option can contain more than one value and therefore some precautions have to be taken when setting its value(s).
The syntax for thix variable is the following:  
in case you want to set only one value (example: core):  
```yaml
swsets:
    - core
```
in cas you want to set multiple values (example: core and ulhpc):  
```yaml
swsets:
    - core
    - ulhpc
```