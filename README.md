# Grapevine Leafroll associated Virus Complex-3 (GLRaV-3) detection with AVIRIS-NG imagery
A repository for projects related to the Cornell Institute for Digital Agriculture

### Abstract
Crop disease threatens agricultural sustainability worldwide. Developing actionable early detection and warning systems for agricultural stakeholders, such as growers and field managers, is crucial to reduce the negative financial and environmental impacts of crop disease, whose losses currently exceed $200B USD annually. Agricultural stakeholders primarily rely on visual scouting and molecular testing reports to identify disease, however these practices are challenging to scale from both a financial and labor perspective. Spectroscopic imagery (SI) can improve crop disease management by offering decision-makers accurate disease maps derived from scalable Machine Learning (ML) models. However, training and deploying ML models on SI requires significant computation and storage capabilities, which limits stakeholder use. This challenge will only become greater as high-resolution, global scale data from forthcoming satellite systems such as Surface Biology & Geology (SBG) becomes available. Here, we present a simple, rapid, reliable, cloud-hosted architecture to streamline crop disease detection with SI from NASA's Airborne Visible/Infrared Imaging Spectrometer Next Generation (AVIRIS-NG) and grapevine leafroll associated virus complex 3 (GLRaV-3) in wine grape as a model system. The software system was designed with three goals in mind. First, we showcase new techniques for processing and refining spectroscopic imagery to produce disease incidence models. Second, we demonstrate a cloud-based disease detection system whose underlying principles allow it to flexibly accommodate model improvements and shifting data modalities. The third goal of our work is to make the insights derived from SI available to agricultural stakeholders via a platform designed with their needs and values (e.g. data privacy) in mind. To this end, we illustrate the efficacy of ML models developed for GLRaV-3 detection in a cloud-native environment that does not retain potentially proprietary stakeholder data (e.g. exact field locations) within it. The key outcome of this work is an innovative, responsive system foundation that can empower agricultural stakeholders to make data-driven disease management decisions with SI, while serving as a framework for others pursuing use-inspired application development for agriculture to follow that ensures social impact and reproducibility while preserving stakeholder privacy.

### About the repository
The repository hosts 
projects and ideas from the __Software-Defined Farm Working Group__, where the focus is building computing systems that complement the work of farmers, both small and industrial, in their quest to be profitable while maximizing sustainability efforts.

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

### Questions?
Please contact _*fer26@cornell.edu*_
