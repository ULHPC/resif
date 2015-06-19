-*- mode: markdown; mode: visual-line; fill-column: 80 -*-
`overview.md`

Copyright (c) 2014 [Sebastien Varrette](mailto:<Sebastien.Varrette@uni.lu>) [www]()

        Time-stamp: <Ven 2014-11-14 16:05 svarrette>

-------------------

# Overview and Underlying Tools

## [Environment Modules](http://modules.sourceforge.net/)

Environment modules are a standard and well-established technology across HPC sites, to permit developing and using complex software builds with dependencies, allowing multiple versions of software stacks and combinations thereof.

[Modules](http://modules.sourceforge.net/) -- Software Environment Management, offers a standard and well-established approach common to most HPC facilities to provide complex [tweaked] software and libraries with dependencies in multiple versions to their users.

The tool in itself is used to manage environment variables such as `PATH`, `LD_LIBRARY_PATH` and `MANPATH`, enabling the easy loading and unloading of application/library profiles and their dependencies.

    | Command                        | Description                                                   |
    |--------------------------------+-------------------------------------------------------------- |
    | `module avail`                 | Lists all the modules which are available to be loaded        |
    | `module load <mod1> [mod2...]` | Load a module                                                 |
    | `module unload <module>`       | Unload a module                                               |
    | `module list`                  | List loaded modules                                           |
    | `module display <module>`      | Display what a module does                                    |
    | `module purge`                 | Unload all modules (purge)                                    |
    | `module use <path>`            | Prepend the directory to the MODULEPATH environment variable  |
    | `module unuse <path>`          | Remove the directory from the MODULEPATH environment variable |
    |                                |                                                               |

*Note:* for more information, see the reference man pages for [modules](http://modules.sourceforge.net/man/module.html) and [modulefile](http://modules.sourceforge.net/man/modulefile.html), or the [official FAQ](http://sourceforge.net/p/modules/wiki/FAQ/).

You can also see the following pages on the [UL HPC website](http://hpc.uni.lu/users/):

* [modules page](https://hpc.uni.lu/users/docs/modules.html).
* [programming page](https://hpc.uni.lu/users/docs/programming.html)

At the heart of environment modules interaction resides the following components:

* the `MODULEPATH` environment variable, which defined the list of searched directories for modulefiles
* `modulefile` (see [an example](https://www.nersc.gov/assets/modulefile_example)) associated to each available software. 

Example of layout:

     $>  pwd
	 /path/to//modulefiles/hopper/myzlib

     $> ls -al
	 total 640
	 drwxrwsr-x  2 xxx xxx  131072 2013-03-24 11:14 .
	 drwxrwsr-x 11 xxx xxx  131072 2013-03-24 11:16 ..
	 -rw-rw-r--  1 xxx xxx    1656 2013-03-24 11:14 1.2.7

     $> cat 1.2.7
	 #%Module1.0
     ##
	 
     ## Required internal variables
	 set		name		zlib
	 set		version		1.2.7
	 set		root		/usr/common/usg/$name/$version
	 [...]



## [Lmod](https://www.tacc.utexas.edu/research-development/tacc-projects/lmod)

[Lmod](https://www.tacc.utexas.edu/research-development/tacc-projects/lmod)  is a [Lua](http://www.lua.org/) based module system that easily handles the `MODULEPATH` Hierarchical problem.

Lmod is a new implementation of Environment Modules that easily handles the MODULEPATH Hierarchical problem. It is drop-in replacement for TCL/C modules and reads TCL modulefiles directly.
In particular, Lmod add many interesting features on top of the traditional implementation focusing on an easier interaction (search, load etc.) for the users.

* [User guide](https://www.tacc.utexas.edu/research-development/tacc-projects/lmod/user-guide)
* [Advanced user guide](https://www.tacc.utexas.edu/research-development/tacc-projects/lmod/advanced-user-guide)
* [Sysadmins Guide](https://www.tacc.utexas.edu/research-development/tacc-projects/lmod/system-administrators-guide)


## [Easybuild](https://hpcugent.github.io/easybuild)

* [Reference documentation](http://easybuild.readthedocs.org/)

[Easybuild](https://hpcugent.github.io/easybuild) is a software build and installation framework that allows you to manage (scientific) software on High Performance Computing (HPC) systems in an efficient way.
It is motivated by the need for a tool that combines the following features:

* a __flexible framework__ for building/installing (scientific) software
* fully __automates__ software builds
* full support and setup of [Environment Modules](http://modules.sourceforge.net/) or Lmod, eventually with a hierarchical layout
* divert from the standard `configure / make / make install` with custom procedures
* allows for easily __reproducing__ previous builds
* keep the software build recipes/specifications __simple and human-readable__
* supports __co-existence of versions/builds__ via dedicated installation prefix and module files
* enables __sharing__ with the HPC community
* automagic __dependency resolution__
* retain logs for traceability of the build processes

For all these reasons, Easybuild has been selected as the reference middleware to handle the building and the installation of the software provided via the modules environment.

On top of the above features, the objective is also to permit to HPC users and newbies to easily build a non-provided software (instead of an admin ;)) on top of the provided software/toolchain stack.
In particular, instead of digging through some installation documentation, fighting with some `--prefix` issue to handle our classical rtfm suggestion (_i.e._ "we have no time now so install it in your homedir"), it might be as simple as:


     # Search for an existing Easyconfigs file for 
     $> eb --search mysoft
	 [...]
	 * $CFGS1/mysoft-3.5-goolf-1.4.10-dmpar.eb
	 * $CFGS1/mysoft-3.5-ictce-4.1.13-dmpar.eb
	 [...]
	 
     # install it 
	 $> eb mysoft-3.5-goolf-1.4.10-dmpar.eb --robot

Once the installation has succeeded, modules will be available for `mysoft` and all of its dependencies with the classical `module load mysoft`.



