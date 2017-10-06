[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1003501.svg)](https://doi.org/10.5281/zenodo.1003501)

# An open library of human kinase domain constructs for automated bacterial expression

This repository contains all code, sequences, and expression data for our abl1 construct screen, 96 kinase expression panel, and Abl1/Src mutant expression test.

## Citation

> **An open library of human kinase domain constructs for automated bacterial expression**
>
> Steven K. Albanese, Daniel L. Parton, Sonya M. Hanson, Lucelenie Rodríguez-Laureano, Mehtap Işık, Julie M. Behr, Scott Gradia, Chris Jeans, Nicholas M. Levinson, Markus A. Seeliger, and John D. Chodera
>
> bioRxiv preprint ahead of submission: [DOI:10.1101/038711](https://doi.org/10.1101/038711)

## Interactive construct expression browser

Browse an [interactive table of kinase expression data and constructs](http://choderalab.github.io/kinome-data/kinase_constructs-addgene_hip_sgc.html).

## Manifest

* `constructs/` - expression constructs and scripts for selecting them, for abl1 construct screen and 96-kinase expression panel
* `expression_data/` - excel files, caliper gels and report from MacroLab for all three expression tests. Contains a combined spreadsheet summarizing three expression tests
* `kinome-database/` - XML database of kinase information used to build this library for the 96-kinase expression panel
* `plasmid_libraries/` - plasmid library data sources
* `manuscript/` - LaTeX manuscript, with figures and bibliography files. Downloaded from overleaf
* `resources/` - CSS resources used for tables
* `mutants-database/` - data of the mutant information gathered for all of the kinases that expressed in the 96-kinase expression test
