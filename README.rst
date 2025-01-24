`pNet <https://github.com/MLDataAnalytics/pNet>`__
====

pNet is a Python package of an `algorithm <https://pubmed.ncbi.nlm.nih.gov/28483721>`__ for computing personalized, sparse, non-negative large-scale functional networks from functional magnetic resonance imaging (fMRI) data, facilitating effective characterization of individual variation in `functional topography <https://pubmed.ncbi.nlm.nih.gov/32078800>`__. The personalized functional networks are **comparable across subjects** while maintaining **subject specific variation**, reflected by their **improved functional coherence** compared with their group-level counterparts. The computation of personalized functional networks is accompanied by `quality control <https://pubmed.ncbi.nlm.nih.gov/36706636>`__, with visualization and quantification of their spatial correspondence and functional coherence in reference to their group-level counterparts.

The `algorithm <https://pubmed.ncbi.nlm.nih.gov/28483721>`__ has been successfully applied to studies of `individual variation in functional topography of association networks in youth <https://pubmed.ncbi.nlm.nih.gov/32078800>`__, `sex differences in the functional topography of association networks in youth <https://pubmed.ncbi.nlm.nih.gov/35939696>`__ (replicated in `Reproducible Sex Differences in Personalized Functional Network Topography in Youth <https://www.biorxiv.org/content/10.1101/2024.09.26.615061v1>`__), `functional network topography of psychopathology in youth <https://pubmed.ncbi.nlm.nih.gov/35927072>`__, `dissociable multi-scale patterns of development in personalized brain networks <https://pubmed.ncbi.nlm.nih.gov/35551181>`__, `multiscale functional connectivity patterns of the aging brain <https://pubmed.ncbi.nlm.nih.gov/36731813>`__, `personalized functional brain network topography in youth cognition <https://pubmed.ncbi.nlm.nih.gov/38110396>`__, and `Polygenic Risk Underlies Youth Psychopathology and Personalized Functional Brain Network Topography <https://www.medrxiv.org/content/10.1101/2024.09.20.24314007v2>`__.

.. figure::
   https://github.com/user-attachments/assets/25809dc1-7757-48d0-8d69-c6a23164941b
   :alt: pnet_image

Getting started
---------------

Follow the Installation Instructions to install pNet, and then check out the `APIs <https://pnet.readthedocs.io/en/latest/api.html>`__ and `Examples <https://github.com/MLDataAnalytics/pNet/tree/main/src/pnet/examples>`__ to learn how to get up and running! For visualization issues that might be caused by VTK, please check `TrobubleShooting <https://github.com/MLDataAnalytics/pNet?tab=readme-ov-file#troubleshooting>`__.

Run with a docker image
~~~~~~~~~~~~~~~~~~~~~~~

::

   docker pull mldataanalytics/fmripnet:latest

or

::

   docker pull ghcr.io/mldataanalytics/fmripnet:latest

::

   docker run mldataanalytics/fmripnet -h

Run with a singularity (`SingularityCE <https://cloud.sylabs.io/library/yongfan/collection/fmripnet>`__) image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   singularity pull --arch amd64 library://yongfan/collection/fmripnet:latest

::

   singularity run fmripnet_latest.sif -h

Download and install pNet
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Download pNet
^^^^^^^^^^^^^^^^

::

   git clone https://github.com/MLDataAnalytics/pNet.git

2. Create a new conda environment for pNet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   cd pNet
   conda env create --name fmripnet -f environment_pnet.yml

3. Install pNet
^^^^^^^^^^^^^^^

::

   conda activate fmripnet
   pip install .
   # or pip install fmripnet

Script usages
~~~~~~~~~~~~~

1. Prepare data
^^^^^^^^^^^^^^^

