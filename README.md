<p align="center">
<img src="https://github.com/YuncongMa/pNet/assets/20191790/942fd973-92bb-4839-887e-7505c57a23e9"  width="800">
</p>

# <br /> pNet: A toolbox for personalized functional network modeling <br />
<p align="center">
<img width="800" src="https://github.com/YuncongMa/pNet/assets/20191790/8e84d7bc-3f9b-48e7-9720-85bd65729c6f">
</p>

* This toolbox is designed to extract personalized functional networks from fMRI data.  <br />
* It is implemented with our spatial-regularized non-negative matrix factorization [**SR-NMF**](https://doi.org/10.1016/j.neuroimage.2017.05.004) and Group-Information-Guided Independent Component Analysis [**GIG-ICA**](https://dx.doi.org/10.1016/j.neuroimage.2012.11.008) to compute personalized FNs. <br />
* It works with both [MATLAB](https://github.com/YuncongMa/pNet/tree/main/MATLAB) and [Python](https://github.com/YuncongMa/pNet/tree/main/Python), and comes with a user-friendly GUI interface in MATLAB, as well as a step-by-step guide to setup a customized workflow script in Python.<br />
* It supports both surface and volume based fMRI data, and multiple fMRI formats, including CIFTI, MGH, MGZ, NIFTI, and MAT.<br />
* It allows input of precomputed group-level FN definition. <br />
* It outputs results of both group-level and personalized FNs, and their visualization graphs, as well as quality control and web-based report.


# Installation
1. The MATLAB version requires MATLAB no older than 2021A. Its GUI version can be accessed by openning pNet.mlapp, or install the pNet.mlappinstall as a MATLAB APP. It can also be compiled into a software, which requires the free MATLAB runtime software at https://www.mathworks.com/products/compiler/matlab-runtime.html. Details can be found in the README.txt in each subfolder containing the compiled pNet.
2. The Python version can run in Conda environment or with Docker (https://www.docker.com). The Python version is available at https://github.com/YuncongMa/pNet/tree/main/Python. Installation details can be found in the README located in the Python folder (https://github.com/YuncongMa/pNet/tree/main/Python#readme). The docker file can be downloaded from [Google Drive](https://drive.google.com/drive/folders/15xBnVnyV79fzmjXG-VrCvtRs_nJa2vEA?usp=share_link).
4. Additional installation information can be found in the help document (/MATLAB/Manual_MATLAB.pdf and /Python/Manual_Python.pdf).


# GUI
The MATLAB version features an intuitive user interface (/MATLAB/GUI/pNet.mlapp) to configure the workflow, carry out the computation and check the results. <br />

<p align="center">
<img src="https://github.com/YuncongMa/pNet/assets/20191790/f5168794-63d2-4076-92c9-8ca3d78e478f" width="800">
</p>

(A) The data input module for loading fMRI scans and brain template files. <br />
(B) A module to setup computation parameters of our spatial-reguarlized NMF method. <br />
(C) Surface-based visualization of both group and personalized FNs (k=17) using HCP S1200 dataset, with left panel showing a binarized atlas generated from the group FNs and the right panel showing five views of three personalized FNs. All the color bars of intensity maps were set from the maximum value of the map to its half value. <br />
(D) Volume-based visualization of both group and personalized FNs (k=17) from Zhen’s multi-cohort iSTAGING study, with left panel showing a binarized functional atlas generated from the group FNs and the right panel showing a three-slice view of three personalized FNs. <br />
(E) Surface-based visualization of a personalized FN. <br />
(F) Surface-based visualization of the maximum t value (two sample t-test, FDR correction, p-value=0.001) of sex differences of individualized FNs (k=50) of the HCP S1200 dataset. <br />
(G) A module for quality control, showing one scan with two FNs mismatched to their group-level counterparts. <br />


# Step-by-step guidance
The Python version features a customized workflow using command line
This will generate a Python script to run a workflow

<p align="center">
<img src="https://github.com/YuncongMa/pNet/assets/20191790/38efac5d-631a-47d8-a34f-fd686f84602d" width="800">
</p>

# Cluster Computation
pNet provides bash scripts to interact with cluster environment for both MATLAB and Python versions. <br />
The MATLAB version uses bash scripts (/MATLAB/Bash_Script) to perform customized pNet workflows. Users need to submit those bash jobs using terminal commands. <br />
The Python version uses a Python script to generate bash scripts and submit bash jobs to the cluster.

# Manual
Two manuals are provided for MATLAB and Python version respectively <br />
https://github.com/YuncongMa/pNet/blob/main/MATLAB/Manual_MATLAB.pdf
https://github.com/YuncongMa/pNet/blob/main/Python/Manual_Python.pdf


# Modules and workflow
pNet consists of five main modules and a customizable workflow.

<p align="center">
<img src="https://github.com/YuncongMa/pNet/assets/20191790/1734f2e7-8770-49e5-9586-e42ab1a94cd6"  width="600">
</p>


* Data input module loads preprocessed fMRI data, with corresponding brain template files to extract coordination information and facilitate visualization. 
* FN computation module is to carry out computation for group-level and personalized FNs. 
* Visualization module can provide both preconfigured and interative displays
* Quality control module will ensure the reliability of the whole computation. 
* Additionally, statistical analyses can be employed to investigate differences in personalized FNs between groups or their relation to behavioral traits.



# Data Structure
pNet organizes data structure with respect to the six panels of its GUI version: Data Input, FN Computation, Group FN, Personalized FN, Statistics, Quality Control.

<p align="center">
<img src="https://github.com/YuncongMa/pNet/assets/20191790/acfb3332-fb96-4458-98be-fde971c2836d" width="800">
</p>


* Each folder contains setting files, data, or figure files.
* Group FNs and corresponding preconfigured visualization files are in Group_FN.
* Perosnalized FNs of each subject or fMRI scan are stored in sub-folders in Personalized_FN.


# Brain Template
The brain template is to get the brain mask and overlay image (T1/T2) for volume data, 3D coordination for brain surface data.
Five built-in brain templates are available in the subfolder "Brain_Template".
1. HCP surface: subfolder "HCP_Surface". It contains 3D mesh shapes (vertices and faces) and brain masks for two hemishperes.
2. FreeSurfer fsaverage5: "FreeSurfer_fsaverage5". It is similar to HCP surface .
3. MNI volume space: subfolder "MNI_Volume". It contains two MATLAB files "Brain_Mask.mat" and "Overlay_Image.mat".
4. HCP surface-volume: It contains both cortical surface information, and subcortical volume.
5. HCP volume: It is similar to MNI volume space.


# Existing group-level FNs
pNet can load existing group-level FNs as reference to obtain personalized FNs for individual fMRI data. <br />
Here we provided 17 FN results (/Group_FN/HCP_Surface/gFN_17_HCP_Surface.mat) for HCP S1200. <br />
And several sets of FN results (k=17, 25, 50, 75, 100, 125, 150) for iSTAGING (/Group_FN/iSTAGING_Volume/gFN_17_iSTAGING_Volume.mat). <br />
More precomputed gFNs will come in future release.


# Quality Control
Personalized FN modeling methods will enhance the functional homogeneity (ex. average functional connectivity with each network) with functional networks, suggesting better functional representation. <br />
pNet generates a file report for the examination about the one-to-one match between gFNs and pFNs, with another figure about the spatial correspondence.

<p align="center">
  <img src= "https://github.com/YuncongMa/pNet/assets/20191790/22f08f1f-a085-4df8-907b-1f7ae0e23c13"  width="600">
</p>


# Report
pNet generates a HTML-based report to check gFNs, all pFNs with hyperlinks, and quality control.
<p align="center">
<img src= "https://github.com/YuncongMa/pNet/assets/20191790/7996c5a0-971d-4e0b-9cab-4b85f15a3682"  width="600">
</p>


# Hardware requirement
It is recommended to run pNet with CPU at least 4 cores, memory (RAM) at least 16GB, and free disk storage at least 10GB. Large dataset and parallel computation will require more CPU cores, memory space, and disk space. CPU and memory inf, as well as estimated memory usage can be found in the parallel section.The pNet UI requires screen displaying resolution at least 1280x960. It is recommended to use an external montior with reosolution at least 1920x1080. 2k and 4k displays are desirable.


# Example
We provided results of three examples for users to learn how to run the pFN computation, and navigate through the precomputed results. For each example, we provided examples of simulated fMRI data, and precomputed results of real fMRI data. Examples can be accessed on Google Drive: https://drive.google.com/drive/folders/1xkCy-0WqYvPA9ooq8txTdc0GsGC-YXMq?usp=share_link.   <br />

1.	HCP surface data. (2 subject, 2 scans per subject, 400 volumes per scan) in .mat format. Precomputed results of 10 subject data are stored in subfolder "Test_FN17".
2.	PNC surface data (2 subject, 1 scan per subject, 300 volumes per scan) in .mgh format. Precomputed results of 10 subject data are stored in subfolder "Test_FN17".
3.	UKBB volume data (2 subject, 1 scan per subject, 200 volumes per scan) in .nii.gz format. Precomputed results of 10 subject data are stored in subfolder "Test_FN17".


The data organization is as below.

<p align="center">
<img src="https://user-images.githubusercontent.com/20191790/223320985-12aed4d4-6bef-4b23-a9a2-ff67f79eced3.jpg" width="600">
</p>



# Reference
[1] Li H, Satterthwaite TD, Fan Y (2017). Large-scale sparse functional networks from resting state fMRI. Neuroimage 156:1-13. <br />
[2] Cui Z, et al (2020). Individual variation in functional topography of association networks in youth. Neuron, 106(2), 340-353. <br />
[3] Du Y, Fan Y (2013). Group information guided ICA for fMRI data analysis. <br />
[4] Cui Z, et al (2022). Linking Individual Differences in Personalized Functional Network Topography to Psychopathology in Youth. Biological Psychiatry. <br />
[5] Shanmugan S, et al (2022). Sex differences in the functional topography of association networks in youth. Proceedings of the National Academy of Sciences, 119(33), e2110416119. <br />
[6] Zhou Z, et al (2023). Multiscale functional connectivity patterns of the aging brain learned from harmonized rsfMRI data of the multi-cohort iSTAGING study. NeuroImage, 269, 119911. <br />
