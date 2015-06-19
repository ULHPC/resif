-*- mode: markdown; mode: visual-line; fill-column: 80 -*-
`command-line-interface.md`

Copyright (c) 2014 [Sebastien Varrette](mailto:<Sebastien.Varrette@uni.lu>) [www]()

        Time-stamp: <Mar 2015-02-27 14:30 mschmitt>

-------------------

# RESIF command line interface

## Overview

This page explains in a first part how to [install the resif script](#installation-of-the-command-line-interface-cli), in a second part [how to use this script](#usage-of-the-cli) and in a third part exposes [some alternative methods to change the configuration](#alternative-configuration-methods).

## Installation of the Command Line Interface (CLI)

**Prerequisites:**

To install this script, you need to have some required packages installed on your computer:

- python 2.6 or above
- git
- pip to install and uninstall the script (On Ubuntu, simply install the `python-pip` package.)

That is enough to install and launch the script itself, but you still need to have the prerequisites for EasyBuild itself, in particular you will need a module tool (either environment-modules or Lmod).  
See the other pages of this documentation for [more details about these tools](https://gitlab.uni.lu/modules/infrastructure/wikis/overview) and the [installation instructions for Lmod](appendix/Lmod-install.md).

### Install from PyPi (recommended)

#### With root permissions

Simply use the following command:  

    pip install resif

You can now start using the command, see below for more information.

#### Without root permissions

Use the following command to install the command:    

    pip install --install-option="--prefix=$HOME/.local" resif
  
Note that you can replace `$HOME/.local` by anything you want as long as you have all the right for this location, just modify the following commands accordingly.

Add then `$HOME/.local/bin` to you path to make the command accessible:

    export PATH=$PATH:$HOME/.local/bin
and `$HOME/.local/lib/python2.7/site-packages` to your pythonpath so that the command's dependencies are accessible:

    export PYTHONPATH=$PYTHONPATH:$HOME/.local/lib/python2.7/site-packages
Note that in this last path, the part `python2.7` may change depending on the python version you use on your computer. Just modify the previous path accordingly to what is actually present in your tree at this point.

### Installation from git

#### With root permissions

Clone the git repository:

    git clone https://github.com/sylmarien/RESIF-PyPi.git

Then go to in this directory and type the following command to install the script:

    python setup.py sdist && pip install dist/*

#### Without root permissions

Clone the git repository:

    git clone https://github.com/sylmarien/RESIF-PyPi.git

Then go to in this directory directory and type the following command to install the script:

    python setup.py sdist && pip install --install-option="--prefix=$HOME/.local" dist/*
Note that you can replace `$HOME/local` by anything you want as long as you have all the right for this location, just modify the following commands accordingly.

Add then `$HOME/.local/bin` to you path:

    export PATH=$PATH:$HOME/.local/bin
and `$HOME/.local/lib/python2.7/site-packages` to your pythonpath:

    export PYTHONPATH=$PYTHONPATH:$HOME/.local/lib/python2.7/site-packages
Note that in this last path, the part `python2.7` may change depending on the python version you use on your computer. Just modify the previous path accordingly to what is actually present in your tree at this point.

### Bash completion

Then, for more comfort, activate the bash auto-completion for the module:

    eval "$(_RESIF_COMPLETE=source resif)"

Since this has to be done each time you launch a new terminal, you may want to create an activation script:

    _RESIF_COMPLETE=source resif > resif-complete.sh
Then you'll just source this file to activate the bash completion (still each time you launch a new terminal):

    source resif-complete.sh
If you want to always have the bash completion, put this file in your `/etc/bash_completion.d` directory (requires root access).

### Check the installation

Let's just check that the installation has been done properly, try this command:

    resif
The output should be an help message looking like that:  
```
Usage: resif [OPTIONS] COMMAND [ARGS]...

  RESIF commandline interface.

  Choose the sub-command you want to execute.

Options:
  --version  Return the version of this script.
  --help     Show this message and exit.

Commands:
  bootstrap          Deploy a fresh EasyBuild install.
  build              Deploy software sets on an existing installatation.
  buildtimesoftware  Print the build time of of a given installed software
                     from a specific software set.
  buildtimeswset     Print the build times of all the installed software of a
                     given software set.
  cleaninstall       Deploy a full environment: bootstrap EasyBuild and use it
                     to install the software sets.
  count              Count the number of easyconfig files that contain the
                     given pattern in their name.
  init               Initialize the git repository in the srcpath.
  search             Show all the easyconfigs which name contains the given
                     pattern.
  update             Update the git repository in the srcpath.
  wipe               Wipe all data in the srcpath.
```

If you have that, then you're all set, continue to learn how to actually use this tool.  

## Usage of the CLI

This documentation is divided in three parts, corresponding to the three main commands of the resif script:  
- [init](#init)
- [update](#update)
- [wipe](#wipe)
- [count](#count)
- [search](#search)
- [buildtimeswset](#buildtimeswset)
- [buildtimesoftware](#buildtimesoftware)
- [bootstrap](#bootstrap)
- [build](#build)
- [cleaninstall](#cleaninstall)

### Init

Usage:

    resif init [OPTIONS]

```
Options:
  --git-architecture URL          Defines an alternative git repository URL or path
                                  to get the architecture from.
  --srcpath path                  Defines an alternative path to put the sources in.
  --overwrite                     Set this flag if you want to overwrite any existing
                                  previous installation at --apps-root.
  --help                          Show this message and exit.
```

Default behavior:  
The `resif init` command will clone the default git infrastructure repository (e.g https://github.com/ULHPC/modules) in the default srcpath (e.g $HOME/.resif/src).  

If you want to use your own configuration, just fork our infrastructure repository and make the changes you want (or create it from scratch but then pay attention to respect the layout we use) and use the `--git-architecture` option to the URL (or the path) to your git repository.

Note that this command must have been executed before using any of the other commands since the other commands rely on the files initialize by this command.

### Update

Usage:

    resif update [OPTIONS]

```
Options:
  --srcpath path                  Defines an alternative path to the repository.
  --help                          Show this message and exit.
```

Default behavior:  
The `resif update` command will update the repository at the default srcpath (e.g $HOME/.resif/src).

### Wipe

Usage:

    resif wipe [OPTIONS]

```
Options:
  --srcpath path                  Defines an alternative path to the repository.
  --yes                           Use to not prompt confirmation message. (Check what you are
                                  trying to do before !)
  --help                          Show this message and exit.
```

Default behavior:  
The `resif wipe` command will remove all data from the default srcpath (e.g $HOME/.resif/src) after having prompt you to confirm it.

### Count

Usage:

    resif count [OPTIONS] CONTENT
      [CONTENT] TEXT              Text to look for in the names of the easyconfig files.

```
Options:
  --rootinstall path              Path to the root of the EasyBuild
                                  installation (contains the various software
                                  sets deployed and the EasyBuild files).
  --mns [EasyBuildMNS|E|HierarchicalMNS|H|ThematicMNS|T]
                                  Module Naming Scheme to be used.
  --help                          Show this message and exit.
```

Default behavior:  
The `resif count sample` command will return the number of easyconfig files that contain "sample" in their name.

### Search

Usage:

    resif search [OPTIONS] CONTENT
      [CONTENT] TEXT              Text to look for in the names of the installed softwares.

```
Options:
  --rootinstall path              Path to the root of the EasyBuild
                                  installation (contains the various software
                                  sets deployed and the EasyBuild files).
  --mns [EasyBuildMNS|E|HierarchicalMNS|H|ThematicMNS|T]
                                  Module Naming Scheme to be used.
  --show-path                     Make the command to show the full path to
                                  the files listed.
  --help                          Show this message and exit.
```

Default behavior:  
The `resif search sample` command will return the names of the easyconfig files that contain "sample" in their name.

### buildtimeswset

Usage

    resif buildtimeswset [OPTIONS] SWSET
      [SWSET] TEXT                Software set to consider.

```
Options:
  --rootinstall path              Path to the root of the EasyBuild installation (contains
                                  the various software sets deployed and the EasyBuild
                                  files).
  --seconds                       Set this flag if you want the software build time output
                                  to be in seconds (not formated).
  --help                          Show this message and exit.
```

Default behavior:  
The `resif buildtimeswset core` command will return the build durations of all the installed softwares of the "core" software set.

### buildtimesoftware

Usage:

    resif buildtimesoftware [OPTIONS] SWSET SOFTWARE
      [SWSET] TEXT                Software set to consider.
      [SOFTWARE] TEXT             Software name to consider.

```
Options:
  --rootinstall TEXT              Path to the root of the EasyBuild installation (contains
                                  the various software sets deployed and the EasyBuild
                                  files).
  --seconds                       Set this flag if you want the software build time output
                                  to be in seconds (not formated).
  --help                          Show this message and exit.
```

Default behavior:  
The `resif buildtimesoftware core sample` command will return the build durations of all the versions of the "sample" software that are installed as a part of the "core" software set.

### Bootstrap

Usage:

    resif bootstrap [OPTIONS]

```
Options:
  --srcpath TEXT                  Source path to the RESIF directory.
  --configfile TEXT               Specify path to a config file to load.
  --gh-ebuser TEXT                Specify a GitHub user that has the EasyBuild
                                  repositories you want to use instead of the
                                  one provided by ULHPC.
  --git-ebframework TEXT          URL or absolute path to EasyBuild framework
                                  Git repository.
  --git-ebblocks TEXT             URL or absolute path for EasyBuild
                                  easyblocks Git repository.
  --git-ebconfigs TEXT            URL or absolute path for EasyBuild
                                  easyconfigs Git repository.
  --branch-ebframework TEXT       Git branch for EasyBuild framework.
  --branch-ebblocks TEXT          Git branch for EasyBuild easyblocks.
  --branch-ebconfigs TEXT         Git branch for EasyBuild easyconfigs.
  --apps-root TEXT                Path to the root directory for apps
                                  (contains all the architecture correspondig
                                  to RESIF).
  --production                    Set this variable if you want to work with
                                  the production branch of the RESIF
                                  repository. (By default, work with the
                                  production branch). Do not use with --devel
                                  or --branch !
  --devel                         Set this variable if you want to work with
                                  the devel branch of the RESIF repository.
                                  (By default, work with the production
                                  branch). Do not use with --production or
                                  --branch !
  --branch TEXT                   Set this variable if you want to work with
                                  the devel branch of the RESIF repository.
                                  (By default, work with the production
                                  branch). Do not use with --production or
                                  --branch !
  --release TEXT                  Release tag or commit of the RESIF
                                  repository to deploy.
  --releasedir TEXT               Directory in which to install the release
                                  (Relative path from the <apps-root>).
                                  Default: <branch>/v<release>-<date>
  --rootinstall TEXT              Path to the root of the EasyBuild
                                  installation (contains the various software
                                  sets deployed and the EasyBuild files).
                                  Default: <apps-root>/<releasedir>
  --append-modulepath TEXT        Paths to append to the modulepath in the
                                  LOADME files.
  --prepend-modulepath TEXT       Paths to prepend to the modulepath in the
                                  LOADME files.
  --mns [EasyBuildMNS|E|HierarchicalMNS|H|ThematicMNS|T]
                                  Module Naming Scheme to be used.
  --overwrite                     Set this flag if you want to overwrite any
                                  existing previous installation at --apps-
                                  root.
  --help                          Show this message and exit.
```

Default behavior:  
`resif  bootstrap` will install EasyBuild in the default <rootinstall>: `$HOME/.local/resif/<branch>/v<version>-<date>` where <branch> is the current branch of the repository at your sourcepath (which by default is `$HOME/.resif/src`), <version> the version of this same repository and <date> the date of the build day (the format is YYYYMMDD). In particular, the EasyBuild module is going to be put in `<rootinstall>/core/modules/base/base/EasyBuild` under the name `install-<version>`.  
To use this EasyBuild, just load one of the files starting with LOADME in <rootinstall> (the choice depends on whether you want to install any new software inside this architecture or outside it: the LOADME suffixed with '-out-place' will put everything outside the rootinstall (see the [variables documentation page](https://gitlab.uni.lu/modules/infrastructure/wikis/variables) for further details.)) and your environment variables will be set up to make you able to load the module.

### Build

Usage:

    resif build [OPTIONS] [SWSETS]...
      [SWSETS] TEXT...            Software sets to deploy.

```
Options:
  --srcpath TEXT                  Source path to the RESIF directory.
  --configfile TEXT               Specify path to a config file to load.
  --rootinstall TEXT              Path to the root of an EasyBuild
                                  installation (contains the various software
                                  sets deployed and the EasyBuild files).
                                  Softwares will be installed in
                                  <rootinstall>/<swset>/modules
  --production                    Set this variable if you want to work with
                                  the production branch of the RESIF
                                  repository. (By default, work with the
                                  production branch). Do not use with --devel
                                  or --branch !
  --devel                         Set this variable if you want to work with
                                  the devel branch of the RESIF repository.
                                  (By default, work with the production
                                  branch). Do not use with --production or
                                  --branch !
  --branch TEXT                   Set this variable if you want to work with
                                  the devel branch of the RESIF repository.
                                  (By default, work with the production
                                  branch). Do not use with --production or
                                  --branch !
  --release TEXT                  Release tag or commit of the RESIF
                                  repository to use.
  --force                         Set this flag if you want to force build
                                  even if release or branch of the existing
                                  stack doesn't match given ones.
  --installdir TEXT               Use if you don't want to deploy the software
                                  inside the <rootinstall>. Softwares will
                                  then be deployed in
                                  <installdir>/<swset>/modules
  --eb-sourcepath TEXT            EasyBuild sourcepath.
  --eb-buildpath TEXT             EasyBuild buildpath.
  --eb-repository TEXT            EasyBuild repository type for successfully
                                  installed easyconfig files.
  --eb-repositorypath TEXT        EasyBuild path to the repository for
                                  successuflly installed easyconfig files.
  --eb-options TEXT               Any command line options to pass to
                                  EasyBuild for the build.
  --buildmode [local|job]         Mode to build the software: either building
                                  locally or in a job.
  --mns [EasyBuildMNS|E|HierarchicalMNS|H|ThematicMNS|T]
                                  Module Naming Scheme to be used.
  --out-place                     Set this option if you want all the files
                                  (sources, build, repository) to be put
                                  outside the rootinstall (in an associated
                                  subdirectory in $HOME/.resif).
  --swsets-config TEXT            Path to a file defining the software sets.
  --help                          Show this message and exit.

```

Default behavior:  
To work properly, you have to load one of the LOADME files before using this command as the minimal requirements to use it are to have the EasyBuild module (the one which name ends with install-<version>) in the MODULEPATH and to know the <rootinstall> of the given EasyBuild (which is also defined in the LOADME file).  
`resif build` will deploy the `core` software set describe in the `$HOME/.resif/src/config/swsets.yaml` file using the EasyBuild module mentioned above installed in the <rootinstall> and will put them in the `<rootinstall>/<swset>/modules` directory.

Note that in each case, if you don't have the rights to write in the directory in which the scripts try to deploy the softwares, it won't work. Moreover, to use the newly installed softwares, you will have to add their path to the MODULEPATH (the easiest way is to add `<rootinstall>/<swset>/modules/all` to the MODULEPATH).

### Cleaninstall

Usage:

    resif cleaninstall [OPTIONS] [SWSETS]...
      [SWSETS] TEXT...            Software set to deploy.

```
Options:
  --srcpath TEXT                  Source path to the RESIF directory.
  --configfile TEXT               Specify path to a config file to load.
  --gh-ebuser TEXT                Specify a GitHub user that has the EasyBuild
                                  repositories you want to use instead of the
                                  one provided by ULHPC.
  --git-ebframework TEXT          URL or absolute path to EasyBuild framework
                                  Git repository.
  --git-ebblocks TEXT             URL or absolute path for EasyBuild
                                  easyblocks Git repository.
  --git-ebconfigs TEXT            URL or absolute path for EasyBuild
                                  easyconfigs Git repository.
  --branch-ebframework TEXT       Git branch for EasyBuild framework.
  --branch-ebblocks TEXT          Git branch for EasyBuild easyblocks.
  --branch-ebconfigs TEXT         Git branch for EasyBuild easyconfigs.
  --apps-root TEXT                Path to the root directory for apps
                                  (contains all the architecture correspondig
                                  to RESIF).
  --production                    Set this variable if you want to work with
                                  the production branch of the RESIF
                                  repository. (By default, work with the
                                  production branch). Do not use with --devel
                                  or --branch !
  --devel                         Set this variable if you want to work with
                                  the devel branch of the RESIF repository.
                                  (By default, work with the production
                                  branch). Do not use with --production or
                                  --branch !
  --branch TEXT                   Set this variable if you want to work with
                                  the devel branch of the RESIF repository.
                                  (By default, work with the production
                                  branch). Do not use with --production or
                                  --branch !
  --release TEXT                  Release tag or commit of the RESIF
                                  repository to deploy.
  --releasedir TEXT               Directory in which to install the release
                                  (Relative path from the <apps-root>).
                                  Default: <branch>/v<release>-<date>
  --rootinstall TEXT              Path to the root of the EasyBuild
                                  installation (contains the various software
                                  sets deployed and the EasyBuild files).
                                  Default: <apps-root>/<releasedir>
  --eb-sourcepath TEXT            EasyBuild sourcepath.
  --eb-buildpath TEXT             EasyBuild buildpath.
  --eb-repository TEXT            EasyBuild repository type for successfully
                                  installed easyconfig files.
  --eb-repositorypath TEXT        EasyBuild path to the repository for
                                  successuflly installed easyconfig files.
  --eb-options TEXT               Any command line options to pass to
                                  EasyBuild for the build.
  --append-modulepath TEXT        Paths to append to the modulepath in the
                                  LOADME files. Also won't reinstall software
                                  found at these paths.
  --prepend-modulepath TEXT       Paths to prepend to the modulepath in the
                                  LOADME files. Also won't reinstall software
                                  found at these paths.
  --mns [EasyBuildMNS|E|HierarchicalMNS|H|ThematicMNS|T]
                                  Module Naming Scheme to be used.
  --buildmode [local|job]         Mode to build the software: either building
                                  locally or in a job.
  --swsets-config TEXT            Path to a file defining the software sets.
  --overwrite                     Set this flag if you want to overwrite any
                                  existing previous installation at --apps-
                                  root.
  --help                          Show this message and exit.
```

Default behavior:  
`resif cleaninstall` basically does `resif bootstrap` and then `resif build`.

## Alternative configuration methods

As of now, we have only seen one way to modify the configuration of the script: the command line options. But there are 2 other ways to do it:  
- through the environment variables
- through a configuration file

However before going any further, it is important to understand the order of priority between the differents sources of configuration. The order of preference for the different configuration types follow the following rules:  
- entries in a configuration file override the corresponding default values
- environment variables override corresponding entries in the configuration file and default values
- command line options override corresponding environment variables, entries in the configuration file and default values.

### Environment variables (supported by all commands)

Any option available through the command line can be set using an environment variable.  
The environment variable associated to an option is named by taking the option name in capital letters without the `--` prefix, replacing the dashes (`-`) with underscores (`_`) and prefixing it by `$RESIF_`.

For example, the `--apps-root` option associated environment variable is `$RESIF_APPS_ROOT`.

**The only exceptions are the EasyBuild-related options.** Those are the options that are prexied with `eb-` (such as `--eb-sourcepath`) and the `--mns` options.  
The ones prefixed with `eb-` follow the same rules except that the prefix is `$EASYBUILD_` instead of `$RESIF_` (ie `--eb-sourcepath` is associated to `$EASYBUILD_SOURCEPATH`).  
The `--mns` option associated environment variable is `$EASYBUILD_MODULE_NAMING_SCHEME`.

### Configuration file (supported only by the bootstrap, build and cleaninstall commands)

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
