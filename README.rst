pNet
====

pNet is a Python package of an
`algorithm <https://pubmed.ncbi.nlm.nih.gov/28483721/>`__ for computing
personalized, sparse, non-negative large-scale functional networks from
functional magnetic resonance imaging (fMRI) data, facilitating
effective characterization of individual variation in `functional
topography <https://pubmed.ncbi.nlm.nih.gov/32078800/>`__. The
personalized functional networks are **comparable across subjects**
while maintaining **subject specific variation**, reflected by their
**improved functional coherence** compared with their group-level
counterparts. The computation of personalized functional networks is
accompanied by `quality
control <https://pubmed.ncbi.nlm.nih.gov/36706636/>`__, with
visualization and quantification of their spatial correspondence and
functional coherence in reference to their group-level counterparts.

The `algorithm <https://pubmed.ncbi.nlm.nih.gov/28483721/>`__ has been
successfully applied to studies of `individual variation in functional
topography of association networks in
youth <https://pubmed.ncbi.nlm.nih.gov/32078800/>`__, `sex differences
in the functional topography of association networks in
youth <https://pubmed.ncbi.nlm.nih.gov/35939696/>`__, `dissociable
multi-scale patterns of development in personalized brain
networks <https://pubmed.ncbi.nlm.nih.gov/35551181/>`__, `functional
network topography of psychopathology in
youth <https://pubmed.ncbi.nlm.nih.gov/35927072/>`__, `personalized
functional brain network topography in youth
cognition <https://pubmed.ncbi.nlm.nih.gov/38110396/>`__, and
`multiscale functional connectivity patterns of the aging
brain <https://pubmed.ncbi.nlm.nih.gov/36731813/>`__.

.. figure::
   https://github.com/user-attachments/assets/b45d02a1-2c82-43b5-b7d5-42fc38a7b298
   :alt: image


Getting started
---------------

Follow the Installation Instructions to install pNet, and then check out
the `APIs <https://pnet.readthedocs.io/en/latest/api.html>`__ and
`Examples <https://github.com/MLDataAnalytics/pNet/tree/main/src/pnet/examples>`__
to learn how to get up and running!

Run with a docker image
~~~~~~~~~~~~~~~~~~~~~~~

::

   docker pull mldataanalytics/fmripnet:latest

or

::

   docker pull ghcr.io/mldataanalytics/fmripnet:latest

::

   docker run mldataanalytics/fmripnet -h

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

::

   1) a number of preprocessed fMRI scans that have been spatially aligned to a template space,
   2) a mask image for excluding voxels/vertices of uninterest,
   3) a brain template image/surface for visualization
   4) a script can be found in cli folder for preparing the brain template data

2. Run the computation (examples can be found in examples folder)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   5) a script (fmripnet.py) can be found in cli folder  for running the computation, supplied with a configuration file (*.toml) for setting the input and output information
      run "python fmripnet.py -h " to get help information
      run "python fmripnet.py -c a_config.toml" to start the computation
      run "python fmripnet.py -c a_config.toml --hpc qsub" to start the computation on a HPC cluster with qsub

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

References
----------

-  Li H, Satterthwaite TD, Fan Y. `Large-scale sparse functional
   networks from resting state
   fMRI <https://pubmed.ncbi.nlm.nih.gov/28483721/>`__. **Neuroimage**.
   2017 Aug 1;156:1-13. doi: 10.1016/j.neuroimage.2017.05.004. Epub 2017
   May 5. PMID: 28483721; PMCID: PMC5568802.
-  Cui Z, Li H, Xia CH, Larsen B, Adebimpe A, Baum GL, Cieslak M, Gur
   RE, Gur RC, Moore TM, Oathes DJ, Alexander-Bloch AF, Raznahan A,
   Roalf DR, Shinohara RT, Wolf DH, Davatzikos C, Bassett DS, Fair DA,
   Fan Y, Satterthwaite TD. `Individual Variation in Functional
   Topography of Association Networks in
   Youth <https://pubmed.ncbi.nlm.nih.gov/32078800/>`__. **Neuron**.
   2020 Apr 22;106(2):340-353.e8. doi: 10.1016/j.neuron.2020.01.029.
   Epub 2020 Feb 19. PMID: 32078800; PMCID: PMC7182484.
