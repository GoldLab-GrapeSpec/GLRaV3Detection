# CIDA
A repository for projects related to the Cornell Institute for Digital Agriculture

### Abstract
The overaraching goal of the [Cornell Institute for Digital Agriculture](https://www.digitalagriculture.cornell.edu/ "CIDA website")  is: how do we feed 10 billion people in 2050 in a __*sustainable*__ manner? That is, as arable lands becomes more scarce with threats such as climate change, how can we feed a growing global population while keeping the planet sustainable for all living creatures. This interdisciplinary initiative brings together researchers from engineering, life, social, and agricultural sciences to solve the most pressing questions facing agri-food systems.

### About the repository
The repository hosts projects and ideas from the __Software-Defined Farm Working Group__, where the focus is building computing systems that complement the work of farmers, both small and industrial, in their quest to be profitable while maximizing sustainability efforts.

#### Data Documentation and Test Data Repo

Test data and miscellaneous documents related to data are kept in [another repository]( https://github.coecis.cornell.edu/beb82/CIDATestData). Test suites run in this codebase should
make reference to a specific commit in the test data repo, to avoid surprises.
Note: we may want to consider using
a BitBucket as an alternative host so we can pull [specific commits from there](https://serverfault.com/questions/117255/git-pull-specific-revision-from-remote-repository); this
could be useful as the history of rapidly changing datasets may become quite large taken in
total.


#### Dealing with line endings on different systems


A good rule of thumb if you experience issues:

```
git config --local core.safecrlf false
git config --local core.autocrlf true
git config --local core.autocrlf true
```

(Optionally replace `--local` with `--global` to make this the default for all of your repositories.)

#### Enabling repository githooks

The githooks are mainly used for safety checks and for bookkeeping, so that problems don't
pop up. Generally the won't run tests, which should be done as a practice and at the CI level.
Each local checkout of a repository should enable githooks by doing:

```
git config --local core.hooksPath .githooks/

```

## Farm Data Server

The [FarmDataServer](FarmDataServer/) project aggregates and serves data from various sources. See the associated [README](FarmDataServer/README.md)  for information on developing and using it.

### Contributions
To contribute, please do the usual `git clone git@github.coecis.cornell.edu:gbr26/CIDA.git`

### Questions?
Please contact _*gbr26@cornell.edu*_
