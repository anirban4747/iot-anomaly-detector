import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_structure_data(normal_path, attack_path):
    print("Structuring streaming data logs...")
    
    normal_df = pd.read_csv(normal_path)
    attack_df = pd.read_csv(attack_path)
    
    normal_df['label'] = 0
    attack_df['label'] = 1
    
    combined_df = pd.concat([normal_df.head(20000), attack_df.head(20000)], axis=0)
    
    X = combined_df.drop(columns=['label'])
    y = combined_df['label']
    
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

if __name__ == "__main__":
    print("Data handling pipeline operational.")