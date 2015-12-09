-*- mode: markdown; mode: visual-line; fill-column: 80 -*-
`workflow.md`

Copyright (c) 2014 [Sebastien Varrette](mailto:<Sebastien.Varrette@uni.lu>) [www]()

        Time-stamp: <Wed 2015-12-09 00:13 svarrette>

-------------------

# RESIF  Variables

The workflow revolves around a few variables that are defined below.  
Although it is interesting to take a look at them to personalize an installation, the script can be used without manually setting any of these options since the necessary ones have a default value. 

Here are all the variables that can be set, followed by their descriptions.

| Variable             | Description                                            | Default (if any)                                       |
|----------------------|--------------------------------------------------------|--------------------------------------------------------|
| `git_control`        | Git URL/path for your resif/modules control repository | <https://github.com/ULHPC/modules>                     |
| `user`               | User operating the process                             | `<whoami>`                                             |
| `group`              | Group                                                  |                                                        |
| `ebaccount`          | Github account hosting EB repos ['hpcugent','ULHPC']   | `hpcugent`                                             |
| `ebframework`        | Git URL/path for EB framework repo                     | `https://github.com/<ebaccount>/easybuild-framework`   |
| `ebblocks`           | Git URL/path for EB easyblocks repo                    | `https://github.com/<ebaccount>/easybuild-easyblocks`  |
| `ebconfigs`          | Git URL/path for EB easyconfigs repo                   | `https://github.com/<ebaccount>/easybuild-easyconfigs` |
| `srcpath`            | Source path for the conf. repository                   | $HOME/.resif/src                                       |
| `configfile`         | Path to custom configuration file                      |                                                        |
| `swsets_config`      | Path to file defining the software sets                | <srcpath>/config/swsets.yaml                           |
| `swsets`             | Software set to deploy  ['core','ulhpc']               | core                                                   |
| `mns`                | Module Naming Scheme     ['EasyBuildMNS',              | ThematicMNS                                            |
|                      | 'HierarchicalMNS', 'ThematicMNS']                      |                                                        |
| `buildmode`          | Local build ('local') vs. job  ('job')                 | local                                                  |
| `apps_root`          | Root directory for apps (modules & sw)                 | $HOME/.local/resif                                     |
| `branch`             | Branch of the RESIF repository to work with            |                                                        |
| `release`            | Release tag or commit to deploy                        | HEAD                                                   |
| `releasedir`         | Subdirectory in which to deploy the release            | <branch>/<release>-<date>                              |
| `rootinstall`        | Root Installation directory                            | <apps_root>/<releasedir>                               |
| `installdir`         | Path to an alternative directory in which to build     |                                                        |
| `eb_sourcepath`      | Directory to store software sources                    | $HOME/.resif/sources                                   |
|                      | and install files                                      |                                                        |
| `eb_buildpath`       | (temporary) directories to host builds                 | $HOME./resif/build                                     |
| `eb_repository`      | Type of repository to store the .eb files              | FileRepository                                         |
|                      | of the successfuly installed softwares                 |                                                        |
| `eb_repositorypath`  | Path to this repository                                | $HOME/.resif/eb_repo                                   |
| `eb_options`         | String of options to pass "as is" to EasyBuild.        | ""                                                     |
| `out_place`          | If set to True, EasyBuild will put the files at its    | True                                                   |
|                      | default location (~/.local/easybuild)                  |                                                        |
| `overwrite`          | Set this flag if you want to overwrite any file        | False                                                  |
|                      | that is already present at the install location        |                                                        |
| `append_modulepath`  | Specify a path to add at the beginning of the          |                                                        |
|                      | modulepath in the LOADME files.                        |                                                        |
| `prepend_modulepath` | Specify a path to add at the end of the modulepath     |                                                        |
|                      | in the LOADME files.                                   |                                                        |

## Specific Configuration variables

### Git control / infrastructure repository `$git_control`


_Default_: <https://github.com/ULHPC/modules>

Set this variable to a Git URL or path to your **Resif / Modules control repository**.
A Resif control repository stores a Resif configuration together with your software sets.

