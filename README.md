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

- [Actions](#Actions)
  - [Setting up an Organization](#Setting-up-an-Organization)
  - [Publishing Projects](#Publishing-Projects)
    - [Publishing a Project](#Publishing-a-Project)
    - [Adding a Submodule to a Published Project](#Adding-a-Submodule-to-a-Project)
  - [Creating a Student Team](#Creating-a-Student-Team)
    - [Create a Student Team](#Create-a-Student-Team)
    - [Update a Student Team](#Update-a-Student-Team)
- [App Scripts](#App-Scripts)
  - [Adding Students](#Adding-Students) 
- [Gradescope](#Gradescope)

# Actions
The actions below can be used to set up and manage the class organization on
GitHub. They can run through the Actions tab on GitHub or by using the 
`gh workflow run` command.

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

## Creating a Student Team

The group projects require creating individual student teams and 
repositories. These teams are nested in the `students` team and 
the repositories are mirrors of the public class repository. 

### Create a Student Team

The `Create Team` action creates a new team and repository for an
individual team. 

#### Parameters

- organization: the name of the organization that we are updating
- team: the name of the team that is being created
- members: a space separated list of members

#### Example

```bash
gh workflow run 'Create Team' --ref main -f organization=cmsc389T-fall22 \
  -f team=Team0 -f members="sagars729 nkrishnan19"
```

### Update a Student Team

The `Update Team` updates a team repository with new changes that
have been pushed to the public repository. As new projects are
released/updated, this action needs to be run to update all team 
repos.

#### Parameters

- organization: the name of the organization that we are updating
- team: the name of the team that is being created

#### Example

```bash
gh workflow run 'Update Team' --ref main -f organization=cmsc389T-fall22 \
  -f team=Team0
```

# App Scripts

## Adding Students

Each semester starts with a Google Form that is used to collect student
information and GitHub usernames. The `add_students.gs` can be linked to
this form to automate adding students to the GitHub organization. The 4
constants will need to be configured to provide the necessary parameters
to GitHub:

- username_field: the title of the field that contains the Github Username
- students_team: the name of the students team (usually `Students`)
- organization: the name of the organization (e.x. `cmsc389T-fall22`)
- github_token: the personal access token with admin access on the org

# Gradescope

To grade projects efficiently and eliminate turnaround time for providing
students feedback, we have automated grading via gradescope.

## Submissions

Instead of a code submission, the necessary data we need for autograding is
one of or a combination of
- A GitHub Repository link (e.x. `https://github.com/sagars729/MyRepo`)
- A GitHub Username (e.x. `sagars729`)
- A Team Name (e.x. `Team1`)

Example 1: For the PacMan project we need the student's GitHub username and
team. An example `submission.txt` file would look like:

```
sagars729
Team1
```

Example 2: For the HelloWorld project, we need the student's repository. An
example `submission.txt` file would look like:

```
https://github.com/sagars729/HelloWorld
```

## Generating an Existing Gradescope Autograder

The `Gradescope` folder contains all autograders we have used in the past.
To create a new autograder,

```bash
cd Gradescope/{project}
zip ~/Downloads/{project}.zip *
```

This will create a new zip file with your autograder in your `Downloads`
folder. 
