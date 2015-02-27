-*- mode: markdown; mode: visual-line; fill-column: 80 -*-
`workflow.md`

Copyright (c) 2014 [Sebastien Varrette](mailto:<Sebastien.Varrette@uni.lu>) [www]()

        Time-stamp: <Mar 2014-12-02 11:22 mschmitt>

-------------------

# RESIF  Variables

The workflow revolves around a few variables that are defined below.  
Although it is interesting to take a look at them to personalize an installation, the script can be used without manually setting any of these options since the necessary ones have a default value. 

Here are all the variables that can be set, followed by their descriptions.

      | Variable                | Description                                        | Default (if any)                   |
      |-------------------------+----------------------------------------------------+------------------------------------|
      | `$git_architecture`     | Git URL/path for your architecture repository      | 'https://github.com/ULHPC/modules' |
      | `$ebuser`               | User operating the process                         | `whoami`                           |
      | `$ebgroup`              | Group                                              |                                    |
      | `$gh_ebuser`            | (opt.) Github user ['hpcugent','ULHPC']            |                                    |
      | `$git_ebframework`      | (opt.) Git URL/path for EB framework repo          |                                    |
      | `$git_ebblocks`         | (opt.) Git URL/path for EB easyblocks repo         |                                    |
      | `$git_ebconfigs`        | (opt.) Git URL/path for EB easyconfigs repo        |                                    |
      | `$branch_ebframework`   | (opt.) Git branch for EB framework                 |                                    |
      | `$branch_ebblocks       | (opt.) Git branch for EB easyblocks                |                                    |
      | `$branch_ebconfigs      | (opt.) Git branch for EB easyconfigs               |                                    |
      | `$srcpath`              | Source path for the conf. repository               | $HOME/.resif/src                   |
      | `$configfile`           | Path to custom configuration file                  |                                    |
      | `$swsets_config`        | Path to file defining the software sets            | <srcpath>/config/swsets.yaml       |
      | `$swsets`               | Software set to deploy  ['core','ulhpc']           | core                               |
      | `$mns`                  | Module Naming Scheme     ['EasyBuildMNS',          | ThematicMNS                        |
      |                         |           'HierarchicalMNS', 'ThematicMNS']        |                                    |
      | `$buildmode`            | Local build ('local') vs. job  ('job')             | local                              |
      | `$apps_root`            | Root directory for apps (modules & sw)             | $HOME/.local/resif                 |
      | `$branch`               | Branch of the RESIF repository to work with        |                                    |
      | `$release`              | Release tag or commit to deploy                    | HEAD                               |
      | `$releasedir`           | Subdirectory in which to deploy the release        | <branch>/<release>-<date>          |
      | `$rootinstall`          | Root Installation directory                        | <apps_root>/<releasedir>           |
      | `$installdir`           | Path to an alternative directory in which to build |                                    |
      | `$eb_sourcepath`        | Directory to store software sources                | $HOME/.resif/sources               |
      |                         | and install files                                  |                                    |
      | `$eb_buildpath`         | (temporary) directories to host builds             | $HOME./resif/build                 |
      | `$eb_repository`        | Type of repository to store the .eb files          | FileRepository                     |
      |                         | of the successfuly installed softwares             |                                    |
      | `$eb_repositorypath`    | Path to this repository                            | $HOME/.resif/eb_repo               |
      | `$out_place`            | Modify the building behavior so EasyBuild files    | False                              |
      |                         |   are all put inside the $HOME/.resif directory    |                                    |
      | `$overwrite`            | Set this flag if you want to overwrite any file    | False                              |
      |                         |  that is already present at the install location   |                                    |
 
## Specific Configuration variables

### Git architecture repository `$git_architecture`

Set this variable to a Git URL or path to use another infractructure repository than the default one.

        | Variable          | value                              |
        |-------------------+------------------------------------|
        | $git_architecture | 'https://github.com/ULHPC/modules' |

