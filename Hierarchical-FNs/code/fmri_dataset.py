import os
import os.path

import numpy as np
import nibabel as nib

import torch
from torch.utils.data import Dataset



class fmriDataset(Dataset):
    def __init__(self, img_lst, mask_name, img_size=None, preproc='vn', img_s=None, img_e=None):
        self.img_lst = []
        with open(img_lst, 'r') as f:
            for line in f:
                self.img_lst.append(line.strip())

        if mask_name is not None:
            self.mask = self._get_mask(mask_name)
        else:
            self.mask = None

        self.mask_cropped = None
        if self.mask is not None:
            if (img_size is not None) and (self.mask.shape[1:-1] != tuple(img_size)):
                if (img_s is not None) and (img_e is not None):
                        self.mask_cropped = self.mask[:,img_s[0]:img_e[0],img_s[1]:img_e[1],img_s[2]:img_e[2],:]

        self.img_size = img_size
        self.preproc = preproc
        self.img_s = img_s
        self.img_e = img_e

    def __len__(self):
        return len(self.img_lst)

    def __getitem__(self, idx):
        if isinstance(idx, int):
            idx = [idx]
        sel_img_lst = [self.img_lst[a] for a in idx]
        sel_img, sel_hdr, sel_l = self._get_data(sel_img_lst)

        x = np.concatenate(sel_img, 0)
        x = np.transpose(x, (0,4,1,2,3))
        return x, sel_l, idx

    def _get_data(self, img_lst):
        img_size = self.img_size
        mask = self.mask[0]
        preproc = self.preproc
        img_s = self.img_s
        img_e = self.img_e

        data = []
        header = []
        lst = []
        for i in range(len(img_lst)):
            #print("  "+str(i+1)+". "+img_lst[i])
            i_img = nib.load(img_lst[i])
            img_data = i_img.get_fdata()
            img_data = img_data.astype(np.float32)

            if (img_size is not None) and (img_data.shape[0:-1] != tuple(img_size)):
                if (img_s is not None) and (img_e is not None):
                    img_data = img_data[img_s[0]:img_e[0],img_s[1]:img_e[1],img_s[2]:img_e[2],:]
                    if mask is not None:
                        mask = mask[img_s[0]:img_e[0],img_s[1]:img_e[1],img_s[2]:img_e[2],:]

            if mask is not None:
                img_data = img_data * mask

            data_shape = img_data.shape
            img_data_mat = np.reshape(img_data, (-1,data_shape[-1]))
            if mask is not None:
                mask_vec = np.reshape(mask, (-1,)) > 0
                sel_data_mat = img_data_mat[mask_vec,:]
            else:
                sel_data_mat = img_data_mat.copy()

            ## data normalization
            if preproc=='gs':
                ## global normalization
                data_mask = sel_data_mat!=0
                tmp_img_data = sel_data_mat[data_mask]
                m_img = np.mean(tmp_img_data)
                s_img = np.std(tmp_img_data)
                tmp_img_data = (tmp_img_data-m_img) / (s_img + 1e-6)
                sel_data_mat[data_mask] = tmp_img_data
                sel_data_mat[np.bitwise_not(data_mask)] = 0
            elif preproc=='vn':
                ## voxel-wise normalization
                m_img = np.mean(sel_data_mat, axis=1, keepdims=True)
                s_img = np.std(sel_data_mat, axis=1, keepdims=True)
                sel_data_mat = (sel_data_mat-m_img) / (s_img + 1e-6)
            elif preproc=='tn':
                ## time-point wise normalization
                m_img = np.mean(sel_data_mat, axis=0, keepdims=True)
                s_img = np.std(sel_data_mat, axis=0, keepdims=True)
                sel_data_mat = (sel_data_mat-m_img) / (s_img + 1e-6)
            elif preproc=='nn':
                max_img = np.amax(sel_data_mat, axis=1, keepdims=True)
                min_img = np.amin(sel_data_mat, axis=1, keepdims=True)
                sel_data_mat = (sel_data_mat-min_img) / (max_img-min_img+1e-6)
            else:
                ## no data preprocessing
                pass

            if mask is not None:
                img_data_mat[mask_vec,:] = sel_data_mat
            else:
                img_data_mat = sel_data_mat
            img_data = np.reshape(img_data_mat, data_shape)
            img_data = np.expand_dims(img_data, 0)

            data.append(img_data)
            header.append(i_img.header)
            #lst.append(os.path.basename(img_lst[i]))
            lst.append(img_lst[i])

        return data, header, lst

    def _get_mask(self, mask_name):
        i_mask = nib.load(mask_name)
        mask_shape = list(i_mask.shape)
        mask_data = i_mask.get_fdata()
        mask_data[mask_data>0] = 1
        mask_data = mask_data.astype(np.float32)

        data_sz = [1] + mask_shape + [1]
        mask = np.empty(data_sz, dtype=np.float32)
        mask[0] = np.expand_dims(mask_data, 3)

        return mask
