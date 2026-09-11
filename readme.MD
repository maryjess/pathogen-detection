# Pathogen Detection Project
## Knowledge Discovery in Bioinformatics

# Background

Disease diagnosis is hard, but crucial. If we could diagnose infections (specifically those caused by bacteria in the scope of this project) early, it will lead to better treatment and improved quality of life.

However, current diagnostic methods such as symptoms checking, blood tests, and imagery could be slow and inaccurate.

# Approach

DNA sequencing is fast and precise. If we could precisely identify reads from patients that are associated with pathogens, we could diagnose them quickly.

In this approach, we represent the reads as **canonical k-mers** (substring of length k), where k = 6.

Read more about canonical k-mers [here](https://bioinfologics.github.io/post/2018/09/17/k-mer-counting-part-i-introduction/).

We used Random Forest model with a two-step approach:

### **1. Decoy prediction model**

Since we noticed that there are [a lot of decoys](assets/species.png) associated with the given training dataset, we trained a random forest model to predict for decoys with threshold of 0.85 (i.e. if less than 85% of the reads are classified as decoys, then the model will regard the dataset as decoy)

### **2. Pathogen prediction model**

For the next step, we applied a threshold of 500 unique 6-mers present, as there was [a number of outliers present](assets/unique-kmers.png) with very few unique 6-mers present, which could be indication of a very short read length.

This second model is a multi-class random forest classifier that predicts the presence of pathogen(s).

# Running the model

### Input

Takes in the canonical 6-mer profile of patient reads, in the format of Numpy (.npy). See sample test data [here](test_data/patient1_6mers.npy).

### Output

Outputs the list of pathogen(s) predicted.

# Credits

Thanks to my fellow groupmates in uni who has contributed to this project:

### **Group Anything**

- Chew Zhen Yuan
- Eliza Soesanto
- Jessica Mary Listijo