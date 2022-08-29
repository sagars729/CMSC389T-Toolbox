# CMSC389T-Toolbox

## Welcome!

A toolbox for facilitating CMSC388T/CMSC389T. This toolbox will include important
scripts and actions that are useful for managing CMSC388T/CMSC389T. This README
will document how to use this toolbox. 

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

## Setting up an Organization

At the start of each semester, the facilitators need to create an organization
that hosts all repositories and teams for students and facilitators. The
`Setup Organization` action will set up a new organization with teams and
starter repositories. This action has two parameters:
- organization: the name of the organization to set up
- admins: a space separated list of admin github usernames

From the command line,
```bash
gh workflow run 'Setup Organization' --ref main -f organization=cmsc389T-fall22 \
  -f admins='sagars729 nkrishnan19 username3 username4'
```

You can also use the Actions tab to run the worfklow from GitHub with the same
parameters.
