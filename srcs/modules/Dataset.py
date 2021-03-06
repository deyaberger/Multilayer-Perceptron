try:
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from utils import conf, print_and_exit
except ModuleNotFoundError as e:
    import sys
    print(f"{e}\nPlease run 'pip install -r requirements.txt'")
    sys.exit()


class Dataset:
    '''
    This class is used to read a specific dataset,
    clean and organize the data so it can be easily used as vectors and matrices for machine learning calculations.
    '''
    def __init__(self, datafile):
        df = self.read_specific_csv(datafile)
        self.from_df_to_matrix(df)
    
    def read_specific_csv(self, datafile):
        try:
            df = pd.read_csv(datafile, header = None)
            self.features = [f"feature {i}" for i in range(df.shape[1] - 2)]
            self.y_name = "diagnosis"
            columns = ["id", self.y_name]
            columns.extend(self.features)
            df.columns = columns
            return (df)
        except Exception as e:
            print_and_exit(f"Error in function 'read_specific_csv' :\n{e}")

    def from_df_to_matrix(self, df):
        '''
        Fillna: fills the empty cells in our dataset with the median value of the columns
        one_hot_encoding : Transforms the options in our output column ("B", "M") into binary numbers: [10, 01]
        X shape (examples, features)
        y shape (examples, predictions)
        prediction is of size 2 (0 or 1)
        '''
        df[self.features] = df[self.features].fillna(df[self.features].median())
        self.X = df[self.features].to_numpy()
        one_hot_encoding = pd.get_dummies(df[self.y_name], drop_first = False)
        self.y_classification = list(one_hot_encoding.columns)
        self.y = one_hot_encoding.to_numpy()
    
    
    def feature_scale_normalise(self):
        '''
        Feature scale the data to converge faster
        '''
        self.scaler = StandardScaler()
        self.scaler.fit(self.X)
        self.X = self.scaler.transform(self.X)


    def split_data(self):
        '''
        Splitting the data into the training set (on which to fit the model) and the testing set (to help evaluate our model)
        '''
        try:
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, train_size=conf.train_size, random_state=42)
        except ValueError as e:
            print_and_exit(f"Error While splitting the data:\n{e}")

    
    def __str__(self):
        return (f"{self.X_train.shape = }, {self.X_test.shape = }, {self.y_train.shape = }, {self.y_test.shape = }")
    