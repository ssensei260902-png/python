# 🤖 Advanced Machine Learning with Python

## Complete Professional Guide from ML to Production Deployment

---

## Table of Contents

1. [Machine Learning Fundamentals](#1-machine-learning-fundamentals)
2. [Scikit-Learn Mastery](#2-scikit-learn-mastery)
3. [Deep Learning with TensorFlow/Keras](#3-deep-learning-with-tensorflowkeras)
4. [PyTorch for Deep Learning](#4-pytorch-for-deep-learning)
5. [Natural Language Processing](#5-natural-language-processing)
6. [Computer Vision](#6-computer-vision)
7. [MLOps & Model Deployment](#7-mlops--model-deployment)
8. [Production ML Systems](#8-production-ml-systems)

---

## 1. Machine Learning Fundamentals

### 1.1 Data Preprocessing Pipeline

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

class DataPreprocessor:
    """Professional data preprocessing pipeline"""

    def __init__(self):
        self.numeric_transformer = None
        self.categorical_transformer = None
        self.preprocessor = None

    def create_pipeline(self, numeric_features, categorical_features):
        """Create preprocessing pipeline"""

        # Numeric pipeline
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        # Categorical pipeline
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        # Combine pipelines
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])

        return self.preprocessor

    def fit_transform(self, X_train, y_train=None):
        """Fit and transform training data"""
        return self.preprocessor.fit_transform(X_train)

    def transform(self, X_test):
        """Transform test data"""
        return self.preprocessor.transform(X_test)


# Usage
df = pd.read_csv('data.csv')

# Separate features
numeric_features = ['age', 'income', 'credit_score']
categorical_features = ['gender', 'education', 'occupation']

X = df[numeric_features + categorical_features]
y = df['target']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Preprocess
preprocessor = DataPreprocessor()
preprocessor.create_pipeline(numeric_features, categorical_features)

X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

print(f"Training shape: {X_train_processed.shape}")
print(f"Test shape: {X_test_processed.shape}")
```

---

## 2. Scikit-Learn Mastery

### 2.1 Complete Classification Pipeline

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns

class MLClassifier:
    """Professional ML classification system"""

    def __init__(self):
        self.models = {
            'logistic': LogisticRegression(max_iter=1000),
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(random_state=42),
            'svm': SVC(probability=True, random_state=42)
        }
        self.best_model = None
        self.best_score = 0

    def train_and_evaluate(self, X_train, y_train, X_test, y_test):
        """Train multiple models and compare"""
        results = {}

        for name, model in self.models.items():
            print(f"\n{'='*50}")
            print(f"Training {name.upper()}")
            print(f"{'='*50}")

            # Cross-validation
            cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
            cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='f1')

            print(f"Cross-validation F1: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

            # Train on full training set
            model.fit(X_train, y_train)

            # Predict
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]

            # Evaluate
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred),
                'recall': recall_score(y_test, y_pred),
                'f1': f1_score(y_test, y_pred),
                'roc_auc': roc_auc_score(y_test, y_pred_proba)
            }

            results[name] = {
                'model': model,
                'metrics': metrics,
                'predictions': y_pred,
                'probabilities': y_pred_proba
            }

            print(f"\nTest Metrics:")
            for metric, value in metrics.items():
                print(f"  {metric}: {value:.4f}")

            # Track best model
            if metrics['f1'] > self.best_score:
                self.best_score = metrics['f1']
                self.best_model = model

        return results

    def hyperparameter_tuning(self, X_train, y_train, model_name='random_forest'):
        """Hyperparameter tuning with GridSearchCV"""

        param_grids = {
            'random_forest': {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 20, 30, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            },
            'gradient_boosting': {
                'n_estimators': [100, 200],
                'learning_rate': [0.01, 0.1, 0.3],
                'max_depth': [3, 5, 7],
                'subsample': [0.8, 1.0]
            },
            'svm': {
                'C': [0.1, 1, 10],
                'gamma': ['scale', 'auto', 0.001, 0.01],
                'kernel': ['rbf', 'linear']
            }
        }

        model = self.models[model_name]
        param_grid = param_grids[model_name]

        print(f"\nTuning {model_name}...")
        grid_search = GridSearchCV(
            model,
            param_grid,
            cv=5,
            scoring='f1',
            n_jobs=-1,
            verbose=1
        )

        grid_search.fit(X_train, y_train)

        print(f"\nBest parameters: {grid_search.best_params_}")
        print(f"Best F1 score: {grid_search.best_score_:.4f}")

        return grid_search.best_estimator_

    def plot_confusion_matrix(self, y_true, y_pred, title='Confusion Matrix'):
        """Plot confusion matrix"""
        cm = confusion_matrix(y_true, y_pred)

        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(title)
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.show()

    def plot_roc_curve(self, y_true, y_pred_proba, title='ROC Curve'):
        """Plot ROC curve"""
        fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
        auc = roc_auc_score(y_true, y_pred_proba)

        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, label=f'AUC = {auc:.4f}')
        plt.plot([0, 1], [0, 1], 'k--', label='Random')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()

    def feature_importance(self, feature_names):
        """Get feature importance"""
        if hasattr(self.best_model, 'feature_importances_'):
            importances = self.best_model.feature_importances_
            indices = np.argsort(importances)[::-1]

            plt.figure(figsize=(10, 6))
            plt.title("Feature Importances")
            plt.bar(range(len(importances)), importances[indices])
            plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=90)
            plt.tight_layout()
            plt.show()

            return dict(zip(feature_names, importances))


# Usage
classifier = MLClassifier()

# Train and evaluate all models
results = classifier.train_and_evaluate(X_train, y_train, X_test, y_test)

# Hyperparameter tuning for best model
best_model = classifier.hyperparameter_tuning(X_train, y_train, 'random_forest')

# Visualizations
classifier.plot_confusion_matrix(y_test, results['random_forest']['predictions'])
classifier.plot_roc_curve(y_test, results['random_forest']['probabilities'])
```

---

## 3. Deep Learning with TensorFlow/Keras

### 3.1 Neural Network for Classification

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
import numpy as np

class NeuralNetworkClassifier:
    """Professional neural network classifier"""

    def __init__(self, input_dim, num_classes=2):
        self.input_dim = input_dim
        self.num_classes = num_classes
        self.model = None
        self.history = None

    def build_model(self, hidden_layers=[128, 64, 32]):
        """Build neural network architecture"""

        self.model = Sequential()

        # Input layer
        self.model.add(Dense(
            hidden_layers[0],
            activation='relu',
            input_dim=self.input_dim
        ))
        self.model.add(BatchNormalization())
        self.model.add(Dropout(0.3))

        # Hidden layers
        for units in hidden_layers[1:]:
            self.model.add(Dense(units, activation='relu'))
            self.model.add(BatchNormalization())
            self.model.add(Dropout(0.3))

        # Output layer
        if self.num_classes == 2:
            self.model.add(Dense(1, activation='sigmoid'))
            loss = 'binary_crossentropy'
            metrics = ['accuracy', tf.keras.metrics.AUC()]
        else:
            self.model.add(Dense(self.num_classes, activation='softmax'))
            loss = 'sparse_categorical_crossentropy'
            metrics = ['accuracy']

        # Compile
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss=loss,
            metrics=metrics
        )

        return self.model

    def train(self, X_train, y_train, X_val, y_val, epochs=100, batch_size=32):
        """Train the model with callbacks"""

        # Callbacks
        early_stopping = callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )

        reduce_lr = callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7
        )

        model_checkpoint = callbacks.ModelCheckpoint(
            'best_model.h5',
            monitor='val_loss',
            save_best_only=True
        )

        tensorboard = callbacks.TensorBoard(
            log_dir='./logs',
            histogram_freq=1
        )

        # Train
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr, model_checkpoint, tensorboard],
            verbose=1
        )

        return self.history

    def evaluate(self, X_test, y_test):
        """Evaluate model"""
        results = self.model.evaluate(X_test, y_test, verbose=0)

        print("\nTest Results:")
        for name, value in zip(self.model.metrics_names, results):
            print(f"{name}: {value:.4f}")

        return results

    def predict(self, X):
        """Make predictions"""
        predictions = self.model.predict(X)

        if self.num_classes == 2:
            return (predictions > 0.5).astype(int)
        else:
            return np.argmax(predictions, axis=1)

    def plot_training_history(self):
        """Plot training history"""
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 2, figsize=(15, 5))

        # Loss
        axes[0].plot(self.history.history['loss'], label='Train Loss')
        axes[0].plot(self.history.history['val_loss'], label='Val Loss')
        axes[0].set_title('Model Loss')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Loss')
        axes[0].legend()
        axes[0].grid(True)

        # Accuracy
        axes[1].plot(self.history.history['accuracy'], label='Train Accuracy')
        axes[1].plot(self.history.history['val_accuracy'], label='Val Accuracy')
        axes[1].set_title('Model Accuracy')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Accuracy')
        axes[1].legend()
        axes[1].grid(True)

        plt.tight_layout()
        plt.show()


