# Revolutionary EasyBuild-based Software Installation Framework (RESIF)

The objective of this repository is to pilot in an easy way the building process of software used within the [UL HPC](http://hpc.uni.lu) platform.

Wished features:

* Automatic Management of [Environment Modules](http://modules.sourceforge.net/) deployment
* Fully automates software builds and supports all available toolchains
* Clean (hierarchical) modules layout to facilitate its usage
* Easy to use
* Minimal requirements (Python 2.x, Ruby >= 1.9.3, Environment modules (Tcl/C or Lmod) 
* Management of _software / module sets_ for which different policies applies, for instance:
  * `core`: set of software present by default, who deserve a special attention (automatic software testing reported on Cdash, etc.)
  * `ulhpc`: in addition to core, all **built** software availaible to the users
* Coherent workflow for both the UL HPC sysadmins and users to cover the following scenarios:
  * [admin] Deployment from scratch of a new software stack
  * [user]  Build a new software on top of the existing stable stack
  * [power user]  as above, and contribute back to the deployed infrastructure (pull request etc.)
  * [admin] add a new software to a software set, on top of the existing stable stack
  * [admin] test the successful _building_ of a given software set (in `/tmp/` or `/dev/shm`) 
  * [admin] prepare a new major / minor / patch release 
* Reproducible and self-contained deployment, coupled with a strongly versioned release mechanism to facilitate access to old environments

For this purpose, the proposed workflow relies heavily on [Easybuild](http://hpcugent.github.io/easybuild/), a flexible framework for building/installing (scientific) software. 