-  A number of preprocessed fMRI scans that have been spatially aligned to a template space (Individual fMRI scans from all subjects can be placed in the same folder. If a subject has multiple separate fMRI scans, it is recommended to create a separate subfolder for each subject and place all of that subject's fMRI scans in the same subfolder. This ensures that the computation results for different subjects are saved in separate subfolders.),
-  A mask image for excluding voxels/vertices of uninterest (The brain mask should be a binary 3D image (1: foreground and 0: background) with the same spatial dimensions as the preprocessed fMRI scans. It is recommended that the brain mask covers the entire gray matter regions of the brain while excluding non-gray matter regions. Additionally, the non-zero regions of the mask should be connected, without any isolated voxels.),
-  A brain template image/surface for visualization.
-  Scripts can be found in `cli folder <https://github.com/MLDataAnalytics/pNet/tree/main/src/pnet/cli>`__ for preparing the brain template data and `precomputed templates <https://github.com/MLDataAnalytics/pNet/tree/main/src/pnet/Brain_Template>`__ are avaiable for data preprocessed with HCP/fMRIprep pipelines. Step-by-step `instructions <https://github.com/MLDataAnalytics/pNet/blob/main/src/pnet/Brain_Template/create_vol_template.md>`__ illustrate how to create a brain template from a gray matter mask and an overlap brain image.

-  Precomputed group FNs 
.. figure:: https://github.com/user-attachments/assets/09ee14d1-5745-4b18-a4e9-8d05dfc0a05f
   :alt: group_FNs

and

.. figure:: https://github.com/user-attachments/assets/0d7c7b1f-024a-4974-8522-35457f1dd3cf
   :alt: vol_group_FNs

are provided in `Group_FNs <https://github.com/MLDataAnalytics/pNet/tree/main/src/pnet/Group_FNs>`__. They can be used to guide the computation of personalized FNs.


2. Example files of scans and configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  An example file with a list of preprocessed fMRI scans:

::

   /cbica/projects/xxx/rfMRI_REST1_LR/rfMRI_REST1_LR_Atlas_MSMAll_hp2000_clean.dtseries.nii
   ...
   /cbica/projects/xxx/rfMRI_REST1_LR/rfMRI_REST1_LR_Atlas_MSMAll_hp2000_clean.dts
   eries.nii

-  An example configration file:

::

   # This is a configuration file for computing personalized functional networks (FNs) given a set of preprocessed fMRI data
   ## input:
   #   1. Provide a txt file with a list of preprocesed fMRI scans, one on each line, as Scan_List.txt
   #   2. Specifiy a brain template file, provide by pnet or prepared with data provided
   #   3. Specify the number of FNs
   ## output:
   #   1. Specify the result folder directory in dir_pnet_result

   [necessary_settings]
   ## Input:
   # a txt file with a list of preprocessed fMRI scan file, one on each line 
   file_scans = "/cbica/home/fanyo/fmripnet/examples/HCP1200_10Surfs.txt"
   # a brain template file. A HCP surface based template is set here, prepared by pnet 
   file_Brain_Template = "/cbica/home/fanyo/.conda/envs/fmripnet/lib/python3.8/site-packages/pnet/Brain_Template/HCP_Surface/Brain_Te   mplate.json.zip"
   # the number of FNs to be computed, should be a positive integer number
   K = 2
   ## Output: setup the output folder
   dir_pnet_result = "/cbica/home/fanyo/comp_space/pNet/examples/FN2_Surface_hpc"

   ## specify the method for computing personalized FNs: SR-NMF or GIG-ICA
   # for GIG-ICA group level FNs (file_gFN) have to be provided
   # and gFN_settings will be ignored
   method="SR-NMF"

   ## date type and format information
   # data type is surface
   dataType = "Surface"
   # data format is HCP surface
   dataFormat = "HCP Surface (*.cifti, *.mat)"

   [pFN_settings]
   ## for computing personalized FNs based on given fMRI scans/cbica/home/fanyo/fmripnet/examples
   # Specify group level FNs if avialable. If not, the group level FNs will be computed first
   file_gFN = "None"

   [gFN_settings]
   ## for computing FNs at a group level by boostrapping the input data
   # Setup number of scans loaded for each bootstrap run for estimating gFNs
   # a larger number is preferred for robustness, but should be no larger than the avaiable scans
   sampleSize = 10  # typical value: 100
   # Setup number of runs for bootstraps
   # a larger number is preferred for robustness, but with increased computational cost
   nBS = 5        #typical value: 50
   # a number of time points for computing group FNs with bootstraps
   # this is for reducing the computational cost by using a partion of all avaiable time points of each fMRI scan
   # for short fMRI scans all available time points should be used for robustness
   nTPoints = 300   # all avaiable time points will be used if seting a value larger than the available number of time points

   ####################################################################################
   # the following is ignored if no HPC computation (with sge or slurm) will be used  #
   ####################################################################################
   [hpc_settings]
   [hpc_settings.pnet_env]
   # specify pnet installation information
   dir_pnet="/cbica/home/fanyo/.conda/envs/fmripnet/lib/python3.8/site-packages/pnet"
   dir_env="/cbica/home/fanyo/.conda/envs/fmripnet"
   dir_python="/cbica/home/fanyo/.conda/envs/fmripnet/bin/python"

   # specify pnet
   [hpc_settings.submit]
   # Setup qsub commands
   submit_command = "sbatch --parsable --time=0:50:00" # "qsub -terse -j y"
   thread_command = "--ntasks-per-node=" #-pe threaded "
   memory_command = "--mem="                   #"-l h_vmem="
   log_command = "--output="  #"-o "

   [hpc_settings.computation_resource]
   # Computation resource request
   memory_bootstrap= "100G"
   thread_bootstrap= 2
   memory_fusion= "10G"
   thread_fusion= 4
   memory_pFN= "10G"
   thread_pFN= 1
   memory_qc= "10G"
   thread_qc= 1
   memory_visualization= "20G"
   thread_visualization= 1

3. Run the computation (examples can be found in examples folder)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  a script (fmripnet.py) can be found in cli folder for running the
   computation, supplied with a configuration file (\*.toml) for setting
   the input and output information

::

      run "python fmripnet.py -h " to get help information
      run "python fmripnet.py -c a_config.toml" to start the computation without HPC
      run "python fmripnet.py -c a_config.toml --hpc" to start the computation on a HPC cluster with sge or slurm

Code examples and usages
~~~~~~~~~~~~~~~~~~~~~~~~

.. _prepare-data-1:

1. Prepare data
^^^^^^^^^^^^^^^

::

   1) a number of preprocessed fMRI scans that have been spatially aligned to a template space,
   2) a mask image for excluding voxels/vertices of uninterest,
   3) a brain template image/surface for visualization

