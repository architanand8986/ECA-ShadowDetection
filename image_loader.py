import glob
import os
from PIL import Image
import torch.utils.data as data
resnext_101_32_path = 'resnext_101_32x4d.pth'
training_root = '/kaggle/input/istd-dataset/ISTD_Dataset'

def make_dataset(root):
    img_list = [os.path.splitext(f)[0] for f in os.listdir(os.path.join(root, 'image')) if f.endswith('.png')]
    return [
        (os.path.join(root, 'image', img_name + '.png'), os.path.join(root, 'label', img_name + '.png'))
        for img_name in img_list]


class ImageFolder(data.Dataset):
    def __init__(self, root, joint_transform=None, transform=None, target_transform=None):
        self.root = root
        self.imgs = make_dataset(root)
        self.joint_transform = joint_transform
        self.transform = transform
        self.target_transform = target_transform

    def __getitem__(self, index):
        img_path, gt_path = self.imgs[index]
        img = Image.open(img_path).convert('RGB')
        target = Image.open(gt_path)

        img, target = self.joint_transform(img, target)
        img = self.transform(img)
        target = self.target_transform(target)

        return img, target

    def __len__(self):
        return len(self.imgs)
