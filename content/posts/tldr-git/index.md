---
title: "🚀 TL;DR - Git"
date: 2021-10-17T10:39:42+02:00
summary: "You want to know how to use Git as a chad developper?"
tags: ["dev", "git", "tldr"]
author: "0xNinja"
showToc: true
TocOpen: false
draft: true
hidemeta: false
comments: false
disableShare: false
disableHLJS: false
hideSummary: false
searchHidden: true
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
---

## Git :fire:

> You want to use Git as a real chad developper? Let's go - **f a s t** - then.

### Basics

Git is a decentralized versioning tool aimimg to help programmers following source code development.

* Track file changes
* Update remote code
* Work simultaneously with a lot of people
* Arrange your code organization

Resources:

* https://www.freecodecamp.org/news/learn-the-basics-of-git-in-under-10-minutes-da548267cc91/
* https://rogerdudler.github.io/git-guide/
* https://lab.github.com/lmachens/git-and-github-first-timers

### Create a new project

#### From scratch

```sh
git init
```

#### From an empty repository

```sh
git clone https://myrepo.org/project-0
# or with ssh (use your public key)
git clone git@myrepo.org:username/project-0
```

### Do some modifications

{{< twitter_simple 1387402963652599813 >}}

```sh
vim my_file.txt # haha :rofl: lol my favorite editor
# add the file to the repository
git add my_file.txt

# change the name of the file
git mv my_file.txt README.md

# delete a file
git rm README.md

# commit your changes
git commit -m 'My changes'

# update the repository
git push
# if from scratch
git remote add origin git@myrepo.org:username/project-0
git push -u origin master
```

### Update your repository

```sh
git pull
```

### Advanced mechanics

```sh
# create new branch and push it to repo
git checkout -b my-branch
vim ...; git add ...; git commit ...
git push -u origin my-branch

# update your submodules
git submodule update --remote --merge

# delete a commit
git commit -amend

# temporary discard your local changes
git stash

# config your git variables
git config user.name PouetPouet
```