It also defines the semantic versioning applied on your HPC platform to allow your user to rebuild the software available at a given period of time. This comes in the context of the [Reproducible research](http://mescal.imag.fr/membres/arnaud.legrand/blog/2015/12/03/talk_15_12_03_Orleans.pdf) initiative we try to promote on our [ULHPC](http://www.uni.lu) platform.

To learn more about this control repository (and learn how to create your own, fitting your needs), go to the [layout and versioning page](layout-and-versioning.md).

### Local user/group deploying the infrastructure `$ebuser` `$ebgroup`

* all processes / jobs are run as this user
* all [sub]directory are assuming having read/write access for that user and/or group

_Defaults_ values:

| Variables | Default  |
|-----------|----------|
| `$user`   | `whoami` |
| `$group`  |          |

### Github account hosting the Easybuild repositories `$ebaccount`

_Default_: `hpcugent` (Alternative: `ULHPC`).

RESIF will require access to the classical [Easybuild](https://hpcugent.github.io/easybuild) repositories (typically the [forks](https://help.github.com/articles/fork-a-repo/) made under a given Github account `<ebaccount>`), _i.e._:

* [Easybuild framework](https://github.com/hpcugent/easybuild-framework): the core of the `eb` tool, providing functionality commonly needed when installing scientific software on HPC systems.
    - _Default_: `https://github.com/<ebaccount>/easybuild-framework`
    - customize the default url and branch with `$ebframework`
* [Easybuild Easyblocks](https://github.com/hpcugent/easybuild-easyblocks/):  implementation of a particular software build and install procedure.
    - _Default_: `https://github.com/<ebaccount>/easybuild-easyblocks/`
    - customize the default url and branch with `$ebblocks`
* [Easybuild Easyconfigs](https://github.com/hpcugent/easybuild-easyconfigs/): probably the **most important** repository since it holds the specification files that are supplied to EasyBuild to build a given software. 
    - _Default_: `https://github.com/<ebaccount>/easybuild-easyconfigs/`
    - customize the default url with `$git_ebblocks`
	- customize the default branch (`master`) with `$branch_ebconfigs`
* [VCS base](https://github.com/hpcugent/vsc-base): some basic Python libraries used by UGent's HPC group
    - _Default_: `https://github.com/hpcugent/vsc-base`
	- customize the default url with `$git_vscbase`

_Defaults_ values:

| Variable                              | Default value                                                         |
|---------------------------------------|-----------------------------------------------------------------------|
| `ebaccount`                           | `hpcugent`                                                            |
| `eb{framework,blocks,configs}`        | `https://github.com/<ebaccount>/easybuild-{framework,blocks,configs}` |

Note that you can specify the branch from the given repository either by using the following syntax for in the corresponding variables:

    'url|branch'

which in an example would look like that:

    'https://github.com/hpcugent/easybuild-framework|master'

Note that if you use this syntax, you have to use the single quotes `''` or the double quotes `""` or else it won't work.

`/!\ IMPORTANT` _If_ you specify `<ebaccount>`, this Github user **MUST** have all the three repositories of EasyBuild (and the VSC-base library), even if you don't use all of them.

### Top Source path `$srcpath`

The parent path of the directory in which the [`Resif control`](https://github.com/ULHPC/modules) repository should / has been cloned.
In particular, all operations (testing / building / installing) are operated from this directory.

The layout of this directory shall typically reflect the following topology:

<pre>
$srcpath
 ├── Gemfile[.lock]   # bundler stuff
 ├── README.md
 ├── Rakefile         # main rakefile 
 ├── VERSION          # current release of the repository
 ├── contribs/        # hold the contributed scripts (bash / zsh completion etc.)
 ├── config/          # hold configurations
 │   └── default.yaml # Default Resif configuration
 │   └── ulhpc.yaml   # configuration for the ULHPC platform deployment
 └── swsets/          # YAML definitions for the software sets
 ├── easybuild/
 │   ├── easyblocks/  # Easyblocks clone
 │   ├── easyconfigs/ # Easyconfigs
 │   ├── framework/   # EasyBuild framework
 └─  └── vsc-base/    # VSC base library
</pre>

Default value:

| Variable   | value            |
|------------|------------------|
| `$srcpath` | $HOME/.resif/src |

__See also__: [Layout and Versioning](layout-and-versioning.md)

### Configuration file `$configfile`

Path to a configuration file that defines several options to use instead of the default ones.

The syntax to follow is from YAML and is the following:  
```yaml
option_name: option_value
```
Except for `$swsets` for which the syntax is:  
```yaml
swsets:
    - value1
    - value2
```

To find information on the available option names and possible values, see the [corresponding page](https://gitlab.uni.lu/modules/infrastructure/wikis/Command-line-interface) of the documentation.

### Software set to deploy `$swsets`

Management of software / module sets for which different policies applies, at least:

* `core`: set of software present by default, which deserve a special attention (automatic software testing reported on Cdash, etc.)
* `ulhpc`: in addition to core, all built software availaible to the users of the [UL HPC platform](http://hpc.uni.lu).

In practice, each software set is assigned a dedicated section of the YAML configuration file `software_sets.yaml` precising the software it holds, for instance:

```yaml
core:
  - GCC-4.8.1.eb
  - GCC-4.9.1.eb
ulhpc:
  - GCC-4.8.2.eb
```

We can imagine to extend the notion of software sets to match the expectations of a given research group in terms of software to be used on the platform, prior to its addition to the `core` set.

Default value:

| Variable  | value |
|-----------|-------|
| `$swsets` | core  |

### Module Naming Scheme `$mns`

The module naming scheme affect the way the modules (resp. the software packages) are organized behind the `<modulesroot>` (resp. the `<packageroot>`) directory.
In particular, they are installed in  their own subdirectory following the active module naming scheme, which can be one of the following:

| Naming Scheme   | Software package/Modulefiles subdirectory layout            | Example                                  |
|-----------------|-------------------------------------------------------------|------------------------------------------|
| EasyBuildMNS    | `<name>/<version>-<toolchain><versionsuffix>`               | OpenFOAM-2.1.1-goolf-1.4.10              |
|                 |                                                             | ABySS-1.3.4-ictce-5.3.0-Python-2.7.3     |
| HierarchicalMNS | `<moduleclass>/<toolchain>/<name>/<version>`                | CAE/goolf-2.1.1/OpenFOAM/2.1.1           |
|                 |                                                             | Bio/ictce-5.3.0/ABySS/1.3.4              |
| ThematicMNS     | `<moduleclass>/<name>/<version>-<toolchain><versionsuffix>` | Bio/ABySS/1.3.4-ictce-5.3.0-Python-2.7.3 |
|                 |                                                             | compiler/GCC/4.8.2                       |

Typical toolchains supported on the UL HPC platform includes (see also `eb --list-toolchains`):

* `goalf`: GCC, OpenMPI, ATLAS, ScaLAPACK, FFTW,
* `goolf`: as above, yet with OpenBLAS replacing ATLAS
* `goolfc`: as above, with CUDA
* `ictce`:  Intel Cluster Studio components with Intel Compilers, iMPI stack, iMKL

Default value:

| Variable | value       |
|----------|-------------|
| `$mns`   | ThematicMNS |

### Build mode `$buildmode`

**Not yet implemented.**

The way the software package are built, _i.e._ either locally (`local`) or via job submission on the platform (`job`). Default value:

| Variable     | value |
|--------------|-------|
| `$buildmode` | local |

### Application Root directory `$apps_root`

The root directory hosting both the software package and the corresponding modules. Default value:

| Variable     | value              |
|--------------|--------------------|
| `$apps_root` | $HOME/.local/resif |

### RESIF branch `$branch`

The branch to use for all the files considering RESIF. By default, it is the one pointed by the HEAD.
   
### Release to deploy `$release` and corresponding sub-directory `$releasedir`

For all deploying situations, we wish to force the specification of a specific _release_ to consider corresponding to any valid git tag / commit / branch of the `$srcpath` repository with the following convention:

* if `$release == HEAD`, then deploy under the sub-directory named with the current branch _i.e._ `<branch>/v<MAJOR>.<MINOR>`
* if `$release` correspond to a tag, try to find it in the git branch (`production` most probably), then deploy under the sub-directory `tag/<tag>`
* otherwise, `$release` shall corresponds to a commit sha1. Use it as reference and deploy it under the sub-directory `commit/<sha1>`

Default value:

| Variable      | value                           |
|---------------|---------------------------------|
| `$release`    | HEAD                            |
| `$releasedir` | <branch>/v<major>.<minor>-date> |

_Ex_: `production/v0.6` 


### Root installation directory `$rootinstall`

Place holder for all installation. Default value:

| Variable       | value                    |
|----------------|--------------------------|
| `$rootinstall` | <apps_root>/<releasedir> |

_Ex_: `/opt/apps/production/v0.6-20141117`

### Install directory `$installdir`

When using the `build` sub-command, if you don't want to install your software in the rootinstall (adding them to the already existing installation), you can specify this variable.  
The softwares will be installed in the path given, e.g in `<installdir>/modules` and `<installdir>/software`.

### Sources path `$eb_sourcepath`

The directory in which EasyBuild looks for software source and install files.

Default value:

| Variable         | value                         |
|------------------|-------------------------------|
| `$eb_sourcepath` | <rootinstall>/.ebdirs/sources |

### Build path `$eb_buildpath`

Each software package is (by default) built in a subdirectory of the specified buildpath under `<name>/<version>/<toolchain><versionsuffix>`

Using `/dev/shm` as build path can significantly speed up builds, if it is available and provides a sufficient amount of space.

Default value:

| Variable        | value                       |
|-----------------|-----------------------------|
| `$eb_buildpath` | <rootinstall>/.ebdirs/build |

### Repository and repository path `$eb_repository` `$eb_repositorypath`

`$eb_repository`: The type of repository that is going to be used to store the easyconfig files of the successfully installed software.  
`$eb_repositorypath`: The path to this repository and depending of the type repostiry chosen, you can also specify a subdirectory in which store the files inside the repository (see below).

Different configurations possible:  
- Flat file repository:

    $eb_repository = FileRepository
    $eb_repositorypath = <path>
where <path> is the path to a directory in which to store the files.
- Git repository:

    $eb_repository = GitRepository
    $eb_repositorypath = <path>,<subdir>
where <path> is the path to the git repository (can be an url) and <subdir> is optional and defines a subdirectory in the git repository in which to store the files.
- SVN repository:

    $eb_repository = SvnRepository
    $eb_repositorypath = <path>,<subdir>
where <path> is the path to the svn repository (can be an url) and <subdir> is optional and defines a subdirectory in the svn repository in which to store the files.

If you add the `<subdir>`, do not put any spaces between the two fields (e.g: /path/to/repo,path/to/subdir and not /path/to/repo, path/to/subdir) as it is considered as a single value, not two separate
ones.

Note that to work properly, the SvnRepository and the GitRepository require some tools that are not installed by default. (See EasyBuild documentation for more details)

Default values:

| Variables            | values                        |
|----------------------|-------------------------------|
| `$eb_repository`     | FileRepository                |
| `$eb_repositorypath` | <rootinstall>/.ebdirs/eb_repo |

### Additional EasyBuild options `$eb_options`

Use this variable to tweak the behavior of EasyBuild more in depth for options that are not supported directly by RESIF.

As an example to run the command as a "dry run":

      resif build --eb-options "--dry-run" core

### Admin mode `$out_place`

If set to `False`,  this will change the behavior of the `build` subcommand so that the EasyBuild files (sources, builds, easyconfigs repository) are going to be put inside the rootinstall (in the `.ebdirs` subdirectory).  
**Note** that it doesn't concern the modules and software files. Where you put these ones depends on the `$rootinstall` and the `$installdir` variables.

Note that all of this is overriden by the other options managing these variables (the EASYBUILD environement variables in particular)

### Overwrite flag `$overwrite`

If set to `True`, RESIF will remove any existing file at the location you want to make the install. If set to `False`, RESIF will stop its execution and throw an error message if it find existing files at the install location.

### Prepend & append modulepath `$prepend_modulepath` `$append_modulepath`

Use these variables to prepend (`$prepend_modulepath`) and/or append (`$append_modulepath`) paths to the MODULEPATH environment variable in the LOADME files when using the `resif bootstrap` and `resif cleaninstall` commands.

Also, when using `resif cleaninstall`, any software already installed in any of these paths will not be installed once again inside the software stack.
