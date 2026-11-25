<h1 align="center">qsiprep test suna - full config</h1>

<p align="center">
  Preprocesses DWI with QSIPrep 0.24.0 (denoising, Gibbs unringing, eddy head-motion and TOPUP distortion correction, coregistration to the T1w) and outputs the preprocessed DWI, T1w, brain mask, tissue segmentation, confounds, image QC and an HTML report.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.859"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.859-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-see_LICENSE-lightgrey.svg" alt="License"></a>
</p>

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Preprocesses DWI with QSIPrep 0.24.0 (denoising, Gibbs unringing, eddy head-motion and TOPUP distortion correction, coregistration to the T1w) and outputs the preprocessed DWI, T1w, brain mask, tissue segmentation, confounds, image QC and an HTML report.**

Converts the T1w and one or more DWI runs to BIDS (optionally naming the runs from the BidsGuess metadata so opposite phase-encoding pairs are grouped) and runs QSIPrep participant-level preprocessing with the selected denoising, unringing, head-motion, B1 bias and PEPOLAR settings, then maps the outputs to brainlife datatypes in ACPC/T1w or MNI152NLin2009cAsym space. Use it for multi-shell, HCP-style data acquired with opposite phase-encoding directions; a second DWI must have the opposite phase-encoding direction of the first. Needs a FreeSurfer license on the compute resource. Registered as a test configuration (name 'qsiprep test suna - full config').

