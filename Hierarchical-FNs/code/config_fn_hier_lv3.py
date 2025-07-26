class Config:
    pass


def train_config():                         # parameter configuration for training
    config = Config()
    config.mode = 'train'

    # training parameters
    config.n_epochs = 100                   # number of training epochs
    config.batch_size = 1                   # batch size
    config.lr = 1e-4                        # learning rate
    config.ne_reg = 50                      # trade-off hyperparameter in the loss function
    config.ne_lv = 'all'

    config.im_size = [56, 72, 56]           # image size of input fMRI data after cropping
    config.im_s = [2, 0, 2]                 # start location used to crop image (for saving GPU memory)
    config.im_e = [58, 72, 58]              # end location used to crop image
    
    config.num_t = 120                      # number of time points of fMRI data used during training to compute loss function 
                                            # in each iteration. can be changed according to available GPU memory, 
                                            # larger num_t consumes more memory
    
    config.t_sample_num = 50                # number of time points of fMRI data used during training to compute time-invariant
                                            # feature representation in each iteration. can be changed according to available 
                                            # GPU memory, larger t_sample_num (<=num_t) consumes more memory
    config.mask_val = 0
    config.im_preproc = 'vn'                # intensity normalization for input fMRI

    # list (.txt) file of training fMRI data, each row corresponds to the preprocessed fMRI of each individual
    config.nii_lst = r'/cbica/home/lihon/code_share/for_manuscripts/ssdl_hier_fn/example_data/tes_fmri_lst.txt'
    # grey matter (cerebral cortex) mask image
    config.im_mask = r'/cbica/home/lihon/code_share/for_manuscripts/ssdl_hier_fn/example_data/mask_gm_cc_3mm.nii.gz'

    # model parameters
    config.n_time_invariant_features = 16           # dimension of the time-invariant feature representation
    config.n_functional_networks = [148, 50, 17]    # number of FNs to be identified from fine to coarse scales

    # output path of the trained model and temporary results
    out_dir_base = '/cbica/home/lihon/code_share/for_manuscripts/ssdl_hier_fn/output/'
    out_prefix = out_dir_base + 'lr{}_k{}_{}_{}_c{}_ne{}'.format(config.lr,
                                                                 config.n_functional_networks[0], config.n_functional_networks[1], config.n_functional_networks[2],
                                                                 config.n_time_invariant_features,
                                                                 config.ne_reg) + config.ne_lv
    # where trained model will be saved
    config.output_dir = out_prefix + '_model/'
    # where temporary results during training will be saved
    config.tmp_dir = out_prefix + '_tmp/'

    # start/resume training from an existing model (if available)
    config.output_dir_start = out_prefix +  '_model/'
    config.start_weights_file = None

    # save model every 10 epochs
    config.checkpoint_interval = 10

    return config


def eval_config():                          # parameter configuration for testing
    config = Config()
    config.mode = 'eval'

    # testing parameters
    config.batch_size = 1

    # model parameters
    config.n_time_invariant_features = 16
    config.n_functional_networks = [148, 50, 17]
    config.T = 2

    config.im_size = [56, 72, 56]
    config.im_s = [2, 0, 2]
    config.im_e = [58, 72, 58]
    config.mask_val = 0
    config.im_preproc = 'vn'

    # list (.txt) file of the testing fMRI data, each row corresponds to the preprocessed fMRI of each individual
    config.nii_lst = r'/cbica/home/lihon/code_share/for_manuscripts/ssdl_hier_fn/example_data/tes_fmri_lst.txt'
    # grey matter (cerebral cortex) mask image
    config.im_mask = r'/cbica/home/lihon/code_share/for_manuscripts/ssdl_hier_fn/example_data/mask_gm_cc_3mm.nii.gz'

    # path to the trained model
    config.weights_file = '/cbica/home/lihon/code_share/for_manuscripts/ssdl_hier_fn/model/weights_100.pth'

    # where the output results will be saved
    config.output_dir = r'/cbica/home/lihon/code_share/for_manuscripts/ssdl_hier_fn/output/testing_res/'

    return config

