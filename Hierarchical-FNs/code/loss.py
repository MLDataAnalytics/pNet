import torch


def train_loss(mri, fns, eps=1e-8):
    spatial_mass = torch.sum(fns, dim=(2, 3, 4))
    spatial_density = torch.einsum('nkxyz, nk -> nkxyz', fns, 1.0 / (spatial_mass + eps))
    TC = torch.einsum('ntxyz, nkxyz -> ntk', mri, spatial_density)
    X_recon = torch.einsum('ntk, nkxyz -> ntxyz', TC, fns)

    recon_error = torch.square(X_recon - mri)
    recon_loss = torch.sum(recon_error)
    return recon_loss


def negentropy_loss(fns, eps=1e-8):
    fn_mass = torch.sum(fns, dim=(2, 3, 4))
    fn_mass = fn_mass / torch.sum(fn_mass, dim=1, keepdim=True) + eps
    ne_loss = torch.sum(fn_mass*torch.log(fn_mass))

    return ne_loss