| | |
|---|---|
| **Inputs** | `neuro/anat/t1w` · `neuro/dwi` |
| **Outputs** | `neuro/dwi` · `neuro/anat/t1w` · `neuro/parcellation/volume` · `neuro/mask` · `report/html` · `neuro/regressors` · `raw` |
| **Container** | `pennbbl/qsiprep:0.24.0` |
| **Requires** | `FREESURFER_LICENSE` |
| **Run it** | [doi.org/10.25663/brainlife.app.859](https://doi.org/10.25663/brainlife.app.859) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `t1` | `neuro/anat/t1w` (!qsiprep) | yes | T1-weighted image of the subject (not already processed by QSIPrep). |
| `dwi` | `neuro/dwi` (!qsiprep, !preprocessed) | yes | One or more raw DWI runs with bvals, bvecs and optional sbref. Multiple runs should be opposite phase-encoding acquisitions; with dwi_use_bidsguess the metadata should contain BidsGuess. |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `output_dwi` | `neuro/dwi` | Preprocessed DWI in ACPC space with bvals and bvecs (FSL-style, or MRtrix-style when xflip is true). |
| `output_anat_preproc` | `neuro/anat/t1w` | Preprocessed T1w in the selected output space. |
| `output_dseg` | `neuro/parcellation/volume` | QSIPrep tissue segmentation (dseg) in the selected space. |
| `output_brainmask` | `neuro/mask` | Brain mask of the preprocessed T1w. |
| `output_report` | `report/html` | QSIPrep HTML report with figures. |
| `regressors` | `neuro/regressors` | DWI confounds time series (regressors.tsv). |
| `dwiqc` | `raw` | QSIPrep DWI image quality metrics (dwiqc.csv). |

<details>
<summary><b>Parameters</b> (13)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `output_resolution` | number | `1.2` | The isotropic voxel size in mm the data will be resampled to after preprocessing. NOTE: only dwi data will be resampled. Usually this should be the same as the input resolution. |
| `output_space` | enum | `T1w` | Volume and surface spaces to resample DWIs into. NOTE: If selecting T1w, the preprocessed T1w image defines the T1w space, not the native T1. Reconstructed surfaces will be registered to the T1w space (ACPC), and not to the input images. WARNING: If selecting template, dwis will be still resampled to the T1w space (and not to the template). *template choice not tested in this version of QSIPrep configuration. Options: `T1w`, `MNI152NLin2009cAsym`. |
| `skipbidsvalidation` | boolean | `false` | Skip the BIDS validation of input data. Try this option if your data is not BIDS compatible but you'd like to go ahead and process it through qsiprep anyway. |
| `denoise_method` | enum | `dwidenoise` | Image-based denoising method. Options: `dwidenoise`, `patch2self`, `none`. |
| `dwi_use_bidsguess` | boolean | `true` | Whether to rename dwi files in bids format based on "BidsGuess" field in metadata. If processing opposite PE directions, must check this option, otherwise QSIPrep cannot pickup the correct dwis to combine |
| `distortion_group_merge` | enum | `average` | How to combine images across distorted groups. Use "average" HCP style OPE (see QSIPrep documentation for detail: https://qsiprep.readthedocs.io/en/latest/preprocessing.html#preprocessing-hcp-style) Options: `none`, `average`, `concat`. |
| `unringing_method` | enum | `mrdegibbs` | Method for Gibbs-ringing removal. Options: `none`, `mrdegibbs`, `rpg`. |
| `b1_biascorrect_stage` | enum | `none` | The stage of processing at which to apply B1 bias correction. Either “final” (after resampling), “none” (skipped entirely) or “legacy” (before concatenation). NOTE: If your sequence has "prescan norm" on, then skip b1 biascorrection, otherwise it might introduce artifacts (see documentation: https://qsiprep.readthedocs.io/en/latest/preprocessing.html#denoising-and-merging-images) Options: `final`, `none`, `legacy`. |
| `hmc_transform` | enum | `Affine` | Transformation to be optimized during head motion correction. Options: `Affine`, `Ridit`. |
| `hmc_model` | enum | `eddy` | Model used to generate target images for hmc. Options: `eddy`, `none`, `3dSHORE`, `tensor`. |
| `pepolar_method` | enum | `TOPUP` | SDC method to be used for PEPOLAR fieldmaps. NOTE: only TOPUP tested. Options: `TOPUP`, `DRBUDDI`, `TOPUP+DRBUDDI`. |
| `b0_to_t1w_transform` | enum | `Rigid` | Transformation model for intramodal registration. Options: `Rigid`, `Affine`. |
| `xflip` | boolean | `true` | Save output bvecs in MRtrix-style. If false (default), bvecs will be saved in FSL-style and will be compatible with DIPY and DSI Studio. |

</details>

<!-- brainlife-app:end -->

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.859](https://doi.org/10.25663/brainlife.app.859), choose `neuro/anat/t1w`, `neuro/dwi` from your project, set the parameters and press **Execute**. The results are saved to your project as `neuro/dwi`, `neuro/anat/t1w`, `neuro/parcellation/volume`, `neuro/mask`, `report/html`, `neuro/regressors`, `raw`.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/) (the App runs in `pennbbl/qsiprep:0.24.0`), [`jq`](https://jqlang.github.io/jq/), `FREESURFER_LICENSE`.

1. Clone this repository.
2. Create `config.json` with the paths to your inputs and the parameters:

   ```json
   {
       "t1": "/path/to/t1/t1",
       "dwi": "/path/to/dwi/dwi",
       "bvecs": "/path/to/dwi/bvecs",
       "bvals": "/path/to/dwi/bvals",
       "sbref": "/path/to/dwi/sbref",
       "sbref_json": "/path/to/dwi/sbref_json",
       "output_resolution": 1.2,
       "output_space": "T1w",
       "skipbidsvalidation": false,
       "denoise_method": "dwidenoise",
       "dwi_use_bidsguess": true,
       "distortion_group_merge": "average",
       "unringing_method": "mrdegibbs",
       "b1_biascorrect_stage": "none",
       "hmc_transform": "Affine",
       "hmc_model": "eddy",
       "pepolar_method": "TOPUP",
       "b0_to_t1w_transform": "Rigid",
       "xflip": true
   }
   ```

3. Run `./main`.

## Troubleshooting

- **Please set FREESURFER_LICENSE in .bashrc**: Set FREESURFER_LICENSE on the compute resource.

## Citing

If you use this App, please cite it, the software it builds on and brainlife.io:

- qsiprep test suna - full config. brainlife.io App. [doi:10.25663/brainlife.app.859](https://doi.org/10.25663/brainlife.app.859)
- Cieslak M. et al. QSIPrep: an integrative platform for preprocessing and reconstructing diffusion MRI data. Nature Methods 18, 775-778 (2021). [doi:10.1038/s41592-021-01185-5](https://doi.org/10.1038/s41592-021-01185-5)
- Matthew Cieslak, Philip A. Cook, Xiaosong He, Fang-Cheng Yeh, Thijs Dhollander, Azeez Adebimpe, Geoffrey K. Aguirre, Danielle S. Bassett, Richard F. Betzel, Josiane Bourque, Laura M. Cabral, Christos Davatzikos, John Detre, Eric Earl, Mark A. Elliott, Shreyas Fadnavis, Damien A. Fair, Will Foran, Panagiotis Fotiadis, Eleftherios Garyfallidis, Barry Giesbrecht, Ruben C. Gur, Raquel E. Gur, Max Kelz, Anisha Keshavan, Bart S. Larsen, Beatriz Luna, Allyson P. Mackey, Michael Milham, Desmond J. Oathes, Anders Perrone, Adam R. Pines, David R. Roalf, Adam Richie-Halford, Ariel Rokem, Valerie J. Sydnor, Tinashe M. Tapera, Ursula A. Tooley, Jean M. Vettel, Jason D. Yeatman, Scott T. Grafton, Theodore D. Satterthwaite. QSIPrep: An integrative platform for preprocessing and reconstructing diffusion MRI. bioRxiv 2020.09.04.282269; doi: https://doi.org/10.1101/2020.09.04.282269
- Fischl. FreeSurfer. *NeuroImage* 62:774-781 (2012). [doi:10.1016/j.neuroimage.2012.01.021](https://doi.org/10.1016/j.neuroimage.2012.01.021)
- Tournier et al. MRtrix3: A fast, flexible and open software framework for medical image processing and visualisation. *NeuroImage* 202:116137 (2019). [doi:10.1016/j.neuroimage.2019.116137](https://doi.org/10.1016/j.neuroimage.2019.116137)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

- Giulia Bertò ([@giulia-berto](https://github.com/giulia-berto))
- Soichi Hayashi ([@soichih](https://github.com/soichih))

**Project director**

- Franco Pestilli ([@francopestilli](https://github.com/francopestilli))

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io, which runs this App, is publicly funded by Wellcome, the U.S. National Institutes of Health and the U.S. National Science Foundation; acknowledging that support helps keep it running.</sub>

## License

See [LICENSE](LICENSE).
