import os
import joblib
import xgboost as xgb
from sklearn.metrics import classification_report, confusion_matrix
from preprocess import load_and_structure_data

def execute_training():
    normal_input = "data/1.benign.csv"
    attack_input = "data/1.mirai.udp.csv"
    
    if not os.path.exists(normal_input) or not os.path.exists(attack_input):
        print(f"Data files missing. Please ensure {normal_input} and {attack_input} are in the data/ folder.")
        return

    X_train, X_test, y_train, y_test, scaler = load_and_structure_data(normal_input, attack_input)
    
    print("Initializing model training across XGBoost parameters...")
    classifier = xgb.XGBClassifier(
        n_estimators=150,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        random_state=42
    )
    
    classifier.fit(X_train, y_train)
    
    predictions = classifier.predict(X_test)
    print("\n--- Network Security Model Evaluation Summary ---")
    print(classification_report(y_test, predictions, target_names=["Normal Traffic", "Botnet Anomaly"]))
    
    print("Confusion Matrix Layout:")
    print(confusion_matrix(y_test, predictions))
    
    os.makedirs('models', exist_ok=True)
    joblib.dump(classifier, 'models/iot_anomaly_xgboost.pkl')
    joblib.dump(scaler, 'models/pipeline_scaler.pkl')
    print("\nModel weights and scaling parameters exported to models/ directory.")

if __name__ == "__main__":
    execute_training()