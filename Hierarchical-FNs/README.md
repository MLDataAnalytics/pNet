# 📊 Mapping Individualized Multi-Scale Hierarchical Brain Functional Networks from fMRI by Self-Supervised Deep Learning

[![Manuscript](https://img.shields.io/badge/BioRxiv-View%20Manuscript-blue)](https://www.biorxiv.org/content/10.1101/2025.04.07.647618v1.abstract)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-Research%20Prototype-orange)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

---

## 🧠 Overview

This repository provides the implementation of a self-supervised deep learning framework for mapping **individualized multi-scale hierarchical brain functional networks (FNs)** from fMRI data. The method captures both spatially resolved FNs and their inter-scale hierarchical structure, enabling a deeper understanding of brain functional organization and its variability across individuals.

---

## 🧪 Methodology

We present a novel self-supervised deep learning framework that:
- Learns intrinsic representations of fMRI data in a low-dimensional latent space.
- Simultaneously computes multi-scale FNs and characterizes their hierarchical structure.
- Optimizes functional homogeneity across scales in an end-to-end learning manner.

The model is trained on fMRI scans from the Human Connectome Project and generalizes to external cohorts.

---

## 🚀 Key Contributions

- 📌 First framework to jointly estimate individualized multi-scale FNs and their inter-scale hierarchy.
- 🧬 End-to-end self-supervised learning using functional homogeneity as the optimization target.
- 🔁 Generalizable across datasets with robust performance on unseen individuals.

---

## 🧭 Applications

- 🧑‍🔬 Association with biological phenotypes such as sex, brain development, and brain health.
- 🧠 Insights into neurocognitive variability and hierarchical brain organization.
- 🧬 Potential for translational research in neuropsychiatric and neurological disorders.

---
## 🛠️ Getting Started

### System Requirements
* **Python:** 3.8+ (Tested with 3.9.18)
* **PyTorch:** `torch` (1.13.1)
* **NumPy:** `numpy` (1.25.2)
* **NiBabel:** `nibabel` (5.1.0)

The code has been successfully tested on CentOS 7.9. No specialized non-standard hardware is required.

### Installation
No specific installation steps are needed beyond ensuring the system requirements above are met.

---
## 🚀 Demo

We provide a ready-to-use demo to help you get started quickly.

**1. Pre-trained Model**

A pre-trained model, developed using fMRI data from the Human Connectome Project (HCP), is available in the `./model` folder.

**2. Example Data**

Preprocessed resting-state fMRI data for three randomly selected testing individuals are included in the `./example_data` folder.

**3. Running the Demo**

You can directly apply the pre-trained model to the example fMRI data by running the testing script. The script is pre-configured to use the demo model and data.

```bash
python ./code/test_fn_hier_lv3.py
```

* **Output Files:** Individualized multi-scale FNs and Hierarchy Coefficients (HCs) will be saved in the `output/` directory. See the table below for details.
* **Performance:** Computing FNs for one individual (using the example data) typically takes only several seconds on a modern desktop with an NVIDIA TITAN Xp GPU. When running on CPU only, it completes in less than 15 seconds.

**4. Image Padding Instructions**

The output images are in the **HCP MNI152 space** with a shape of **[56, 72, 56]**, but need to be padded to match the original image dimensions of **[61, 73, 61]** (for 3mm scans).

#### 🛠️ Padding and Saving Procedure

To align the output image to the original dimensions and save it as a new NIfTI file, use the following Python code:

```python
import nibabel as nib
import numpy as np

# Load the output image
fn_nii_file = "output_fn.nii.gz"
fn_nii = nib.load(fn_nii_file)
fn_img = fn_nii.get_fdata()

# Get the number of volumes (if 4D)
num_fn = fn_img.shape[-1]

# Create a new padded array with the target shape
fn_img_p = np.zeros((61, 73, 61, num_fn))
fn_img_p[2:58, 0:72, 2:58, :] = fn_img

# Create a new NIfTI image using the original affine and header
fn_nii_p = nib.Nifti1Image(fn_img_p, affine=fn_nii.affine, header=fn_nii.header)

# Save the padded image
nib.save(fn_nii_p, "output_fn_padded.nii.gz")
```

---
## ⚙️ Usage Instructions

### Model Training
1.  Configure your training parameters in the `./code/config_fn_hier_lv3.py` file.
2.  Execute the training script:
    ```bash
    python ./code/train_fn_hier_lv3.py
    ```

### Model Testing
1.  To test the model and generate individualized FNs and hierarchy coefficients, adjust parameters in `./code/config_fn_hier_lv3.py`.
2.  Run the testing script:
    ```bash
    python ./code/test_fn_hier_lv3.py
    ```

### Configuration Details
Detailed comments explaining input and parameter configurations for both training and testing can be found directly within the `./code/config_fn_hier_lv3.py` file.

---
## 📁 Repository and Output Structure

### Repository Structure
| Directory | Description |
|---|---|
| `code/` | Contains all the Python scripts for model training, testing, and configuration. |
| `example_data/` | Provides a small set of preprocessed resting-state fMRI data for demonstration. |
| `model/` | Stores the pre-trained deep learning model for immediate use. |
| `output/` | This directory is where the results will be saved after model testing. |
| `README.md`| This overview and instructions file. |

### Output Files
| File Name | Description |
|---|---|
| `${sbj_id}_fn_l${scale_id}_4d.nii.gz` | Individualized multi-scale FNs. |
| `${sbj_id}_hier_wt_l1to2.npy` | Hierarchy Coefficients (HCs) for fine-to-intermediate scale. |
| `${sbj_id}_hier_wt_l2to3.npy` | Hierarchy Coefficients (HCs) for intermediate-to-coarse scale. |

---
## 📖 Manuscript & Citation
For a comprehensive understanding of our methodology, results, and discussions, please refer to the full manuscript. If you use this code in your research, please consider citing:

**Manuscript:** [bioRxiv: 10.1101/2025.04.07.647618v1](https://www.biorxiv.org/content/10.1101/2025.04.07.647618v1.abstract)

```bibtex

@article {Li2025.04.07.647618,
	author = {Li, Hongming and Zhuo, Chuanjun and Cui, Zaixu and Cieslak, Matthew and Salo, Taylor and Gur, Raquel E. and Gur, Ruben C. and Shinohara, Russell T. and Oathes, Desmond J. and Davatzikos, Christos and Satterthwaite, Theodore D. and Fan, Yong},
	title = {Mapping individualized multi-scale hierarchical brain functional networks from fMRI by self-supervised deep learning},
	elocation-id = {2025.04.07.647618},
	year = {2025},
	doi = {10.1101/2025.04.07.647618},
	publisher = {Cold Spring Harbor Laboratory},
	abstract = {The brain{\textquoteright}s multi-scale hierarchical organization supports functional segregation and integration. Characterizing the hierarchy of individualized multi-scale functional networks (FNs) is crucial for understanding these fundamental brain processes. It provides promising opportunities for both basic neuroscience and translational research in neuropsychiatric illness. However, current methods typically compute individualized FNs at a single scale and are not equipped to quantify any possible hierarchical organization. To address this limitation, we present a self-supervised deep learning (DL) framework that simultaneously computes multi-scale FNs and characterizes their across-scale hierarchical structure at the individual level. Our method learns intrinsic representations of fMRI data in a low-dimensional latent space to effectively encode multi-scale FNs and their hierarchical structure by optimizing functional homogeneity of FNs across scales jointly in an end-to-end learning manner. A DL model trained on fMRI scans from the Human Connectome Project successfully identified individualized multi-scale hierarchical FNs for unseen individuals and generalized to two external cohorts. Furthermore, the individualized hierarchical structure of FNs was significantly associated with biological phenotypes, including sex, brain development, and brain health. Our framework provides an effective method to compute multi-scale FNs and to characterize the inter-scale hierarchy of FNs for individuals, facilitating a comprehensive understanding of brain functional organization and its inter-individual variation.Competing Interest StatementThe authors have declared no competing interest.},
	URL = {https://www.biorxiv.org/content/early/2025/04/07/2025.04.07.647618},
	eprint = {https://www.biorxiv.org/content/early/2025/04/07/2025.04.07.647618.full.pdf},
	journal = {bioRxiv}
}

```
---

## 📬 Contact

For any questions, collaborations, or further information, please feel free to reach out by opening an issue in this repository.

---

## 🙏 Acknowledgment

This project has been generously supported in part by the National Institutes of Health (NIH) through grants **U24NS130411**, **R01EB022573**, and **AG066650**. We are grateful for their support in making this research possible.