2. Setup the computation
^^^^^^^^^^^^^^^^^^^^^^^^

::

   1) the number of functional networks,
   2) the output folder information,
   3) optional parameters

3. Example code:
^^^^^^^^^^^^^^^^

::

   import pnet

   # create a txt file of fMRI scans, each line with a fMRI scan 
   file_scan = 'sbj_lst.txt'
   # create a brain template file consisting of information of the mask image and the brain template for visualization or use a template that is distributed with the package) 
   file_Brain_Template = pnet.Brain_Template.file_MNI_vol

   # Setup
   # data type is volume
   dataType = 'Volume'
   # data format is NIFTI, which stores a 4D matrix
   dataFormat = 'Volume (*.nii, *.nii.gz, *.mat)'
   # output folder
   dir_pnet_result = 'Test_FN17_Results'

   # number of FNs
   K = 17

   # Setup number of scans loaded for each bootstrap run for estimating group functional networks
   sampleSize = 100 # The number should be no larger than the number of available fMRI scans. A larger number of samples can improve the computational robustness but also increase the computational cost.  Recommended: >=100
   # Setup number of runs for bootstraps
   nBS = 50         # A larger number of run can improve the computational robustness but also increase the computational cost. recommended: >=10
   # Setup number of time points for computing group FNs with bootstraps
   nTPoints = 200   # The number should be no larger than the number of available time points of the fMRI scans. A larger number of samples can improve the computational robustness but also increase the computational cost.  If not set or larger than the number of available time points (assuming smaller than 9999), all availabe time points will be used.

   # Run pnet workflow
   pnet.workflow_simple(
           dir_pnet_result=dir_pnet_result,
           dataType=dataType,
           dataFormat=dataFormat,
           file_scan=file_scan,
           file_Brain_Template=file_Brain_Template,
           K=K,
           sampleSize=sampleSize,
           nBS=nBS,
           nTPoints=nTPoints
       )


Brain templates and precomputed group FNs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Brain Template
^^^^^^^^^^^^^^^
A brain template provides a brain mask and an overlay structural image for volume data (both in the same space of the preprocessed fMRI data), and 3D coordinates for brain surface data.

- Five built-in brain templates are located in the `Brain_Template <https://github.com/MLDataAnalytics/pNet/tree/main/src/pnet/Brain_Template/>`__ subfolders:

::
   
   HCP Surface: Located in the "HCP_Surface" subfolder, this template contains 3D mesh shapes (vertices and faces) and brain masks for both hemispheres.

   FreeSurfer fsaverage5: Located in the "FreeSurfer_fsaverage5" subfolder, this template is similar in structure to the HCP Surface template.
   
   MNI Volume Space: Located in the "MNI_Volume" subfolder, this template contains two MATLAB files: "Brain_Mask.mat" and "Overlay_Image.mat".

   HCP Surface-Volume: This template contains both cortical surface information and subcortical volume data.
   
   HCP Volume: This template is similar in structure to the MNI Volume Space template.
   
