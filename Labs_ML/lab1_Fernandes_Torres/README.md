# Décision et apprentissage, G3 SDIA, Ecole Centrale de Lille

Read carefully the instructions below to run the Jupyter notebook file (`.ipynb` extension) and complete the lab.

Authors: P.-A. Thouvenin, L. Filstroff

- [Décision et apprentissage, G3 SDIA, Ecole Centrale de Lille](#d%C3%A9cision-et-apprentissage-g3-sdia-ecole-centrale-de-lille)
  - [General guidelines](#general-guidelines)
  - [Working on the computers at Centrale Lille](#working-on-the-computers-at-centrale-lille)
  - [Configuring your personal computer](#configuring-your-personal-computer)

## General guidelines

After retrieving the resources for the lab on moodle:

- place the `.zip archive` in a local folder;
- unzip the `.zip` archive;
- rename the folder with the convention `labX_Name1_Name2` (replacing `X` by the lab number)
- duplicate the notebook file and rename it `labX_Name1_Name2.ipynb`;
- at the end of the session, do not forget to transfer your work to your own network space if you are working on a machine from the school (do not leave your work on the C: drive).

## Working on the computers at Centrale Lille

All packages required for the labs are already installed on the system. The instructions below indicate how to run the notebook, depending on the operating system on which your sessions has been launched.

- Linux / MacOS: open a terminal, and use de `cd` command to move the lab folder. Issue the following commands in the terminal.

  ```bash
  # run jupyter lab
  jupyter lab
  ```

- Windows: open an `Anaconda command prompt` from the startup menu, and use de `cd` command to move the lab folder. Issue the following commands in the terminal.

  ```bash
  # moving to your personal drive on the server (usually D drive)
  D:

  # moving to the unzipped lab archive (replace path as appropriate)
  cd path/to/lab/archive

  # run jupyter lab
  jupyter lab
  ```

## Configuring your personal computer

To configure the lab on your own machine, follow the instructions below to create a `conda` environment using the provided `requirement.txt` file, depending on the operating system (OS) of your computer.

First install Anaconda by following the online documentation, depending on your OS: https://docs.anaconda.com/free/anaconda/install/

- Linux / MacOS: open a terminal, and use de `cd` command to move the lab folder. Issue the following commands in the terminal.

  ```bash
  conda clean --all
  conda update conda

  # moving to the unzipped lab archive (replace path as appropriate)
  cd path/to/lab/archive

  # create conda environment
  conda create --name dap -c conda-forge --file requirement.txt

  # activate environment and start the lab
  conda activate dap

  # run jupyter lab
  jupyter lab

  # to delete the environment if needed
  # conda env remove --name dap
  ```

- Windows: open an `Anaconda command prompt` from the startup menu, and use de `cd` command to move the lab folder. Issue the following commands in the terminal.

  ```bash
  conda clean --all
  conda update conda

  # moving to the unzipped lab archive (replace path as appropriate)
  cd path/to/lab/archive

  # create conda environment
  conda create --name dap -c conda-forge --file requirement.txt

  # activate environment and start the lab
  conda activate dap

  # run jupyter lab
  jupyter lab

  # to delete the environment if needed
  # conda env remove --name dap
  ```

> **Note**: for a faster installation on your machine, consider replacing `conda` by the excellent [`mamba`](https://mamba.readthedocs.io/en/latest/installation.html), an alternative version of `conda` entirely implemented in C++. It's command line interface is exactly the same as `conda` (replace `conda ...` commands by `mamba ...`) In this case, the commands above can be trivially adapted.
