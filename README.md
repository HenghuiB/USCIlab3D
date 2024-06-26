# USCILab3D Dataset: A Large-scale, Long-term Outdoor Dataset

Welcome to the repository for the USCILab3D Dataset! This repository contains the code and tools associated with our paper, "USCILab3D Dataset: A Large-scale, Long-term Outdoor Dataset."

## Table of Contents

- [Introduction](#introduction)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Processing Raw Bagfiles](#processing-raw-bagfiles)
  - [Creating SLAM Info](#creating-slam-info)
  - [Dividing Sectors](#dividing-sectors)
  - [Running COLMAP](#running-colmap)
  - [Using GPT-4 and Grounded-SAM](#using-gpt-4-and-grounded-sam)
  - [Projection](#projection)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

This repository provides the code necessary to process and utilize the USCILab3D Dataset, a large-scale, long-term outdoor dataset. The dataset and associated tools are designed for research and development in the fields of computer vision, SLAM (Simultaneous Localization and Mapping), and AI.

## Repository Structure

The repository is organized into two main directories, each with its own README:

- **vision_toolkit**: Contains code for processing raw bagfiles, creating SLAM info, dividing sectors, and running COLMAP.
- **3d2d_ann**: Contains code related to GPT-4, Grounded-SAM, and projection.

## Installation

To get started, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/yourusername/USCILab3D-Dataset.git
cd USCILab3D-Dataset
# Follow the installation instructions in each subdirectory's README
