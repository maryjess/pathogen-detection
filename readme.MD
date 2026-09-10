# CS4220 Pathogen Detection Project

Group Anything

- Chew Zhen Yuan
- Eliza Soesanto
- Jessica Mary Listijo

# Instructions on how to run the model

In this directory, there are several files:

- `labels_to_species.csv`, containing the mapping of the labels to each pathogen species
- `decoy_detection.joblib`, the first model to detect decoys
- `pathogen_detection_rf.joblib`, the second model to predict pathogens
- `final_two_step_approach.ipynb`, a Jupyter notebook containing a short code to run the model
- `readme.MD` this readme file, contains guide to run the model

See the steps below on how to run the model.

1. Open the `final_two_step_approach.ipynb` file
1. The third block is to configure the test data path. Currently it is set to be for `patient1_6mers.npy`, assuming that it is inside the `test_data` directory. The `test_data_path` at the third line could be changed to the path for the test data used. The format of the test data should be in the forms of NumPy array `.npy`. Make sure it leads to an `.npy` file, not a directory.
1. The paths for the `labels_to_species.csv` file and the two models are already configured.
1. The last block will print out the predicted species and output them as a CSV file as the result file. The output is named according to the test data provided, for instance `patient1.csv` if the test data is `patient1_6mers.npy`.
