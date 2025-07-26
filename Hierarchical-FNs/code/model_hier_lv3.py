import torch
import torch.nn as nn
import torch.nn.functional as F

import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.autograd.set_detect_anomaly(True)


class FeatureExtractor(nn.Module):
    def __init__(self, c_features, eps=1e-9):
        super().__init__()
        self.eps = eps
        self.conv = nn.Conv3d(1, c_features, kernel_size=3, stride=1, padding=1, bias=False)
        self.norm = nn.InstanceNorm3d(c_features, affine=True)

        nn.init.trunc_normal_(self.conv.weight, std=0.01, a=-0.02, b=0.02)

    def forward(self, X):
        # Temporally separated convolution
        X = F.leaky_relu(torch.stack([
            self.conv(X[:, i, None, :, :, :])
            for i in range(X.shape[1])
        ], 0))

        # Average pooling along temporal axis
        X = torch.mean(X, 0)
        X = self.norm(X)

        return X


class UNet(nn.Module):
    def __init__(self, c_features, eps=1e-9):
        super().__init__()
        self.eps = eps

        self.conv1 = nn.Conv3d(c_features, 16, kernel_size=3, stride=1, padding=1, bias=False)
        self.conv2 = nn.Conv3d(16, 32, kernel_size=3, stride=2, padding=1, bias=False)
        self.conv3 = nn.Conv3d(32, 32, kernel_size=3, stride=2, padding=1, bias=False)
        self.conv4 = nn.Conv3d(32, 32, kernel_size=3, stride=2, padding=1, bias=False)
        self.deconv5 = nn.Conv3d(32, 32, kernel_size=3, stride=1, padding=1, bias=False)
        self.deconv6 = nn.Conv3d(64, 32, kernel_size=3, stride=1, padding=1, bias=False)
        self.deconv7 = nn.Conv3d(64, 16, kernel_size=3, stride=1, padding=1, bias=False)
        self.conv8 = nn.Conv3d(32, 16, kernel_size=3, stride=1, padding=1, bias=False)
        self.conv9 = nn.Conv3d(16, 16, kernel_size=3, stride=1, padding=1, bias=False)

        nn.init.trunc_normal_(self.conv1.weight, std=0.01, a=-0.02, b=0.02)
        nn.init.trunc_normal_(self.conv2.weight, std=0.01, a=-0.02, b=0.02)
        nn.init.trunc_normal_(self.conv3.weight, std=0.01, a=-0.02, b=0.02)
        nn.init.trunc_normal_(self.conv4.weight, std=0.01, a=-0.02, b=0.02)
        nn.init.trunc_normal_(self.deconv5.weight, std=0.01, a=-0.02, b=0.02)
        nn.init.trunc_normal_(self.deconv6.weight, std=0.01, a=-0.02, b=0.02)
        nn.init.trunc_normal_(self.deconv7.weight, std=0.01, a=-0.02, b=0.02)
        nn.init.trunc_normal_(self.conv8.weight, std=0.01, a=-0.02, b=0.02)
        nn.init.trunc_normal_(self.conv9.weight, std=0.01, a=-0.02, b=0.02)

        self.norm1 = nn.InstanceNorm3d(16, affine=True)
        self.norm2 = nn.InstanceNorm3d(32, affine=True)
        self.norm3 = nn.InstanceNorm3d(32, affine=True)
        self.norm4 = nn.InstanceNorm3d(32, affine=True)
        self.norm5 = nn.InstanceNorm3d(32, affine=True)
        self.norm6 = nn.InstanceNorm3d(32, affine=True)
        self.norm7 = nn.InstanceNorm3d(16, affine=True)
        self.norm8 = nn.InstanceNorm3d(16, affine=True)
        self.norm9 = nn.InstanceNorm3d(16, affine=True)

    def forward(self, X):
        X1 = self.norm1(F.leaky_relu(self.conv1(X), negative_slope=0.01))
        X2 = self.norm2(F.leaky_relu(self.conv2(X1), negative_slope=0.01))
        X3 = self.norm3(F.leaky_relu(self.conv3(X2), negative_slope=0.01))
        X4 = self.norm4(F.leaky_relu(self.conv4(X3), negative_slope=0.01))
        X5 = self.norm5(F.leaky_relu(self.deconv5(X4), negative_slope=0.01))
        X5 = torch.cat([F.interpolate(X5, X3.shape[2:5]), X3], 1)
        X6 = self.norm6(F.leaky_relu(self.deconv6(X5), negative_slope=0.01))
        X6 = torch.cat([F.interpolate(X6, X2.shape[2:5]), X2], 1)
        X7 = self.norm7(F.leaky_relu(self.deconv7(X6), negative_slope=0.01))
        X7 = torch.cat([F.interpolate(X7, X1.shape[2:5]), X1], 1)
        X8 = self.norm8(F.leaky_relu(self.conv8(X7), negative_slope=0.01))
        X9 = self.norm9(F.leaky_relu(self.conv9(X8), negative_slope=0.01))
        return X9, X4


class Output_softmax(nn.Module):
    def __init__(self, k_networks, T=1, eps=1e-9):
        super().__init__()
        self.eps = eps
        self.T = T
        self.conv1 = nn.Conv3d(16, k_networks[0], kernel_size=3, stride=1, padding=1)
        nn.init.trunc_normal_(self.conv1.weight, std=0.01, a=-0.02, b=0.02)

    def forward(self, X):
        X1 = F.softmax(self.conv1(X)/self.T, dim=1)
        return X1


