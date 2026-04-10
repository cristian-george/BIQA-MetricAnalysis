# Comparison of Classical and Machine Learning Methods for Blind Image Quality Assessment

This repository contains the source code used in our IEEE Access paper:
"Comparing Blind Image Quality Metrics for Reliable Image Assessment".

It includes:
- classical feature-based BIQA methods (MATLAB)
- machine learning based BIQA methods (Python/TensorFlow)
- dataset preprocessing scripts for reproducing the experimental setup from the paper

<br>

## Dataset access and availability
Datasets are not redistributed in this repository.

They must be downloaded separately from their official sources, then arranged to match the folder structure expected by the scripts/configuration files.

<br>

## Repository layout
- `preprocess_datasets/`: stand-alone preprocessing scripts used to prepare the datasets.
- `feature-based_methods/`: MATLAB implementations for BRISQUE, NIQE, BIQI, BLIINDS-2, and DIIVINE.
- `ML-based_methods/`: Python training/evaluation pipeline for deep BIQA predictors.

<br>

## Dataset preprocessing
Install preprocessing dependencies from the dedicated file:

```bash
cd preprocess_datasets
pip install -r requirements.txt
```

Current scripts:
- `data_splitting.py`: split KonIQ-10K into train/validation/test and generate corresponding CSV label files.
- `FLIVE.py`: white-pad FLIVE images to `384x512`.
- `FLIVE_Patch.py`: white-pad FLIVE Patch images to `256x256`.
- `LIVE2.py`: white-pad LIVE2 class images to `384x512`.
- `LIVEitW.py`: resize LIVEitW images to `512x512`.

Important notes:
- Paths are resolved relative to the current working directory (the folder from which you run each command), not relative to the script file itself.
- For the default paths in this repository, run preprocessing scripts from `preprocess_datasets/`. For example:
  ```bash
  cd preprocess_datasets
  python LIVE2.py
  ```

- Update `input_folder`, `output_folder`, or dataset root variables inside each script to match your local dataset location before running.
- This is intentional and follows the reproducibility setup described in the article.

<br>

## Feature-based methods
The code for the classical blind image quality estimators (BRISQUE, NIQE, BIQI, BLIINDS-2, and DIIVINE) is based on the implementation available [here](https://github.com/dsoellinger/blind_image_quality_toolbox). Several modifications have been made to ensure compatibility with MATLAB R2022b.

<br>

## ML-based methods

### (0) Environment setup
Use Python 3.11 for reproducibility.

In the paper, experiments were run with TensorFlow 2.15. In this repository, dependencies were updated to TensorFlow 2.20 to keep the project up-to-date.

Install dependencies:

```bash
cd ML-based_methods
pip install -r requirements.txt
```

### (1) Pre-trained weights
Pre-trained model weights are available [here](https://drive.google.com/drive/folders/1PWRgR8h7esZezD9ReSY-hXaCvMHFzGN4?usp=sharing).


The Drive contains 3 archives (one per training setup used in the paper):
- trained on KonIQ-10K
- trained on LIVE2
- trained on LIVE2+KonIQ-10K

Extract these archives into:
- `data/trained_on_KonIQ-10K/models`
- `data/trained_on_LIVE2/models`
- `data/trained_on_LIVE2+KonIQ-10K/models`


### (2) Running the project
The project is executed via `main.py`:

```bash
cd ML-based_methods
python main.py
```

Interactive options in `main.py`:
- `1`: train a model
- `2`: evaluate a model
- `3`: print model summary
- `4`: plot score distribution
- `5`: plot predicted vs. true scores
- `6`: plot difference error
- `7`: plot absolute error

### (3) Configuration files
To train/evaluate a model, edit files in `ML-based_methods/config`:

1. `model_config.json`
- Select architecture with `net_name` (for example: `efficientnet_v2_s`, `resnet50`, `inception_v3`, `vgg16`, `nasnet_mobile`).
- Set input size with `input_shape`.
- Control fine-tuning with `freeze_backbone` and `freeze_head_bn`.
- Configure prediction head with `pooling`, `dense`, and `dropout`.

2. `train_config.json`
- Set dataset location with `root_directory` (typically under `../../Datasets/...`).
- Choose train/validation image subfolders with `train_directory` and `val_directory`.
- Set CSV label files with `train_lb` and `val_lb`.
- Configure optimization/training: `augment`, `batch_size`, `epoch_size`, `loss`, and `lr` schedule.
- Configure checkpoints and logs under `callbacks` (`tensorboard` and `model_checkpoint`).
- For resumed training, set `continue_train.from_epoch` and `continue_train.from_weights`.

3. `evaluate_config.json`
- Set `weights_path` to the `.h5`/`weights.h5` checkpoint to evaluate.
- Set `test_dirs` (one folder or a list of folders).
- Set `test_lbs` to matching CSV files (or `null` for unlabeled inference).
- Keep `batch_size` consistent with available memory.

Note: when `test_lbs` is provided, its length must match `test_dirs`.

CSV notes:
- Training/evaluation CSV files are expected to include `image_name`.
- For supervised evaluation metrics (PLCC/SROCC/KROCC/RMSE), include a `MOS` column.
- If `MOS` is missing and `test_lbs` is `null`, inference still runs and saves predicted MOS only.

<br>

## Summary
1. Prepare datasets under your local `Datasets/` root (or update all paths in scripts/configs accordingly).
2. Optionally run the preprocessing scripts from `preprocess_datasets/`.
3. Install dependencies and run `main.py` from `ML-based_methods/`.
4. Edit `config/model_config.json`, `config/train_config.json`, and `config/evaluate_config.json` for your experiment.
5. Train (`option 1`) and/or evaluate (`option 2`) from the interactive menu.

<br>

## Citation
If you use this code in research, please cite:

```bibtex
@ARTICLE{fieraru2025comparing,
	author={Fieraru, Cristian George and Biserică, Maria and Plajer, Ioana Cristina and Ivanovici, Mihai},
	journal={IEEE Access},
	title={Comparing Blind Image Quality Metrics for Reliable Image Assessment},
	year={2025},
	volume={13},
	number={},
	pages={110322-110335},
	doi={10.1109/ACCESS.2025.3583029}
}
```
