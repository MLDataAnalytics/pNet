import os
import torch
import torch.nn as nn

import numpy as np
import nibabel as nib

from config_fn_hier_lv3 import *
from model_hier_lv3 import Model
from loss import train_loss, negentropy_loss
from fmri_dataset import fmriDataset



device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
torch.autograd.set_detect_anomaly(True)

if __name__ == '__main__':
    config = train_config()
    print('Configuration: ', config.mode)

    if not os.path.exists(config.output_dir):
        os.makedirs(config.output_dir)
    if not os.path.exists(config.tmp_dir):
        os.makedirs(config.tmp_dir)

    fmri_ds = fmriDataset(config.nii_lst, config.im_mask, config.im_size, 
                          config.im_preproc, config.im_s, config.im_e)
    trainloader = torch.utils.data.DataLoader(fmri_ds,
                                              batch_size=config.batch_size,
                                              shuffle=True,
                                              num_workers=1)
    len_dataset = len(trainloader.dataset)

    model = Model(k_networks=config.n_functional_networks,
                  c_features=config.n_time_invariant_features,
                  im_sz=config.im_size)

    if config.start_weights_file is not None:
        model.load_state_dict(torch.load(config.start_weights_file))
        print('Continue training, start with: ', config.start_weights_file)        

    model = model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), config.lr)

    for epoch in range(config.n_epochs):
        running_loss = 0.0
        r_df_loss = 0.0
        r_ne_loss = 0.0

        for i, i_batch in enumerate(trainloader, 0):
            batch_dat = torch.squeeze(i_batch[0], 1)
            batch_lst = i_batch[1][0]
            batch_idx = i_batch[2][0]

            # get data_y (for computing loss)
            t_num_tot = batch_dat.shape[1]
            if t_num_tot <= config.num_t:
                data_y = batch_dat
                config.num_t = t_num_tot
            else:
                ii_step = np.int32(np.floor(t_num_tot/config.num_t))
                max_st_ii = t_num_tot - config.num_t * ii_step
                st_ii = np.random.choice(max_st_ii)
                sel_tp_ii = np.arange(st_ii, t_num_tot, ii_step)
                sel_tp_ii = sel_tp_ii[:config.num_t]
                data_y = batch_dat[:,sel_tp_ii,:,:,:]

            # get data (as input to the network)
            t_step = np.int32(np.floor(config.num_t/config.t_sample_num))
            max_st_t = config.num_t - t_step * config.t_sample_num
            st_t = np.random.choice(max_st_t)
            sel_tp = np.arange(st_t, config.num_t, t_step)
            sel_tp = sel_tp[:config.t_sample_num]
            data = data_y[:,sel_tp,:,:,:]

            X = data.float().to(device)
            X_y = data_y.float().to(device)

            optimizer.zero_grad()
            Y, Wt = model(X)
            # masked Y
            if fmri_ds.mask_cropped is not None:
                mask = torch.from_numpy(np.transpose(fmri_ds.mask_cropped, (0,4,1,2,3))) 
            else:
                mask = torch.amax(torch.abs(X_y), 1, True) > config.mask_val
            nz_num = torch.sum(mask).float().to(device)
            Y = [Yi * mask.float().to(device) for Yi in Y]

            #
            df_loss = []
            for li in range(len(Y)):
                df_loss_li = train_loss(mri=X_y, fns=Y[li]) / nz_num 
                df_loss.append(torch.unsqueeze(df_loss_li,0))
            df_loss = torch.sum(torch.cat(df_loss)) 

            if config.ne_lv == 'all':
                # ne_loss v2, at all scales
                ne_loss = []
                for li in range(len(Y)):
                    ne_loss_li = negentropy_loss(fns=Y[li]) * config.ne_reg / np.log(config.n_functional_networks[li])    # config.n_functional_networks[li]
                    ne_loss.append(torch.unsqueeze(ne_loss_li,0))
                ne_loss = torch.sum(torch.cat(ne_loss))
            else:
                # ne_loss v1, only at fineset scale
                ne_loss = negentropy_loss(fns=Y[0]) * config.ne_reg / config.n_functional_networks[0]

            loss = df_loss + ne_loss

            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

            optimizer.step()

            running_loss += loss.item()
            r_df_loss += df_loss.item()
            r_ne_loss += ne_loss.item()
            if (i+1) % min(5, len_dataset-1) == 0:
                print(f'[epoch {epoch + 1}, iter {i + 1:5d}] loss: {running_loss/(i+1):.3f}, data_fitting: {r_df_loss/(i+1):.3f}, neg_entropy: {r_ne_loss/(i+1):.3f}')

            if i>0 and i % min(100, len_dataset-1) == 0:
                for li in range(len(Y)):
                    Y_np = Y[li].cpu().detach().numpy()
                    Y_np = np.transpose(Y_np, (0,2,3,4,1))
                    for bi in range(Y_np.shape[0]):
                        bi_nii = nib.load(batch_lst[bi])
                        bi_hdr = bi_nii.header
                        nii = nib.Nifti1Image(Y_np[bi,:,:,:,:], bi_hdr.get_best_affine(), bi_hdr)
                        nib.save(nii, config.tmp_dir+"/{:02d}_fn_l{:d}_4d.nii.gz".format(bi+1, li+1))

                for li in range(len(Wt)):
                    wt_np = Wt[li].cpu().detach().numpy()
                    np.save(config.tmp_dir+"/{:02d}_hier_wt_l{:d}to{:d}.npy".format(1, li+1, li+2), wt_np)  # assume the batch size is 1

        if epoch % config.checkpoint_interval == 0:
            torch.save(model.state_dict(), config.output_dir
                       + 'weights_{}.pth'.format(epoch))

    torch.save(model.state_dict(), config.output_dir
               + 'weights_{}.pth'.format(config.n_epochs))