- Scripts and examples for generating custom templates:

   Scripts can be found in `cli folder <https://github.com/MLDataAnalytics/pNet/tree/main/src/pnet/cli>`__ for preparing the brain template data

   `Precomputed templates <https://github.com/MLDataAnalytics/pNet/tree/main/src/pnet/Brain_Template>`__ are avaiable for data preprocessed with HCP/fMRIprep pipelines

   Step-by-step `instructions <https://github.com/MLDataAnalytics/pNet/blob/main/src/pnet/Brain_Template/create_vol_template.md>`__ illustrate how to create a brain template from a gray matter mask and an overlap brain image.


Precomputed group FNs
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Precomputed group FNs are provided in `Group_FNs <https://github.com/MLDataAnalytics/pNet/tree/main/src/pnet/Group_FNs>`__. They can be used to guide the computation of personalized FNs.

Quality Control
~~~~~~~~~~~~~~~

pNet generates a report that facilitates examination of the one-to-one correspondence between group-level functional networks (gFNs) and personalized functional networks (pFNs), including figures illustrating their spatial correspondence and comparing their functional coherence.

.. figure:: https://github.com/user-attachments/assets/36adc816-aefb-470f-9923-5d82b0433007
   :alt: QA_Figures


Reports
~~~~~~

pNet also generates an HTML-based report to facilitate visualization of gFNs, pFNs via hyperlinks, and quality control metrics.

.. figure:: https://github.com/user-attachments/assets/65546842-3784-43b0-8e3e-c089e4ab3cce
   :alt: Report_figures



References
----------

