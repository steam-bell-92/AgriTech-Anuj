# Plant Disease Detection

This project provides resources for detecting plant diseases using deep learning models. It includes pre-trained PyTorch models, test images for evaluation, and example result screenshots.

## Contents

- `plant-disease-model.pth` & `plant-disease-model-complete.pth`: Pre-trained PyTorch models for plant disease classification.
- `test/`: Folder containing sample images of various plant diseases and healthy plants for testing the models.
- `Screenshot 2025-06-19 175549.png`, `Screenshot 2025-06-19 175613.png`, `Screenshot 2025-06-19 175628.png`: Example screenshots showing model predictions or results.

## Usage

1. **Model Files**: Use the provided `.pth` files with your PyTorch inference scripts to classify plant diseases from images. Example usage:
   ```python
   import torch
   model = torch.load('plant-disease-model.pth')
   model.eval()
   # Add your image preprocessing and prediction code here
   ```
2. **Test Images**: Use the images in the `test/` folder to evaluate the model's performance or for demonstration purposes.
3. **Screenshots**: Refer to the screenshots for sample outputs and results.

## How to Contribute
- Fork the repository and create a new branch for your changes.
- Add your improvements or new features.
- Test your changes with the provided test images.
- Submit a pull request with a clear description of your changes.


---
For any questions or issues, please open an issue or contact the maintainer. 