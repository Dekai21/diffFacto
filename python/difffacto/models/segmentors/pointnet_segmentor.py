import torch
from torch import nn
import torch.nn.functional as F
from difffacto.utils.registry import ENCODERS, build_from_cfg, SEGMENTORS

@SEGMENTORS.register_module()
class PointNetDenseCls(nn.Module):
    def __init__(self, n_class = 2):
        super(PointNetDenseCls, self).__init__()
        self.k = n_class
        self.feat = build_from_cfg(dict(type="PointNet", global_feat=False, latent_dim=1024), ENCODERS)
        self.conv1 = torch.nn.Conv1d(1088, 512, 1)
        self.conv2 = torch.nn.Conv1d(512, 256, 1)
        self.conv3 = torch.nn.Conv1d(256, 128, 1)
        self.conv4 = torch.nn.Conv1d(128, self.k, 1)
        self.bn1 = nn.BatchNorm1d(512)
        self.bn2 = nn.BatchNorm1d(256)
        self.bn3 = nn.BatchNorm1d(128)

    def forward(self, x):
        batchsize = x.size()[0]
        n_pts = x.size()[1]
        x  = self.feat(x.transpose(1,2))
        global_feat = x
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = self.conv4(x)
        x = x.transpose(2,1).contiguous()
        x = F.log_softmax(x.view(-1,self.k), dim=-1)
        x = x.view(batchsize, n_pts, self.k)
        return x, global_feat