# Usage
nn = NeuralNetworkClassifier(input_dim=X_train.shape[1], num_classes=2)

# Build model
model = nn.build_model(hidden_layers=[128, 64, 32])
print(model.summary())

# Train
history = nn.train(X_train, y_train, X_val, y_val, epochs=100, batch_size=32)

# Evaluate
nn.evaluate(X_test, y_test)

# Plot
nn.plot_training_history()

# Predict
predictions = nn.predict(X_test)
```

---

## 4. PyTorch for Deep Learning

### 4.1 Custom PyTorch Model

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np

class CustomDataset(Dataset):
    """Custom PyTorch dataset"""

    def __init__(self, X, y):
        self.X = torch.FloatTensor(X)
        self.y = torch.FloatTensor(y)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


class NeuralNet(nn.Module):
    """PyTorch neural network"""

    def __init__(self, input_size, hidden_sizes, num_classes, dropout=0.3):
        super(NeuralNet, self).__init__()

        layers = []

        # Input layer
        layers.append(nn.Linear(input_size, hidden_sizes[0]))
        layers.append(nn.ReLU())
        layers.append(nn.BatchNorm1d(hidden_sizes[0]))
        layers.append(nn.Dropout(dropout))

        # Hidden layers
        for i in range(len(hidden_sizes) - 1):
            layers.append(nn.Linear(hidden_sizes[i], hidden_sizes[i + 1]))
            layers.append(nn.ReLU())
            layers.append(nn.BatchNorm1d(hidden_sizes[i + 1]))
            layers.append(nn.Dropout(dropout))

        # Output layer
        layers.append(nn.Linear(hidden_sizes[-1], num_classes))

        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)


class PyTorchTrainer:
    """Professional PyTorch training system"""

    def __init__(self, model, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.model = model.to(device)
        self.device = device
        self.history = {'train_loss': [], 'val_loss': [], 'train_acc': [], 'val_acc': []}

    def train_epoch(self, train_loader, criterion, optimizer):
        """Train for one epoch"""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(self.device), labels.to(self.device)

            # Forward pass
            optimizer.zero_grad()
            outputs = self.model(inputs)

            # Calculate loss
            loss = criterion(outputs, labels.long())

            # Backward pass
            loss.backward()
            optimizer.step()

            # Statistics
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        epoch_loss = running_loss / len(train_loader)
        epoch_acc = 100 * correct / total

        return epoch_loss, epoch_acc

    def validate(self, val_loader, criterion):
        """Validate model"""
        self.model.eval()
        running_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)

                outputs = self.model(inputs)
                loss = criterion(outputs, labels.long())

                running_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        epoch_loss = running_loss / len(val_loader)
        epoch_acc = 100 * correct / total

        return epoch_loss, epoch_acc

    def train(self, train_loader, val_loader, epochs=100, lr=0.001):
        """Full training loop"""
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', patience=5, factor=0.5
        )

        best_val_loss = float('inf')

        for epoch in range(epochs):
            # Train
            train_loss, train_acc = self.train_epoch(train_loader, criterion, optimizer)

            # Validate
            val_loss, val_acc = self.validate(val_loader, criterion)

            # Update learning rate
            scheduler.step(val_loss)

            # Save history
            self.history['train_loss'].append(train_loss)
            self.history['val_loss'].append(val_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_acc'].append(val_acc)

            # Save best model
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                torch.save(self.model.state_dict(), 'best_model.pth')

            # Print progress
            if (epoch + 1) % 10 == 0:
                print(f'Epoch [{epoch+1}/{epochs}]')
                print(f'  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%')
                print(f'  Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%')
                print(f'  LR: {optimizer.param_groups[0]["lr"]:.6f}')

        return self.history


# Usage
# Prepare data
train_dataset = CustomDataset(X_train, y_train)
val_dataset = CustomDataset(X_val, y_val)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Create model
model = NeuralNet(
    input_size=X_train.shape[1],
    hidden_sizes=[128, 64, 32],
    num_classes=2,
    dropout=0.3
)

# Train
trainer = PyTorchTrainer(model)
history = trainer.train(train_loader, val_loader, epochs=100, lr=0.001)
```

