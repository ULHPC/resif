-*- mode: markdown; mode: visual-line; fill-column: 80 -*-
`command-line-interface.md`

Copyright (c) 2015 [Sebastien Varrette](mailto:<Sebastien.Varrette@uni.lu>) [www]()

        Time-stamp: <Tue 2015-12-08 21:16 svarrette>

-------------------

# EasyBuild repositories development

## Overview

This document describes the way modifications should be added to the various EasyBuild repositories hosted on the ULHPC github.

## Overview of the repository

The repository contain multiple branches and more will be added as development of EasyBuild goes on. Here is a short description to understand their roles:

* _master_: Branch in sync with the upstream _master_ branch of the corresponding ugent repository.
* _develop_: Branch in sync with the upstream _develop_ branch of the corresponding ugent repository.
* _uni.lu-master_: Branch in sync with _master_ in term of EasyBuild development but with the ULHPC-specific modifications.
* _uni.lu-develop_: Branch in sync with _develop_ in term of EasyBuild development but with the ULHPC-specific modifications.
* _uni.lu-vx.y.z_: Branch containing the version x.y.z of the EasyBuild repository (corresponds to the _easybuild-easyconfigs-vx.y.z_ tag) with the ULHPC-specific modifications.

At all time, the ULHPC-specific modifications should be the same in _uni.lu-master_, _uni.lu-develop_ and _uni.lu-vx.y.z_ should be the same. The next part aims at explaining how to achieve that result.

## Adding ULHPC-specific modifications

When adding new ULHPC-specific modification, the process should be the following:

1. Create a new branch from _uni.lu-master_.
2. Make the modifications on this branch
3. Merge the branch in _uni.lu-master_, _uni.lu-develop_ **and** _uni.lu-vx.y.z_ for all x.y.z posterior to the version in uni.lu-master.

The important part is that you should **not** merge a more recent branch into an older one (for example from _uni.lu-develop_ into _uni.lu-master_) because that would make both branches the same whereas they should not (usually) be.

## Contributing to the ugent repositories

First and foremost, read the [ugent guidelines to contributing back](https://github.com/hpcugent/easybuild/wiki/Contributing-back).

Then, if you want to contribute from the ULHPC repository, use the _develop_ branch (and not the _uni.lu-develop_ branch) and simply respect the general ugent guidelines.