class Hier_pred(nn.Module):
    def __init__(self, k_networks, hp_dim=441, T=1, eps=1e-9):      # 441: spatial dimension of the btnk feature maps for input fMRI with a size of [56, 72, 56]
        super().__init__()
        self.eps = eps
        self.k_networks = k_networks
        self.T = T

        self.conv1_1 = nn.Conv3d(32, k_networks[0], kernel_size=3, stride=1, padding=1)
        nn.init.trunc_normal_(self.conv1_1.weight, std=0.01, a=-0.02, b=0.02)
        self.conv1_2 = nn.Conv3d(k_networks[0], k_networks[0], kernel_size=3, stride=1, padding=1)
        nn.init.trunc_normal_(self.conv1_2.weight, std=0.01, a=-0.02, b=0.02)
        self.fc1_1 = nn.Linear(hp_dim, 64)
        self.fc1_2 = nn.Linear(64, 64)
        self.fc1_3 = nn.Linear(64, k_networks[1])
        self.norm1_1 = nn.InstanceNorm3d(k_networks[0], affine=True)
        self.norm1_2 = nn.InstanceNorm3d(k_networks[0], affine=True)

        self.conv2_1 = nn.Conv3d(32, k_networks[1], kernel_size=3, stride=1, padding=1)
        nn.init.trunc_normal_(self.conv2_1.weight, std=0.01, a=-0.02, b=0.02)
        self.conv2_2 = nn.Conv3d(k_networks[1], k_networks[1], kernel_size=3, stride=1, padding=1)
        nn.init.trunc_normal_(self.conv2_2.weight, std=0.01, a=-0.02, b=0.02)
        self.fc2_1 = nn.Linear(hp_dim, 64)
        self.fc2_2 = nn.Linear(64, 64)
        self.fc2_3 = nn.Linear(64, k_networks[2])
        self.norm2_1 = nn.InstanceNorm3d(k_networks[1], affine=True)
        self.norm2_2 = nn.InstanceNorm3d(k_networks[1], affine=True)

    def forward(self, X):
        fea1 = self.norm1_1(F.leaky_relu(self.conv1_1(X), negative_slope=0.01))
        fea1 = self.norm1_2(F.leaky_relu(self.conv1_2(fea1), negative_slope=0.01))
        fea_tr1 = torch.permute(fea1, (1,0,2,3,4))
        fea_rs1 = torch.reshape(fea_tr1, (self.k_networks[0],-1))
        fn_wt1 = F.leaky_relu(self.fc1_1(fea_rs1), negative_slope=0.01)
        fn_wt1 = F.leaky_relu(self.fc1_2(fn_wt1), negative_slope=0.01)
        fn_wt1 = F.softmax(self.fc1_3(fn_wt1)/self.T, dim=1)

        fea2 = self.norm2_1(F.leaky_relu(self.conv2_1(X), negative_slope=0.01))
        fea2 = self.norm2_2(F.leaky_relu(self.conv2_2(fea2), negative_slope=0.01))
        fea_tr2 = torch.permute(fea2, (1,0,2,3,4))
        fea_rs2 = torch.reshape(fea_tr2, (self.k_networks[1],-1))
        fn_wt2 = F.leaky_relu(self.fc2_1(fea_rs2), negative_slope=0.01)
        fn_wt2 = F.leaky_relu(self.fc2_2(fn_wt2), negative_slope=0.01)
        fn_wt2 = F.softmax(self.fc2_3(fn_wt2)/self.T, dim=1)

        return fn_wt1, fn_wt2


# maps a N x T x D x H x W tensor --> N x K1 x D x H x W tensor, N x K2 x D x H x W tensor, ...
class Model(nn.Module):
    def __init__(self, k_networks=[148, 40, 20], c_features=16, im_sz=[56, 72, 56], T=1, eps=1e-9):
        super().__init__()

        self.eps = eps
        self.T = T

        self.feature_extractor = FeatureExtractor(c_features)
        self.unet = UNet(c_features)
        self.output = Output_softmax(k_networks, self.T)

        hp_dim = np.int32(np.prod(im_sz) / pow(pow(2,3),3))
        self.out_wt = Hier_pred(k_networks, hp_dim, self.T)

    def forward(self, x):
        x = self.feature_extractor(x)
        x_fea, x_btnk = self.unet(x)
        y1 = self.output(x_fea)
        
        w = self.out_wt(x_btnk)
        
        wt12 = torch.unsqueeze(w[0], dim=0)
        y2 = torch.einsum('nfxyz, nfc -> ncxyz', y1, wt12) 
        y2_vsum = torch.sum(y2, dim=1, keepdim=True)
        y2 = y2 / (y2_vsum + self.eps)
        
        wt23 = torch.unsqueeze(w[1], dim=0)
        y3 = torch.einsum('nfxyz, nfc -> ncxyz', y2, wt23)
        y3_vsum = torch.sum(y3, dim=1, keepdim=True)
        y3 = y3 / (y3_vsum + self.eps)

        return [y1, y2, y3], w
