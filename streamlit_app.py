import streamlit as st
import joblib
import pandas as pd
import warnings
import ntpath

warnings.simplefilter(action='ignore')

# def path_leaf(path):
#     _, tail = ntpath.split(path)
#     return tail or "Directory is empty"

# changeable
# test_data_path = 'test_data/patient1_6mers.npy'

# test_data = path_leaf(test_data_path)
# if test_data == "Directory is empty":
#     return FileNotFoundError("Path specified is a directory, not file. Select path to numpy file (.npy)")

data_source = st.radio("Select data source", ("Upload your own test data", "Use example test data"), key = "data_source")

if data_source == "Use example test data":
    test_data = "test_data/patient1_6mers.npy"
    result_file_name = test_data.split(".")[0].split("_")[0]
    loaded_array = np.load(test_data)
    st.write("Preview: ", loaded_array[:5])
else:
    test_data = st.file_uploader("Upload your test data (.npy)", type = ['npy'], key = "test_data")

if test_data is not None and st.button("Run Pathogen Prediction"):
    result_file_name = test_data.split(".")[0].split("_")[0]
    loaded_array = np.load(test_data)
    st.write("Preview: ", loaded_array[:5])
    
    # Labels to species conversion
    labels_to_species = pd.read_csv('labels_to_species.csv', index_col = 0)
    labels_df = dict(zip(labels_to_species.labels, labels_to_species.species_name))
    
    @st.cache_resource
    def load_models():
        decoy_detection = joblib.load("decoy_detection.joblib")
        pathogen_detection = joblib.load("pathogen_detection_rf.joblib")
        return decoy_detection, pathogen_detection

    decoy_detection, pathogen_detection = load_models()

    st.title("Pathogen Detection Project")
    st.write("A two-step approach used to detect pathogens (bacterial strains) from sample patient genomic data.")

    DECOY = 6
    RF_THRESHOLD = 0.63
    DECOY_THRESHOLD = 0.85
    MIN_UNIQUE_KMER = 500

    patient_df = pd.DataFrame(loaded_array)
    patient_df['num_cols_with_values'] = patient_df.gt(0).sum(axis = 1)

    # Filtering out reads with less than 500 unique k-mers
    patient_df = patient_df[patient_df['num_cols_with_values'] > MIN_UNIQUE_KMER]
    patient_df = patient_df.drop(['num_cols_with_values'], axis = 1)

    ### First model: detecting decoy
    y_pred_decoy = decoy_rf.predict(patient_df)
    # Filtering out decoys with threshold of 0.85
    if y_pred_decoy.sum() / len(y_pred_decoy) > DECOY_THRESHOLD:
        predictions = [DECOY]
    st.success(f"Decoy prediction: {predictions}")

    else:
        ### Second model: predicting pathogens
        y_predprob = pathogen_rf.predict_proba(patient_df)
        y_pred = np.argmax(y_predprob, axis = 1)
        
        # Filter out probabilities less than threshold of 0.63
        y_pred[np.where(y_predprob.max(axis = 1) < RF_THRESHOLD)] = -1
        predictions = list(np.unique(y_pred))

        # If there is a pathogen predicted, it is not a decoy dataset
        if DECOY in predictions:
            # Removing decoy
            predictions.remove(DECOY)
        if -1 in predictions:
            # Removing unconfident predictions
            predictions.remove(-1)
        
        predictions_species_name = list(map(lambda x:labels_df[x], predictions))
        st.success(f"Pathogen prediction: {predictions_species_name}")

        # Write to CSV result file
        with open(f"{result_file_name}.csv", "w") as file:
            file.write("labels")
            file.write('\n')
            for index, species in enumerate(predictions_species_name):
                file.write(species)
                if not index == len(predictions_species_name) - 1:
                    file.write('\n')

    return FileNotFoundError("No data uploaded. Please provide a numpy file (.npy) to run the prediction.")