To learn more about this architecture repository (and learn how to create your own, fitting your needs), go to the [layout and versioning page](https://gitlab.uni.lu/modules/infrastructure/wikis/layout-and-versioning).

### Local user/group deploying the infrastructure `$ebuser` `$ebgroup`

* all processes / jobs are run as this user
* all [sub]directory are assuming having read/write access for that user and/or group

Default value:

      | Variables | value    |
      |-----------+----------|
      | $ebuser   | `whoami` |
      | $ebgroup  |          |

### (optional) Alternatives to the use of the Easybuild subtrees of the [`infrastructure`](https://gitlab.uni.lu/modules/infrastructure) repository

If you do not wish to use the Easybuild subtrees present in the [`modules-infrastructure`](https://gitlab.uni.lu/modules/infrastructure) repository, you might use the following alternative approaches:

* precising the [Github user](https://github.com/) that fork __all three__ Easybuild repositories _i.e_ `easybuild-{framework,easyblocks,easyconfigs}` -- see `$gh_ebuser`
    - in this case, you might wish also to customize the Git branch to consider -- see `$branch_eb{framework,blocks,configs}}`
* __[TODO]__ customizing the Git URLs for the Easybuild repositories -- see `$git_eb{framework,blocks,configs}}`
    - as above, you might wish also to customize the Git branch to consider -- see `$branch_eb{framework,blocks,configs}}`

#### Github user hosting the Easybuild git repository forks `$gh_ebuser`

If you do not wish to use the Easybuild subtrees present in the [`modules-infrastructure`](https://gitlab.uni.lu/modules/infrastructure) repository but rather your own [fork] of easybuild sources (_i.e._), you might precise here the GitHub user.

Default value:

      | Variable     | value |
      |--------------+-------+
      | `$gh_ebuser` |       |

In particular in this case, we expect to find the following repository available:

* Easybuild Framework repository: `https://github.com/<gh_ebuser>/easybuild-framework`
* Easyblocks repository:          `https://github.com/<gh_ebuser>/easybuild-easyblocks`
* Easyconfigs repository:         `https://github.com/<gh_ebuser>/easybuild-easyconfigs`

For each of the above repository, you might wish to specialize the Git branch to consider (`master` by default) using the variables `$branch_eb{framework,blocks,configs}`.

#### Github repositories forks for EasyBuild `$git_framework`, `$git_easyblocks`, `$git_easyconfigs`

If you want to use forks coming from several sources, you can provide directly the URL or path to the git you want to use for a given EasyBuild part.

Note that you can combine this method with the previous one, taking into consideration that the git repository that will be given with this method will be prefered over the first one. E.g if you provide hpcugent as the gh-ebuser and the URL to the ULHPC fork of the easyconfig repository, you will in the end use the framework and the easyblocks from the hpcugent GitHub repositories and the easyconfigs from the ULHPC fork of this repository.

You can specify the branch from the given repository either by using the variables described below (`$branch_ebframework`) and so on) or by using the following syntax for in the current variables:

    'url|branch'
which in an example would look like that:

    'https://github.com/hpcugent/easybuild-framework|master'
for the framework part.  
Note that if you use this syntax you have to use the single quotes `''` or the double quotes `""` or else it won't work.

#### Specifying branch to use for alternative sources `$branch_ebframework`, `$branch_ebblocks`, `$branch_ebconfigs`

You can specify a branch to use. If this options is unused for a given source, then, for this source, the branch used will be the one of the HEAD.

#### Final notes on the alternative sources provisioning

It is important to keep in mind that if you give a gh_ebuser, then this user MUST have all the three repositories of EasyBuild, even if you don't use all of them (by providing a specific repositroy with the second method), although this requirement isn't true with the second method, because any missing repository will be taken from the gh_ebuser if you provide one, or from the subtree if you don't.

### Top Source path `$srcpath`

The parent path of the directory in which the [`modules-infrastructure`](https://gitlab.uni.lu/modules/infrastructure) repository shall / has been cloned.
In particular, all operations (testing / building / installing) are operated from this directory.

The layout of this directory shall typically reflect the following topology:

<pre>
$srcpath
├── Gemfile[.lock]   # bundler stuff
├── README.md
├── Rakefile         # main rakefile 
├── VERSION          # current release of the repository
├── bin/             # hold the scripts piloting all operations
├── config/          # hold configurations
│   └── swsets.yaml  # YAML definitions for the software sets
├── easybuild/
│   ├── easyblocks/  # git subtree for Easyblocks
│   ├── easyconfigs/ # git subtree for Easyconfigs
│   ├── framework/   # git subtree for EasyBuild framework
└─  └── wiki/        # git subtree for the wiki
</pre>

Default value:

      | Variable   | value            |
      |------------+------------------+
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

      | Variable | value |
      |----------+-------+
      | $swsets  | core  |

### Module Naming Scheme `$mns`

The module naming scheme affect the way the modules (resp. the software packages) are organized behind the `<modulesroot>` (resp. the `<packageroot>`) directory.
In particular, they are installed in  their own subdirectory following the active module naming scheme, which can be one of the following:

      | Naming Scheme   | Software package/Modulefiles subdirectory layout            | Example                                 |
      |-----------------+-------------------------------------------------------------+-----------------------------------------|
      | EasyBuildMNS    | `<name>/<version>-<toolchain><versionsuffix>`               | OpenFOAM-2.1.1-goolf-1.4.10             |
      |                 |                                                             | ABySS-1.3.4-ictce-5.3.0-Python-2.7.3    |
      | HierarchicalMNS | `<moduleclass>/<toolchain>/<name>/<version>`                | CAE/goolf-2.1.1/OpenFOAM/2.1.1          |
      |                 |                                                             | Bio/ictce-5.3.0/ABySS/1.3.4             |
      | ThematicMNS     | `<moduleclass>/<name>/<version>-<toolchain><versionsuffix>` | Bio/ABySS/1.3.4-ictce-5.3.0-Python-2.7.3|
      |                 |                                                             | compiler/GCC/4.8.2                      |

Typical toolchains supported on the UL HPC platform includes (see also `eb --list-toolchains`):

* `goalf`: GCC, OpenMPI, ATLAS, ScaLAPACK, FFTW,
* `goolf`: as above, yet with OpenBLAS replacing ATLAS
* `goolfc`: as above, with CUDA
* `ictce`:  Intel Cluster Studio components with Intel Compilers, iMPI stack, iMKL

Default value:

      | Variable | value       |
      |----------+-------------+
      | $mns     | ThematicMNS |

### Build mode `$buildmode`

**Not yet implemented.**

The way the software package are built, _i.e._ either locally (`local`) or via job submission on the platform (`job`). Default value:

      | Variable   | value |
      |------------+-------+
      | $buildmode | local |

### Application Root directory `$apps_root`

The root directory hosting both the software package and the corresponding modules. Default value:

      | Variable   | value              |
      |------------+--------------------|
      | $apps_root | $HOME/.local/resif |

### RESIF branch `$branch`

The branch to use for all the files considering RESIF. By default, it is the one pointed by the HEAD.
   
### Release to deploy `$release` and corresponding sub-directory `$releasedir`

For all deploying situations, we wish to force the specification of a specific _release_ to consider corresponding to any valid git tag / commit / branch of the `$srcpath` repository with the following convention:

* if `$release == HEAD`, then deploy under the sub-directory named with the current branch _i.e._ `<branch>/v<MAJOR>.<MINOR>`
* if `$release` correspond to a tag, try to find it in the git branch (`production` most probably), then deploy under the sub-directory `tag/<tag>`
* otherwise, `$release` shall corresponds to a commit sha1. Use it as reference and deploy it under the sub-directory `commit/<sha1>`

Default value:

      | Variable    | value                            |
      |-------------+----------------------------------|
      | $release    | HEAD                             |
      | $releasedir | <branch>/v<major>.<minor>-date> |

_Ex_: `production/v0.6` 


### Root installation directory `$rootinstall`

Place holder for all installation. Default value:

      | Variable     | value                    |
      |--------------+--------------------------|
      | $rootinstall | <apps_root>/<releasedir> |

_Ex_: `/opt/apps/production/v0.6-20141117`

### Install directory `$installdir`

When using the `build` sub-command, if you don't want to install your software in the rootinstall (adding them to the already existing installation), you can specify this variable.  
The softwares will be installed in the path given, e.g in `<installdir>/modules` and `<installdir>/software`.

### Sources path `$eb_sourcepath`

The directory in which EasyBuild looks for software source and install files.

Default value:

      | Variable        | value                         |
      |-----------------+-------------------------------+
      | $eb_sourcepath  | <rootinstall>/.ebdirs/sources |

### Build path `$eb_buildpath`

Each software package is (by default) built in a subdirectory of the specified buildpath under `<name>/<version>/<toolchain><versionsuffix>`

Using `/dev/shm` as build path can significantly speed up builds, if it is available and provides a sufficient amount of space.

Default value:

      | Variable      | value                       |
      |---------------+-----------------------------+
      | $eb_buildpath | <rootinstall>/.ebdirs/build |

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

      | Variables          | values                        |
      |--------------------+-------------------------------+
      | $eb_repository     | FileRepository                |
      | $eb_repositorypath | <rootinstall>/.ebdirs/eb_repo |

### Admin mode `$out_place`

If set to `True`,  this will change the behavior of the `build` subcommand so that the EasyBuild files (sources, builds, easyconfigs repository) are going to be put inside the rootinstall (in the `.ebdirs` subdirectory).  
**Note** that it doesn't concern the modules and software files. Where you put these ones depends on the `$rootinstall` and the `$installdir` variables.

The new values are then:

      | Variables          | values                                |
      |--------------------+---------------------------------------|
      | $eb_sourcepath     | $HOME/.resif/v<version>-<date>/sources |
      | $eb_buildpath      | $HOME/.resif/v<version>-<date>/build   |
      | $eb_repositorypath | $HOME/.resif/v<version>-<date>/eb_repo |

Note that all of this is overriden by the other options managing these variables (the EASYBUILD environement variables in particular)

### Overwrite flag `$overwrite`

If set to `True`, RESIF will remove any existing file at the location you want to make the install. If set to `False`, RESIF will stop its execution and throw an error message if it find existing files at the install location.
