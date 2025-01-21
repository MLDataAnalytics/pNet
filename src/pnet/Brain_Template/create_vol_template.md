# Generating a Brain Template for Computing Functional Networks from Volumetric fMRI Data

This example demonstrates creating a brain template based on the MNI152 template, commonly used for preprocessing fMRI data (e.g., in the fMRIPrep pipeline).

## Steps:

### 1 - Download the MNI152 template: Obtain the template from the TemplateFlow website or the MNI website.

### 2 - Segment the MNI152 template: Use FreeSurfer (or a comparable tool) to segment the MNI152 T1/T2 images, generating masks for gray matter tissue.

### 3 - Map FreeSurfer segmentations to the original MNI152 space: Use mri_vol2vol and mri_label2vol (from FreeSurfer) to map the segmentation results back to the original MNI152 image space.

#### For Images (e.g., brain.mgz):
   ```bash
   cd $SUBJECTS_DIR/<subjid>/mri
   mri_vol2vol --mov brain.mgz --targ rawavg.mgz --regheader --o brain-in-rawavg.nii.gz --no-save-reg
   ```
   - `rawavg.mgz` is in the native space of your anatomical image, so it is used as the target space.
   - The output `brain-in-rawavg.mgz` will be in the native space.

#### For Segmentations (e.g., aseg.mgz):
   ```bash
   cd $SUBJECTS_DIR/<subjid>/mri
   mri_label2vol --seg ribbon.mgz --temp rawavg.mgz --o ribbon-in-rawavg.nii.gz --regheader ribbon.mgz
   ```
   - This command maps the segmentation to the native space.

#### For Surfaces:
   - First, create a registration matrix:
     ```bash
     tkregister2 --mov rawavg.mgz --targ orig.mgz --reg register.native.dat --noedit --regheader
     ```
   - Then, map the surface to the native space:
     ```bash
     mri_surf2surf --sval-xyz pial --reg register.native.dat rawavg.mgz --tval lh.pial.native --tval-xyz rawavg.mgz --hemi lh --s subjectname
     ```
### 4 - Generate a ribbon mask -- others can be generated in the same way
   ```bash
    fslmaths ribbon-in-rawavg.nii.gz -thr 41.5 -bin tmp1.nii.gz         # left cortex
    fslmaths ribbon-in-rawavg.nii.gz -thr 2.5 -uthr 3.5 -bin tmp2.nii.gz    # right cortex
    fslmaths tmp1.nii.gz -add tmp2.nii.gz -bin ribbon-in-rawavg-bin.nii.gz  # combine left and right cortex
    ResampleImage 3 ribbon-in-rawavg-bin.nii.gz ribbon-in-rawavg-bin-2mm.nii.gz 2x2x2 size=1,spacing=0 1 char  # resample to 2mm
   ```
- fslmaths and ResampleImage are tools from FSL and ANTs, respectively.
### 5 - Generate a brain template
   ```bash
   cd /cbica/home/fanyo/pNet/src/pnet/cli
   python Generate_VolumetricTemplate.py 
      --mask /cbica/home/fanyo/MNI_ICBM/mni_icbm152_nlin_asym_09c_freesurf/mni_icbm152_tal_nlin_asym_09c/mri/ribbon-in-rawavg-bin-2mm.nii.gz 
      --overlay /cbica/home/fanyo/MNI_ICBM/mni_icbm152_nlin_asym_09c/mni_icbm152_t1_tal_nlin_asym_09c.nii.gz 
      --output ./
   ```
- This command generates a brain template for computing personalized FNs. You must **modify** the directory paths to correspond to your data organization.