-  Pines AR, Larsen B, Cui Z, Sydnor VJ, Bertolero MA, Adebimpe A,
   Alexander-Bloch AF, Davatzikos C, Fair DA, Gur RC, Gur RE, Li H,
   Milham MP, Moore TM, Murtha K, Parkes L, Thompson-Schill SL,
   Shanmugan S, Shinohara RT, Weinstein SM, Bassett DS, Fan Y,
   Satterthwaite TD. `Dissociable multi-scale patterns of development in
   personalized brain
   networks <https://pubmed.ncbi.nlm.nih.gov/35551181/>`__. **Nat
   Commun**. 2022 May 12;13(1):2647. doi: 10.1038/s41467-022-30244-4.
   PMID: 35551181; PMCID: PMC9098559.
-  Cui Z, Pines AR, Larsen B, Sydnor VJ, Li H, Adebimpe A,
   Alexander-Bloch AF, Bassett DS, Bertolero M, Calkins ME, Davatzikos
   C, Fair DA, Gur RC, Gur RE, Moore TM, Shanmugan S, Shinohara RT,
   Vogel JW, Xia CH, Fan Y, Satterthwaite TD. `Linking Individual
   Differences in Personalized Functional Network Topography to
   Psychopathology in
   Youth <https://pubmed.ncbi.nlm.nih.gov/35927072/>`__. **Biol
   Psychiatry**. 2022 Dec 15;92(12):973-983. doi:
   10.1016/j.biopsych.2022.05.014. Epub 2022 May 18. PMID: 35927072;
   PMCID: PMC10040299.
-  Shanmugan S, Seidlitz J, Cui Z, Adebimpe A, Bassett DS, Bertolero MA,
   Davatzikos C, Fair DA, Gur RE, Gur RC, Larsen B, Li H, Pines A,
   Raznahan A, Roalf DR, Shinohara RT, Vogel J, Wolf DH, Fan Y,
   Alexander-Bloch A, Satterthwaite TD. `Sex differences in the
   functional topography of association networks in
   youth <https://pubmed.ncbi.nlm.nih.gov/35939696/>`__. **Proc Natl
   Acad Sci U S A**. 2022 Aug 16;119(33):e2110416119. doi:
   10.1073/pnas.2110416119. Epub 2022 Aug 8. PMID: 35939696; PMCID:
   PMC9388107.
-  Keller AS, Pines AR, Shanmugan S, Sydnor VJ, Cui Z, Bertolero MA,
   Barzilay R, Alexander-Bloch AF, Byington N, Chen A, Conan GM,
   Davatzikos C, Feczko E, Hendrickson TJ, Houghton A, Larsen B, Li H,
   Miranda-Dominguez O, Roalf DR, Perrone A, Shetty A, Shinohara RT, Fan
   Y, Fair DA, Satterthwaite TD. `Personalized functional brain network
   topography is associated with individual differences in youth
   cognition <https://pubmed.ncbi.nlm.nih.gov/38110396/>`__. **Nat
   Commun**. 2023 Dec 18;14(1):8411. doi: 10.1038/s41467-023-44087-0.
   PMID: 38110396; PMCID: PMC10728159.
-  Zhou Z, Li H, Srinivasan D, Abdulkadir A, Nasrallah IM, Wen J, Doshi
   J, Erus G, Mamourian E, Bryan NR, Wolk DA, Beason-Held L, Resnick SM,
   Satterthwaite TD, Davatzikos C, Shou H, Fan Y; ISTAGING Consortium.
   `Multiscale functional connectivity patterns of the aging brain
   learned from harmonized rsfMRI data of the multi-cohort iSTAGING
   study <https://pubmed.ncbi.nlm.nih.gov/36731813/>`__. **Neuroimage**.
   2023 Apr 1;269:119911. doi: 10.1016/j.neuroimage.2023.119911. Epub
   2023 Jan 30. PMID: 36731813; PMCID: PMC9992322.
-  Li H, Srinivasan D, Zhuo C, Cui Z, Gur RE, Gur RC, Oathes DJ,
   Davatzikos C, Satterthwaite TD, Fan Y. `Computing personalized brain
   functional networks from fMRI using self-supervised deep
   learning <https://pubmed.ncbi.nlm.nih.gov/36706636/>`__. **Med Image
   Anal**. 2023 Apr;85:102756. doi: 10.1016/j.media.2023.102756. Epub
   2023 Jan 21. PMID: 36706636; PMCID: PMC10103143.

Support
-------

If you encounter problems or bugs with pNet, or have questions or
improvement suggestions, please feel free to get in touch via the
`Github issues <https://github.com/MLDataAnalytics/pNet/issues>`__.

Previous versions:
------------------

**Matlab and Python:** https://github.com/MLDataAnalytics/pNet_Matlab

**Matlab:**
https://github.com/MLDataAnalytics/Collaborative_Brain_Decomposition

**GIG-ICA:** https://www.nitrc.org/projects/gig-ica/