---

## 5. Natural Language Processing

### 5.1 Text Classification with Transformers

```python
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)
from datasets import Dataset
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

class TextClassifier:
    """Text classification with Transformers"""

    def __init__(self, model_name='distilbert-base-uncased', num_labels=2):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_labels
        )

    def tokenize_data(self, texts):
        """Tokenize texts"""
        return self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors='pt'
        )

    def prepare_dataset(self, texts, labels):
        """Prepare dataset for training"""
        encodings = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512
        )

        return Dataset.from_dict({
            'input_ids': encodings['input_ids'],
            'attention_mask': encodings['attention_mask'],
            'labels': labels
        })

    def compute_metrics(self, pred):
        """Compute evaluation metrics"""
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)

        precision, recall, f1, _ = precision_recall_fscore_support(
            labels, preds, average='binary'
        )
        acc = accuracy_score(labels, preds)

        return {
            'accuracy': acc,
            'f1': f1,
            'precision': precision,
            'recall': recall
        }

    def train(self, train_texts, train_labels, val_texts, val_labels, output_dir='./results'):
        """Train the model"""
        # Prepare datasets
        train_dataset = self.prepare_dataset(train_texts, train_labels)
        val_dataset = self.prepare_dataset(val_texts, val_labels)

        # Training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=3,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=64,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=100,
            evaluation_strategy='epoch',
            save_strategy='epoch',
            load_best_model_at_end=True,
        )

        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=self.compute_metrics
        )

        # Train
        trainer.train()

        return trainer

    def predict(self, texts):
        """Make predictions"""
        encodings = self.tokenize_data(texts)

        self.model.eval()
        with torch.no_grad():
            outputs = self.model(**encodings)

        predictions = torch.argmax(outputs.logits, dim=-1)
        probabilities = torch.softmax(outputs.logits, dim=-1)

        return predictions.numpy(), probabilities.numpy()


# Usage
texts_train = ["This is great!", "This is terrible", "I love it", "I hate it"]
labels_train = [1, 0, 1, 0]

classifier = TextClassifier()
trainer = classifier.train(texts_train, labels_train, texts_val, labels_val)

# Predict
predictions, probabilities = classifier.predict(["This is amazing!"])
print(f"Prediction: {predictions[0]}, Probability: {probabilities[0]}")
```

---

## 6. Model Deployment

### 6.1 FastAPI ML Model Serving

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from typing import List

# Load model
model = joblib.load('model.pkl')
preprocessor = joblib.load('preprocessor.pkl')

app = FastAPI(title="ML Model API")


class PredictionInput(BaseModel):
    """Input schema"""
    features: List[float]


class PredictionOutput(BaseModel):
    """Output schema"""
    prediction: int
    probability: float


@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    """Make prediction"""
    try:
        # Preprocess
        features = np.array(input_data.features).reshape(1, -1)
        features_processed = preprocessor.transform(features)

        # Predict
        prediction = model.predict(features_processed)[0]
        probability = model.predict_proba(features_processed)[0][prediction]

        return PredictionOutput(
            prediction=int(prediction),
            probability=float(probability)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "healthy"}


# Run with: uvicorn app:app --reload
```

---

This comprehensive guide covers everything from basic ML to production deployment. Practice these techniques to become an ML expert!
