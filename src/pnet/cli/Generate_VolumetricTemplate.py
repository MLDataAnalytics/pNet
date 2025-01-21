import os
import numpy as np
import nibabel as nib
import argparse
from pnet.Module.Data_Input import load_fmri_scan, save_brain_template
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a brain template for computing function networks from volumetric data.')
    parser.add_argument('--mask', type=str, help="""A binary mask NIfTI file with 1 for the foreground and 0 for the background. 
                        The mask file should have the same spatial dimensions as the preprocessed fMRI scans.""")
    parser.add_argument('--overlay', type=str, help="""A NIfTI file serves as the background for displaying the functional networks. 
                        Typically, it is a T1 brain image with high spatial resolution (such as 1mm isotropic) and its spatial 
                        dimensions should be an integer multiple of the spatial dimensions of the preprocessed fMRI scans.""")
    parser.add_argument('--output', type=str, help='An output folder name for the template.')
    
    args = parser.parse_args()
    
    dataType = 'Volume'
    dataFormat = '3D Matrix'
    Brain_Mask, _, _ = load_fmri_scan(args.mask, dataType=dataType, dataFormat='Volume (*.nii, *.nii.gz, *.mat)', Reshape=False, Normalization=None)
    Overlay_Image, _, _ = load_fmri_scan(args.overlay, dataType=dataType, dataFormat='Volume (*.nii, *.nii.gz, *.mat)', Reshape=False, Normalization=None)
    Brain_Mask = (Brain_Mask > 0).astype(np.uint8)
    
    # Check the spatial dimensions of the mask and overlay image 
    # and make sure the overlay image is an integer multiple of the mask image
    if len(Brain_Mask.shape) == 4:
        Brain_Mask = np.squeeze(Brain_Mask, axis=3)
    if len(Overlay_Image.shape) == 4:
        Overlay_Image = np.squeeze(Overlay_Image, axis=3)
    
    upsampling = int(np.round(Overlay_Image.shape[0] / Brain_Mask.shape[0]))
    overlay_shape = tuple(int(dim * upsampling) for dim in Brain_Mask.shape)
    temp = np.zeros(overlay_shape, dtype=np.float32)
    temp[0:Overlay_Image.shape[0], 0:Overlay_Image.shape[1], 0:Overlay_Image.shape[2]] = Overlay_Image.copy()
    overlay_image = temp.copy()
    
    # generate the brain template 
    Brain_Template = {'Data_Type': dataType,
                      'Template_Format': dataFormat,
                      'Brain_Mask': Brain_Mask,
                      'Overlay_Image': overlay_image}
    
    # Create the output folder if it does not exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    save_brain_template(args.output,
                        Brain_Template)
    print(f"There are {np.sum(Brain_Mask)} voxels in the brain")
    