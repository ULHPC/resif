-*- mode: markdown; mode: visual-line; fill-column: 80 -*-
`command-line-interface.md`

Copyright (c) 2014 [Sebastien Varrette](mailto:<Sebastien.Varrette@uni.lu>) [www]()

        Time-stamp: <Mar 2014-12-02 11:22 mschmitt>

-------------------

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

### Full bootstrap

If all you want is to replicate the architecture on the clusters but on your computer (requires root permissions), just execute the following command:  
`bash <(curl https://raw.githubusercontent.com/ULHPC/modules/develop/binscripts/bootstrap.sh)`  
It will clone the modules repository in the default place (`$HOME/.resif/src`), install the script and execute the `resif cleaninstall` command, installing EasyBuild and the core set of softwares at the default place (`/user/local/apps`).

### Check the installation

Let's just check that the installation has been done properly, try this command:  
`resif`  
The output should be an help message looking like that:  
```
Usage: resif [OPTIONS] COMMAND [ARGS]...

  RESIF commandline interface.

  Choose the sub-command you want to execute.

Options:
  --help  Show this message and exit.

Commands:
  bootstrap
  build         [SWSETS] TEXT...
  cleaninstall  [SWSETS] TEXT...
```

If you have that, then you're all set, continue to learn how to actually use this tool.  

## Usage of the CLI

This documentation is divided in three parts, corresponding to the three main commands of the resif script:  
- [bootstrap](#bootstrap)
- [build](#build)
- [cleaninstall](#cleaninstall)

### Bootstrap

Usage: `resif bootstrap [OPTIONS]`

Options:
```
  --srcpath path                  Source path to the RESIF directory.
  --configfile path               Specify path to a config file to load.
  --gh-ebuser TEXT                Specify a GitHub user that has the EasyBuild
                                  repositories you want to use instead of the
                                  one provided by ULHPC.
  --git-ebframework URL           URL or path to EasyBuild framework Git
                                  repository.
  --git-ebblocks URL              URL or path for EasyBuild easyblocks Git
                                  repository.
  --git-ebconfigs URL             URL or path for EasyBuild easyconfigs Git
                                  repository.
  --branch-ebframework TEXT       Git branch for EasyBuild framework.
  --branch-ebblocks TEXT          Git branch for EasyBuild easyblocks.
  --branch-ebconfigs TEXT         Git branch for EasyBuild easyconfigs.
  --apps-root path                Path to the root directory for apps
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
  --releasedir relative path      Directory in which to install the release
                                  (Relative path from the <apps-root>).
                                  Default: <branch>/v<release>-<date>
  --rootinstall path              Path to the root of the EasyBuild
                                  installation (contains the various software
                                  sets deployed and the EasyBuild files).
                                  Default: <apps-root>/<releasedir>
  --mns [EasyBuildMNS|E|HierarchicalMNS|H|ThematicMNS|T]
                                  Module Naming Scheme to be used.
  --help                          Show this message and exit.
```

Default behavior:  
`resif  bootstrap` will install EasyBuild in the default <rootinstall>: `/usr/local/<branch>/v<version>-<date>` where <branch> is the current branch of the repository at your sourcepath (which by default is `$HOME/.resif/src`), <version> the version of this same repository and <date> the date of the build day (the format is YYYYMMDD). In particular, the EasyBuild module is going to be put in `<rootinstall>/core/modules/base/base/EasyBuild` under the name `install-<version>`.  
To use this EasyBuild, just load one of the files starting with LOADME in <rootinstall> (the choice depends on whether you want to install any new software inside this architecture or outside it: the LOADME suffixed with '-out-place' will put everything outside the rootinstall (see the [variables documentation page](https://gitlab.uni.lu/modules/infrastructure/wikis/variables) for further details.)) and your environment variables will be set up to make you able to load the module.

### Build

Usage: `resif build [OPTIONS] [SWSETS]...`

    [SWSETS] TEXT...  
        Software sets to deploy.

Options:
```
  --srcpath path                  Source path to the RESIF directory.
  --configfile path               Specify path to a config file to load.
  --rootinstall path              Path to the root of an EasyBuild
                                  installation (contains the various software
                                  sets deployed and the EasyBuild files).
                                  Softwares will be installed in
                                  <rootinstall>/<swset>/modules
  --installdir path               Use if you don't want to deploy the software
                                  inside the <rootinstall>. Softwares will
                                  then be deployed in
                                  <installdir>/<swset>/modules
  --eb-sourcepath path            EasyBuild sourcepath.
  --eb-buildpath path             EasyBuild buildpath.
  --eb-repository TEXT            EasyBuild repository type for successfully
                                  installed easyconfig files.
  --eb-repositorypath path        EasyBuild path to the repository for
                                  successuflly installed easyconfig files.
  --buildmode [local|job]         Mode to build the software: either building
                                  locally or in a job.
  --mns [EasyBuildMNS|E|HierarchicalMNS|H|ThematicMNS|T]
                                  Module Naming Scheme to be used.
  --out-place                     Set this option if you want all the files
                                  (sources, build, repository) to be put
                                  outside the rootinstall (in an associated
                                  subdirectory in $HOME/.resif).
  --swsets-config path            Path to a file defining the software sets.
  --help                          Show this message and exit.

```

Default behavior:  
To work properly, you have to load one of the LOADME files before using this command as the minimal requirements to use it are to have the EasyBuild module (the one which name ends with install-<version>) in the MODULEPATH and to know the <rootinstall> of the given EasyBuild (which is also defined in the LOADME file).  
`resif build` will deploy the `core` software set describe in the `$HOME/.resif/src/config/swsets.yaml` file using the EasyBuild module mentioned above installed in the <rootinstall> and will put them in the `<rootinstall>/<swset>/modules` directory.

Note that in each case, if you don't have the rights to write in the directory in which the scripts try to deploy the softwares, it won't work. Moreover, to use the newly installed softwares, you will have to add their path to the MODULEPATH (the easiest way is to add `<rootinstall>/<swset>/modules/all` to the MODULEPATH).

### Cleaninstall

Usage: `resif cleaninstall [OPTIONS] [SWSETS]...`

    [SWSETS] TEXT...                Software set to deploy.

Options:
```
  --srcpath path                  Source path to the RESIF directory.
  --configfile path               Specify path to a config file to load.
  --gh-ebuser TEXT                Specify a GitHub user that has the EasyBuild
                                  repositories you want to use instead of the
                                  one provided by ULHPC.
  --git-ebframework URL           URL or path to EasyBuild framework Git
                                  repository.
  --git-ebblocks URL              URL or path for EasyBuild easyblocks Git
                                  repository.
  --git-ebconfigs URL             URL or path for EasyBuild easyconfigs Git
                                  repository.
  --branch-ebframework TEXT       Git branch for EasyBuild framework.
  --branch-ebblocks TEXT          Git branch for EasyBuild easyblocks.
  --branch-ebconfigs TEXT         Git branch for EasyBuild easyconfigs.
  --apps-root path                Path to the root directory for apps
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
  --releasedir relative path      Directory in which to install the release
                                  (Relative path from the <apps-root>).
                                  Default: <branch>/v<release>-<date>
  --rootinstall path              Path to the root of the EasyBuild
                                  installation (contains the various software
                                  sets deployed and the EasyBuild files).
                                  Default: <apps-root>/<releasedir>
  --mns [EasyBuildMNS|E|HierarchicalMNS|H|ThematicMNS|T]
                                  Module Naming Scheme to be used.
  --buildmode [local|job]         Mode to build the software: either building
                                  locally or in a job.
  --swsets-config path            Path to a file defining the software sets.
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
