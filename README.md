# CMSC389T-Toolbox

## Welcome!

This toolbox will include important scripts and actions that are useful for managing 
CMSC388T/CMSC389T. This README will document how to use this toolbox. 

## Before you Start

Actions in this repository will use a personal access token. If you have forked
this repository, you will need to add a personal access token to allow GitHub
Actions to interact with the class organization. If you are a collaborator on
this repository and the token has expired, you will need to add a new secret
called `TOKEN` which contains your personal access token.

The class organization needs to be created manually. Make sure you create and are
an owner of this organization. Otherwise, your won't have the required permissions
to run the scripts below.

- We usually name our organizations `cmsc38{X}T-{season}{year}` e.x. `cmsc389T-fall22`
- Make sure to add a picture for the organization! We usually choose from 
  [Octodex](https://octodex.github.com).

## Table of Contents

- [Setting up an Organization](#Setting-up-an-Organization)
- [Publishing Projects](#Publishing-Projects)
  - [Publishing a Project](#Publishing-a-Project)
  - [Adding a Submodule to a Published Project](#Adding-a-Submodule-to-a-Project)

## Setting up an Organization

At the start of each semester, the facilitators need to create an organization
that hosts all repositories and teams for students and facilitators. The
`Setup Organization` action will set up a new organization with teams and
starter repositories. 

#### Parameters

- organization: the name of the organization to set up
- admins: a space separated list of admin github usernames

#### Example

```bash
gh workflow run 'Setup Organization' --ref main -f organization=cmsc389T-fall22 \
  -f admins='sagars729 nkrishnan19 username3 username4'
```

## Publishing Projects

For this class, we keep two repositories: a private TA repository that contains
all projects before they are released (for internal development) and a public
student repo that contains finalized polished versions of those projects. 

### Publishing a Project
The `Publish Project` action allows facilitators to publish a project from the
private repository to the public repository.

#### Parameters

- organization: the name of the organization that we are updating
- project: the name of the project that is being published/updated

#### Example

```bash
gh workflow run 'Publish Project' --ref main -f organization=cmsc389T-fall22 \
  -f project=P0
```

### Adding a Submodule to a Project

Some projects will require a linked submodule that is generated
from a template repository. The `Publish Project Submodule` action
creates a new repository in the organization from a template and 
adds that new repo as a submodule to an existing project. 

#### Parameters

- organization: the name of the organization that we are updating
- project: the name of the project that is being published/updated
- template: the template repository used to create the new submodule
- name: the new name of the submodule

#### Example

```bash
gh workflow run 'Publish Project Submodule' --ref main -f organization=cmsc389T-fall22 \
  -f project=P0 -f template=sagars729/git-java-setup-template --name=git-java-setup
```
