# CUDA 和 PyTorch 安装指南

本项目包含一个自动化安装脚本，可以检测您系统上的CUDA版本并安装与之兼容的PyTorch版本。

## 使用方法

### 自动安装（推荐）

直接运行安装脚本，它会自动检测CUDA版本并安装合适的PyTorch版本：

```bash
python install_dependencies.py
```

### 指定CUDA版本

如果您想强制使用特定的CUDA版本，可以使用以下命令：

```bash
python install_dependencies.py --force-cuda 12.7
```

### 无GPU环境

如果您的系统没有NVIDIA GPU或没有安装CUDA，脚本会自动安装CPU版本的PyTorch。

## CUDA 与 PyTorch 版本对应关系

下表显示了不同CUDA版本和PyTorch版本的兼容性及其发布时间：

| CUDA版本 | 兼容的PyTorch版本 | CUDA发布时间 | PyTorch发布时间 |
|---------|----------------|------------|---------------|
| CUDA 12.8 | 2.6.0+cu126 | 2024年7月 | 2024年6月 |
| CUDA 12.7 | 2.6.0+cu126 | 2024年5月 | 2024年6月 |
| CUDA 12.6 | 2.6.0+cu126 | 2024年3月 | 2024年6月 |
| CUDA 12.5 | 2.6.0+cu121 | 2024年1月 | 2024年6月 |
| CUDA 12.4 | 2.6.0+cu121 | 2023年11月 | 2024年6月 |
| CUDA 12.3 | 2.6.0+cu121 | 2023年10月 | 2024年6月 |
| CUDA 12.2 | 2.6.0+cu121 | 2023年8月 | 2024年6月 |
| CUDA 12.1 | 2.6.0+cu121 | 2023年6月 | 2024年6月 |
| CUDA 12.0 | 2.1.0+cu121 | 2023年3月 | 2023年10月 |
| CUDA 11.8 | 2.2.0+cu118 | 2022年11月 | 2024年1月 |
| CUDA 11.7 | 2.0.0+cu117 | 2022年6月 | 2023年3月 |
| CUDA 11.6 | 1.13.1+cu116 | 2022年1月 | 2022年12月 |
| CUDA 11.5 | 1.12.1+cu115 | 2021年10月 | 2022年8月 |
| CUDA 11.4 | 1.12.1+cu113 | 2021年7月 | 2022年8月 |
| CUDA 11.3 | 1.12.1+cu113 | 2021年4月 | 2022年8月 |
| CUDA 11.2 | 1.10.2+cu113 | 2020年12月 | 2021年10月 |
| CUDA 11.1 | 1.10.2+cu111 | 2020年11月 | 2021年10月 |
| CUDA 11.0 | 1.9.1+cu111 | 2020年7月 | 2021年8月 |
| CUDA 10.2 | 1.12.1+cu102 | 2019年11月 | 2022年8月 |
| CUDA 10.1 | 1.7.1+cu101 | 2019年2月 | 2020年11月 |
| CUDA 10.0 | 1.6.0+cu100 | 2018年9月 | 2020年7月 |
| CUDA 9.2 | 1.5.1+cu92 | 2018年5月 | 2020年4月 |
| CUDA 9.0 | 1.1.0 | 2017年9月 | 2019年5月 |

## 故障排除

如果安装过程中遇到问题，您可以尝试以下步骤：

1. **检查CUDA是否正确安装**：
   ```bash
   nvidia-smi
   ```

2. **手动卸载并重新安装PyTorch**：
   ```bash
   pip uninstall -y torch torchvision torchaudio
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
   ```

3. **验证PyTorch安装**：
   ```python
   import torch
   print(torch.__version__)
   print(torch.cuda.is_available())
   ```

## 注意事项

- 较新版本的CUDA通常可以运行为较旧版本CUDA编译的PyTorch
- 反之则不行：旧版本的CUDA通常无法运行为新版本CUDA编译的PyTorch
- 如果您更新了NVIDIA驱动或CUDA，建议重新运行安装脚本 