-*- mode: markdown; mode: visual-line; fill-column: 80 -*-
`layout-and-versioning.markdown`

Copyright (c) 2014 [Sebastien Varrette](mailto:Sebastien.Varrette@uni.lu) 

        Time-stamp: <Lun 2014-11-17 01:17 svarrette>

-------------------

# Directory / git / Modules  Layout and Versioning

## Source Repository Layout

The layout of the source repository reflects the topology detailed in the [Variables page](variables.md).

     <srcpath>.
	    ├── ... 
		├── VERSION          # current release of the repository
		├── bin/             # hold some script files (Custom Module Naming scheme and bash completion script)
		├── config/          # hold configurations
		├── easybuild/       # Git subtrees for EB
	    ├── ... 

__See also__ Top Source path `$srcpath` in [Variables](variables.md)

## Releasing mechanism

A [semantic versioning](http://semver.org/) approach is enforced, the current version being stored on the `VERSION` file at the root of the [module-infrastructure](https://gitlab.uni.lu/modules/infrastructure/) repository.
In this context, a version number have the following format:

      <major>.<minor>.<patch>

where:

* `< major >` corresponds to the major version number
* `< minor >` corresponds to the minor version number
* `< patch >` corresponds to the patching version number

Example: `0.1.5`

> Again, the current version number is stored in the file `VERSION`.
> __/!\ NEVER MAKE ANY MANUAL CHANGES TO THIS FILE__

For more information on the version, run:

     $> rake version:info

### Releasing policy 

* MAJOR version increments when incompatible changes applies.
This includes for instance
     - any major change in the [UL HPC platform](http://hpc.uni.lu)  that render the provided software useless or with limited performance (_ex:_ introduction of a new interconnect technology / topology etc.)
     - a new major release of [Easybuild](http://hpcugent.github.io/easybuild/)

* MINOR version increments when functionalities are provided in a backwards-compatible manner.
This includes for instance:
     - a new minor release of [Easybuild](http://hpcugent.github.io/easybuild/)
	 - adding a new software to the `core` software set (implying the testing framework reported on [CDash](http://cdash.uni.lu/index.php?project=UL-HPC-Testing))
	  
* PATCH version increments when backwards-compatible bug fixes / changes are provided.
This includes for instance:
     - adding a new missing software to the `ulhpc` software set

For the sake of simplicity, **only the Major and Minor release lead to a new root directory (named v.X.Y) in the environment modules directory layout**.
In particular, any patch release `X.Y.Z` is applied into the existing `X.Y` environment modules hierarchy.

### Modules Directory layout vs. Releasing

The below layout applies below `$appsroot` (see [Variable](variables.md)), _i.e._ `/opt/apps` in the below examples. 






### Git layout vs. Releasing

__All associated operations are automated by a set of tasks within the `Rakefile`__ (see `rake -T` and all the tasks `rake {git,version}:*`)

The Git branching model for the repository follows the guidelines of [gitflow](http://nvie.com/posts/a-successful-git-branching-model/) -- see this [tutorial](http://blog.jessitron.com/2012/07/skinny-on-git-flow.html) for instance.
The full workflow is illustrated in the below image:

![Gitflow workflow](https://www.atlassian.com/git/images/tutorials/collaborating/comparing-workflows/gitflow-workflow/01.svg) 


In particular, the central repository holds two main __immortal__ branches with an infinite lifetime:

* `production` (_blue_):  the *production-ready* branch. Every commit on this branch is a release version, and thus is tagged with its version number. Also, this is a [protected branch](https://gitlab.uni.lu/modules/infrastructure/protected_branches), meaning it is designed to:
    - prevent push for all except masters.
	- prevent branch from force push
	- prevent branch from removal
	
* `devel` (_violet_): the main branch where the latest developments intervene. Features will be merged in here. This is the *default* branch you get when you clone the repository.

In parallel, [gitflow](http://nvie.com/posts/a-successful-git-branching-model/) allows for three species of __mortal__ branches that come and go:

* `release/v.X.Y.Z` (_cyan_): Release branches, initiated from the `devel` branch upon invocation of the command `rake version:bump:{major,minor,patch}`, which will start the releasing process for you using `git-flow`.
    - `v.X.Y.Z` corresponds to the __exact release version__, in particular the `devel` branch remain in the previous version until the merge and the release is effective (see below)
    - finishing the release is performed via `rake version:release`. This will merges back the commits into the `production` (resp. the `devel`) branch, create a new tag and push remotely all changes. Also, the release branch will be deleted.


* `feature/<name>` (_green_): any new functionality that will be include several commits, initiated from the `devel` branch upon invocation of the command `rake git:feature:start[name]` (or `git flow feature start <name>`). 
     - this branch is local, you might want to publish it remotely using `git flow feature publish <name>`, allowing your colleagues can grab and track it using `git flow feature track <name>`
     - finishing the feature is performed via `rake git:feature:finish` (or `git flow feature finish <name>`). This will merge back the commits back into the `devel` branch. The feature branch is deleted.

* `hotfix/v.X.Y.Z` (_white_):  this branches off the `production` branch, and allow fixes to wind up in a new production release.
     - `v.X.Y.Z` corresponds to the __next release version__, in particular the `production` branch (and thus the `devel` one) remain in the previous version until the merge and the hotfix is effective (see below)
     - finishing a hotfix is performed via `git flow hotfix finish X.Y.Z`.This will merges back the commits into the `production` (resp. the `devel`) branch, create a new tag.
	 - __TODO [SV]__ complete Rakefile task for that



## Installed Apps Directory Layout 

Upon installation in `<appsroot>` (_i.e._ `/opt/apps` by default assuming an admin role), we expect to have the following layout:

<pre>
$appsroot
├── commit
│   └── ecb532e-20141003
├── devel
├── production
│   ├── v0.5 -> v0.5-20140211
│   ├── v0.5-20140211
│   ├── v0.6 -> v0.6-20140611
│   ├── v0.6-20140611
│   └── v0.6-20141007
├── stable -> production/v0.6
├── tag
│   ├── v0.5.0
│   ├── v0.5.1
│   └── v0.6.0
└── testing
    ├── hcartiaux
	├── jflf
	├── svarrette
	├── vplugaru
	└── xbesseron
</pre>

In particular, the following sub-directories are proposed:

* `commit/`: hosting specific commits
* `{devel,production}/`:  hosting the deployment operated from the `devel` (resp. the `production`) branch
* `stable`: a symlink to the current stable release of the platform 
* `tag/`: hosting specific tags, listed by their names
* `testing/`: hosting the tested deployments operated by a specific [power] user, _i.e._ at least the UL HPC sysadmins. 
