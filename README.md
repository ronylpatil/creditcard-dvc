E2E ML Workflow
==============================

Implemented data versioning, model experimentation & CI using DVC, DVClive & GitHub Actions.

[![CI Pipeline](https://github.com/ronylpatil/creditcard-dvc/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/ronylpatil/creditcard-dvc/actions/workflows/ci.yaml)

**Blog :** 

## Installation

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.

## Usage

1. Change the input parameters of `params.yaml`.
2. Run `dvc exp run` to execute the e2e workflow.
 
## Folder Structure

- `/src`: Contains the source code files.
- `/data`: Stores input and output data files.
- `/log`: Store the log files.
- `/dvclive`: Store the logged parameters & metrics. 

## Dataset

- Download the dataset from [here](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud).
--------
