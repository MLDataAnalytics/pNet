import os
import torch

import numpy as np
import nibabel as nib

from config_fn_hier_lv3 import *
from model_hier_lv3 import Model
from fmri_dataset import fmriDataset



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if __name__ == '__main__':
    with torch.no_grad():
        config = eval_config()

        if not os.path.exists(config.output_dir):
            os.makedirs(config.output_dir)

        fmri_ds = fmriDataset(config.nii_lst, config.im_mask, config.im_size, 
                              config.im_preproc, config.im_s, config.im_e)
        testloader = torch.utils.data.DataLoader(fmri_ds,
                                                 batch_size=config.batch_size,
                                                 shuffle=False,
                                                 num_workers=1)
        len_dataset = len(testloader.dataset)

        model = Model(k_networks=config.n_functional_networks,
                      c_features=config.n_time_invariant_features,
                      im_sz=config.im_size,
                      T=config.T)
        model.load_state_dict(torch.load(config.weights_file, map_location=device))
        model = model.to(device)
        model.eval()

        for i, i_batch in enumerate(testloader, 0):
            batch_dat = torch.squeeze(i_batch[0], 1)
            batch_lst = i_batch[1][0]
            batch_idx = i_batch[2][0]

            print("{:04d}. ".format(batch_idx[0]+1) + batch_lst[0]) # for batch_size=1

            X = batch_dat.float().to(device)
            Y, Wt = model(X)

            # masked Y
            if fmri_ds.mask_cropped is not None:
                mask = torch.from_numpy(np.transpose(fmri_ds.mask_cropped, (0,4,1,2,3)))

                mask_d = torch.amax(torch.abs(X), 1, True) > config.mask_val
                mask = mask.float().to(device) * mask_d.float().to(device)
            else:
                mask = torch.amax(torch.abs(X), 1, True) > config.mask_val
            Y = [Yi * mask.float().to(device) for Yi in Y]

            for li in range(len(Y)):
                Y_np = Y[li].cpu().detach().numpy()
                Y_np = np.transpose(Y_np, (0,2,3,4,1))
                for bi in range(Y_np.shape[0]):
                    bi_nii = nib.load(batch_lst[bi])
                    bi_hdr = bi_nii.header
                    nii = nib.Nifti1Image(Y_np[bi,:,:,:,:], bi_hdr.get_best_affine(), bi_hdr)
                    nib.save(nii, config.output_dir+"/{:04d}_fn_l{:d}_4d.nii.gz".format(config.batch_size*i+bi+1, li+1))

            for li in range(len(Wt)):
                wt_np = Wt[li].cpu().detach().numpy()
                # assume the batch size is 1
                np.save(config.output_dir+"/{:04d}_hier_wt_l{:d}to{:d}.npy".format(config.batch_size*i+bi+1, li+1, li+2), wt_np)

        print("Finished.")