-  Li H, Satterthwaite TD, Fan Y. `Large-scale sparse functional networks from resting state fMRI <https://pubmed.ncbi.nlm.nih.gov/28483721/>`__. **Neuroimage**. 2017 Aug 1;156:1-13. doi: 10.1016/j.neuroimage.2017.05.004. Epub 2017 May 5. PMID: 28483721; PMCID: PMC5568802.
-  Cui Z, Li H, Xia CH, Larsen B, Adebimpe A, Baum GL, Cieslak M, Gur RE, Gur RC, Moore TM, Oathes DJ, Alexander-Bloch AF, Raznahan A, Roalf DR, Shinohara RT, Wolf DH, Davatzikos C, Bassett DS, Fair DA, Fan Y, Satterthwaite TD. `Individual Variation in Functional Topography of Association Networks in Youth <https://pubmed.ncbi.nlm.nih.gov/32078800/>`__. **Neuron**. 2020 Apr 22;106(2):340-353.e8. doi: 10.1016/j.neuron.2020.01.029. Epub 2020 Feb 19. PMID: 32078800; PMCID: PMC7182484.
-  Pines AR, Larsen B, Cui Z, Sydnor VJ, Bertolero MA, Adebimpe A, Alexander-Bloch AF, Davatzikos C, Fair DA, Gur RC, Gur RE, Li H, Milham MP, Moore TM, Murtha K, Parkes L, Thompson-Schill SL, Shanmugan S, Shinohara RT, Weinstein SM, Bassett DS, Fan Y, Satterthwaite TD. `Dissociable multi-scale patterns of development in personalized brain networks <https://pubmed.ncbi.nlm.nih.gov/35551181/>`__. **Nat Commun**. 2022 May 12;13(1):2647. doi: 10.1038/s41467-022-30244-4. PMID: 35551181; PMCID: PMC9098559.
-  Cui Z, Pines AR, Larsen B, Sydnor VJ, Li H, Adebimpe A, Alexander-Bloch AF, Bassett DS, Bertolero M, Calkins ME, Davatzikos C, Fair DA, Gur RC, Gur RE, Moore TM, Shanmugan S, Shinohara RT, Vogel JW, Xia CH, Fan Y, Satterthwaite TD. `Linking Individual Differences in Personalized Functional Network Topography to Psychopathology in Youth <https://pubmed.ncbi.nlm.nih.gov/35927072/>`__. **Biol Psychiatry**. 2022 Dec 15;92(12):973-983. doi: 10.1016/j.biopsych.2022.05.014. Epub 2022 May 18. PMID: 35927072; PMCID: PMC10040299.
-  Shanmugan S, Seidlitz J, Cui Z, Adebimpe A, Bassett DS, Bertolero MA, Davatzikos C, Fair DA, Gur RE, Gur RC, Larsen B, Li H, Pines A, Raznahan A, Roalf DR, Shinohara RT, Vogel J, Wolf DH, Fan Y, Alexander-Bloch A, Satterthwaite TD. `Sex differences in the functional topography of association networks in youth <https://pubmed.ncbi.nlm.nih.gov/35939696/>`__. **Proc Natl Acad Sci U S A**. 2022 Aug 16;119(33):e2110416119. doi:   10.1073/pnas.2110416119. Epub 2022 Aug 8. PMID: 35939696; PMCID: PMC9388107.
-  Keller AS, Pines AR, Shanmugan S, Sydnor VJ, Cui Z, Bertolero MA, Barzilay R, Alexander-Bloch AF, Byington N, Chen A, Conan GM, Davatzikos C, Feczko E, Hendrickson TJ, Houghton A, Larsen B, Li H, Miranda-Dominguez O, Roalf DR, Perrone A, Shetty A, Shinohara RT, Fan Y, Fair DA, Satterthwaite TD. `Personalized functional brain network topography is associated with individual differences in youth cognition <https://pubmed.ncbi.nlm.nih.gov/38110396/>`__. **Nat Commun**. 2023 Dec 18;14(1):8411. doi: 10.1038/s41467-023-44087-0. PMID: 38110396; PMCID: PMC10728159.
-  Zhou Z, Li H, Srinivasan D, Abdulkadir A, Nasrallah IM, Wen J, Doshi J, Erus G, Mamourian E, Bryan NR, Wolk DA, Beason-Held L, Resnick SM, Satterthwaite TD, Davatzikos C, Shou H, Fan Y; ISTAGING Consortium.   `Multiscale functional connectivity patterns of the aging brain learned from harmonized rsfMRI data of the multi-cohort iSTAGING study <https://pubmed.ncbi.nlm.nih.gov/36731813/>`__. **Neuroimage**. 2023 Apr 1;269:119911. doi: 10.1016/j.neuroimage.2023.119911. Epub 2023 Jan 30. PMID: 36731813; PMCID: PMC9992322.
-  Li H, Srinivasan D, Zhuo C, Cui Z, Gur RE, Gur RC, Oathes DJ, Davatzikos C, Satterthwaite TD, Fan Y. `Computing personalized brain functional networks from fMRI using self-supervised deep learning <https://pubmed.ncbi.nlm.nih.gov/36706636/>`__. **Med Image Anal**. 2023 Apr;85:102756. doi: 10.1016/j.media.2023.102756. Epub 2023 Jan 21. PMID: 36706636; PMCID: PMC10103143.
- Keller AS, Sun KY, Francisco A, Robinson H, Beydler E, Bassett DS, Cieslak M, Cui Z, Davatzikos C, Fan Y, Gardner M, Kishton R, Kornfield SL, Larsen B, Li H, Linder I, Pines A, Pritschet L, Raznahan A, Roalf DR, Seidlitz J, Shafiei G, Shinohara RT, Wolf DH, Alexander-Bloch A, Satterthwaite TD, Shanmugan S. `Reproducible Sex Differences in Personalized Functional Network Topography in Youth <https://doi.org/10.1101/2024.09.26.615061>`__. bioRxiv [Preprint]. 2024 Sep 29:2024.09.26.615061. doi: 10.1101/2024.09.26.615061. PMID: 39386637; PMCID: PMC11463432.
* Sun KY, Schmitt JE, Moore TM, Barzilay R, Almasy L, Schultz LM, Mackey AP, Kafadar E, Sha Z, Seidlitz J, Mallard TT, Cui Z, Li H, Fan Y, Fair DA, Satterthwaite TD, Keller AS, Alexander-Bloch A. `Polygenic Risk Underlies Youth Psychopathology and Personalized Functional Brain Network Topography <https://doi.org/10.1101/2024.09.20.24314007>`__. ***medRxiv*** [Preprint]. 2024 Sep 27:2024.09.20.24314007. doi: 10.1101/2024.09.20.24314007. PMID: 39399003; PMCID: PMC11469391.

Troubleshooting
---------------
vtk-osmesa (off-screen MESA):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

If vtk-osmesa (off-screen MESA) cannot be installed with conda (conda install -c conda-forge “vtk>=9.2=\ *osmesa*”), please have a try with pip (a solution provided by `albertleemon <https://github.com/albertleemon>`__):

::

   pip install --extra-index-url https://wheels.vtk.org vtk-osmesa

Support
-------

If you encounter problems or bugs with pNet, or have questions or improvement suggestions, please feel free to get in touch via the `Github issues <https://github.com/MLDataAnalytics/pNet/issues>`__.

Acknowledgment
--------------

This project has been supported in part by NIH grants U24NS130411 and R01EB022573.

Previous versions:
------------------

**Matlab and Python:** https://github.com/MLDataAnalytics/pNet_Matlab

**Matlab:** https://github.com/MLDataAnalytics/Collaborative_Brain_Decomposition

**GIG-ICA:** https://www.nitrc.org/projects/gig-ica/
