import torch
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    Trainer, TrainingArguments, EarlyStoppingCallback
)
from datasets import Dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from sklearn.model_selection import KFold
import shutil
import os

# ================================================================================
# DETECTAR GPU AUTOMATICAMENTE + DEFINIR FP16/BF16 CORRETAMENTE
# ================================================================================

if torch.cuda.is_available():
    device = "cuda"
    print("[INFO] GPU CUDA detectada.")
elif torch.backends.mps.is_available():
    device = "mps"
    print("[INFO] GPU Apple Silicon (MPS) detectada.")
else:
    device = "cpu"
    print("[INFO] Nenhuma GPU detectada → usando CPU.")

use_fp16 = False
use_bf16 = False
torch_dtype = torch.float32

if device == "cuda":
    if torch.cuda.is_bf16_supported():
        use_bf16 = True
        torch_dtype = torch.bfloat16
        print("[INFO] BF16 suportado → usando bf16=True.")
    else:
        use_fp16 = True
        torch_dtype = torch.float16
        print("[INFO] BF16 NÃO suportado → usando fp16=True.")
elif device == "mps":
    torch_dtype = torch.float16
    print("[INFO] Usando FP16 em MPS.")
else:
    print("[INFO] CPU → usando float32.")

# ================================================================================
# CALLBACK CORRIGIDO - Solução definitiva da comunidade
# ================================================================================
class TrainEvalCallback(EarlyStoppingCallback):
    """
    Callback que avalia o conjunto de treino ao final de cada época usando trainer.predict,
    calcula métricas manualmente e salva em CSV.
    SOLUÇÃO CORRETA: trainer.predict + cálculo manual de loss/accuracy
    """
    def __init__(self, trainer_ref, train_dataset, suffix="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trainer = trainer_ref
        self.train_dataset = train_dataset
        self.suffix = suffix
        self.train_history = []

    def on_epoch_end(self, args, state, control, **kwargs):
        try:
            # 1. Fazer predições no conjunto de treino
            predictions = self.trainer.predict(self.train_dataset)
            
            # 2. Calcular accuracy manualmente
            y_true = predictions.label_ids
            y_pred = np.argmax(predictions.predictions, axis=-1)
            train_accuracy = accuracy_score(y_true, y_pred)
            
            # 3. Calcular loss manualmente (CORREÇÃO DEFINTIVA)
            logits = torch.tensor(predictions.predictions, dtype=torch.float32)
            labels = torch.tensor(predictions.label_ids, dtype=torch.long)
            loss_fn = torch.nn.CrossEntropyLoss(reduction='mean')
            train_loss = loss_fn(logits, labels).item()
            
            # 4. Salvar no histórico
            self.train_history.append({
                "epoch": float(state.epoch),
                "train_loss": train_loss,
                "train_accuracy": train_accuracy
            })
            
            # DEBUG (pode remover depois)
            # print(f"[TrainEval {self.suffix}] Época {state.epoch:.1f}: Loss={train_loss:.6f}, Acc={train_accuracy:.4f}")
            
        except Exception as e:
            print(f"[ERRO no callback {self.suffix}]: {e}")
        
        return control

    def on_train_end(self, args, state, control, **kwargs):
        if self.train_history:
            df = pd.DataFrame(self.train_history)
            csv_name = f"training_train_metrics_{self.suffix}.csv"
            df.to_csv(csv_name, index=False)
            print(f"[INFO] Métricas de TREINO salvas em '{csv_name}'")
        return control

# ================================================================================
# FUNÇÃO PARA PLOTAR MÉTRICAS - Versão corrigida
# ================================================================================
def plot_training_metrics(trainer, suffix=""):
    """
    Plota gráficos de loss e accuracy para treino e validação.
    Usa: - train_metrics do callback (treino)
         - log_history do trainer (validação)
    """
    # 1. Salvar histórico do trainer (validação)
    history = trainer.state.log_history
    if history:
        df_history = pd.DataFrame(history)
        df_history.to_csv(f"training_log_history_{suffix}.csv", index=False)
        print(f"[INFO] Histórico do Trainer salvo em 'training_log_history_{suffix}.csv'")
    else:
        print(f"[WARNING] Nenhum histórico encontrado para {suffix}")
        df_history = pd.DataFrame()
    
    # 2. Carregar métricas de treino do callback
    train_csv = f"training_train_metrics_{suffix}.csv"
    if os.path.exists(train_csv):
        df_train = pd.read_csv(train_csv)
        if df_train.empty:
            print(f"[WARNING] CSV de treino vazio para {suffix}")
            df_train = pd.DataFrame()
    else:
        print(f"[WARNING] Arquivo {train_csv} não encontrado")
        df_train = pd.DataFrame()
    
    # 3. Extrair séries de validação do log_history
    eval_entries = []
    for entry in history:
        if isinstance(entry, dict) and 'eval_loss' in entry:
            eval_entries.append(entry)
    
    if eval_entries:
        df_eval = pd.DataFrame(eval_entries)
        
        # Extrair épocas e métricas de validação
        if 'epoch' in df_eval.columns:
            epochs_eval = df_eval['epoch'].tolist()
        else:
            epochs_eval = list(range(1, len(df_eval) + 1))
        
        eval_loss = df_eval['eval_loss'].tolist() if 'eval_loss' in df_eval.columns else []
        eval_acc = df_eval['eval_accuracy'].tolist() if 'eval_accuracy' in df_eval.columns else []
    else:
        epochs_eval, eval_loss, eval_acc = [], [], []
    
    # 4. Extrair séries de treino do CSV
    if not df_train.empty:
        if 'epoch' in df_train.columns:
            epochs_train = df_train['epoch'].tolist()
        else:
            epochs_train = list(range(1, len(df_train) + 1))
        
        train_loss = df_train['train_loss'].tolist() if 'train_loss' in df_train.columns else []
        train_acc = df_train['train_accuracy'].tolist() if 'train_accuracy' in df_train.columns else []
    else:
        epochs_train, train_loss, train_acc = [], [], []
    
    # 5. Verificar consistência dos dados
    if len(epochs_eval) != len(eval_loss) or len(epochs_eval) != len(eval_acc):
        print(f"[WARNING] Dados de validação inconsistentes para {suffix}")
    
    if len(epochs_train) != len(train_loss) or len(epochs_train) != len(train_acc):
        print(f"[WARNING] Dados de treino inconsistentes para {suffix}")
    
    # 6. Plotar gráficos
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Subplot 1: Loss
    ax1 = axes[0]
    if epochs_train and train_loss:
        ax1.plot(epochs_train, train_loss, label='Train Loss', color='blue', linewidth=2)
    if epochs_eval and eval_loss:
        ax1.plot(epochs_eval, eval_loss, label='Validation Loss', color='red', 
                linestyle='--', linewidth=2)
    
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title(f'Loss durante Treinamento ({suffix})')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Subplot 2: Accuracy
    ax2 = axes[1]
    if epochs_train and train_acc:
        ax2.plot(epochs_train, train_acc, label='Train Accuracy', color='blue', linewidth=2)
    if epochs_eval and eval_acc:
        ax2.plot(epochs_eval, eval_acc, label='Validation Accuracy', color='green',
                linestyle='--', linewidth=2)
    
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.set_title(f'Acurácia de Treinamento e Validação ({suffix})')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar figura
    plt.savefig(f'training_metrics_{suffix}.png', dpi=600)
    plt.close()
    
    print(f'[INFO] Gráfico salvo em "training_metrics_{suffix}.png"')

# ================================================================================
# FUNÇÕES AUXILIARES (mantidas do original)
# ================================================================================
def carregar_codigos(caminho_arquivo, label):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read()
    codigos = conteudo.split("========================================")
    return [{"code": codigo.strip(), "label": label} for codigo in codigos if codigo.strip()]

def plot_final_accuracies(train_accuracy, val_accuracy, test_accuracy, suffix=""):
    plt.figure(figsize=(6, 4))
    accuracies = [train_accuracy, val_accuracy, test_accuracy]
    labels = ["Train", "Validation", "Test"]
    plt.bar(labels, accuracies, color=["blue", "orange", "green"])
    plt.ylabel("Acurácia")
    plt.title(f"Acurácias Finais ({suffix})")
    for i, v in enumerate(accuracies):
        plt.text(i, v, f"{v:.4f}", ha='center', va='bottom')
    plt.savefig(f"final_accuracies_{suffix}.png", dpi=600)
    plt.close()

def calcular_acuracia(trainer, train_dataset, val_dataset, test_dataset, suffix=""):
    train_results = trainer.predict(train_dataset)
    train_accuracy = accuracy_score(train_results.label_ids, np.argmax(train_results.predictions, axis=-1))
    val_results = trainer.predict(val_dataset)
    val_accuracy = accuracy_score(val_results.label_ids, np.argmax(val_results.predictions, axis=-1))
    test_results = trainer.predict(test_dataset)
    test_accuracy = accuracy_score(test_results.label_ids, np.argmax(test_results.predictions, axis=-1))
    print(f"Train: {train_accuracy:.4f} | Val: {val_accuracy:.4f} | Test: {test_accuracy:.4f}")
    plot_final_accuracies(train_accuracy, val_accuracy, test_accuracy, suffix)
    return train_accuracy, val_accuracy, test_accuracy

def avaliar_modelo(trainer, test_dataset, suffix=""):
    resultados = trainer.predict(test_dataset)
    y_true = resultados.label_ids
    y_pred = np.argmax(resultados.predictions, axis=-1)
    acc = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary')
    matriz_conf = confusion_matrix(y_true, y_pred)
    print(f"\n=== Métricas Finais ({suffix}) ===")
    print(f"Acurácia: {acc:.4f} | Precisão: {precision:.4f} | Recall: {recall:.4f} | F1: {f1:.4f}")
    plt.figure(figsize=(5, 4))
    sns.heatmap(matriz_conf, annot=True, fmt='d', cmap="Blues",
                xticklabels=["Indefinido", "Independente"],
                yticklabels=["Indefinido", "Independente"])
    plt.title(f"Matriz de Confusão ({suffix})")
    plt.savefig(f"confusion_matrix_{suffix}.png", dpi=600)
    plt.close()

# ================================================================================
# MAIN (mantida do original com correções)
# ================================================================================
def main():
    arquivo_independente = "codigos_independentes_balanceado.py"
    arquivo_indefinido = "codigos_indefinidos_balanceado.py"

    print("Carregando dados...")
    dados_indep = carregar_codigos(arquivo_independente, 1)
    dados_indef = carregar_codigos(arquivo_indefinido, 0)
    dataset = dados_indep + dados_indef

    # Embaralhar dados para evitar viés
    import random
    random.shuffle(dataset)
    
    print(f"Total de exemplos carregados: {len(dataset)}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    def tokenizar_exemplo(exemplos):
        return tokenizer(exemplos["code"], padding="max_length", truncation=True, max_length=512)

    dataset = Dataset.from_list(dataset)
    dataset = dataset.map(tokenizar_exemplo, batched=True)

    X = np.array(dataset["input_ids"])
    y = np.array(dataset["label"])
    attention_masks = np.array(dataset["attention_mask"])

    kf = KFold(n_splits=10, shuffle=True, random_state=42)
    resultados_folds = []

    for fold, (train_index, test_index) in enumerate(kf.split(X)):
        suffix = f"Fold{fold+1}"
        print(f"\n================ {suffix} ================")
        print(f"Treino: {len(train_index)} amostras, Teste: {len(test_index)} amostras")

        train_dataset = Dataset.from_dict({
            "input_ids": X[train_index],
            "attention_mask": attention_masks[train_index],
            "label": y[train_index]
        })
        test_dataset = Dataset.from_dict({
            "input_ids": X[test_index],
            "attention_mask": attention_masks[test_index],
            "label": y[test_index]
        })

        split = train_dataset.train_test_split(test_size=0.2, seed=42)
        train_dataset, val_dataset = split["train"], split["test"]
        
        print(f"Após split: Treino={len(train_dataset)}, Validação={len(val_dataset)}")

        # Formatar para tensores
        train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
        val_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
        test_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

        model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME,
            num_labels=2,
            torch_dtype=torch_dtype
        )
        model.to(device)

        def compute_metrics(eval_pred):
            logits, labels = eval_pred
            preds = np.argmax(logits, axis=-1)
            acc = accuracy_score(labels, preds)
            precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
            return {"accuracy": acc, "precision": precision, "recall": recall, "f1": f1}

        training_args = TrainingArguments(
            output_dir=f"./fold_{fold+1}_transformer",
            evaluation_strategy="epoch",
            save_strategy="epoch",
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            load_best_model_at_end=True,

            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,

            num_train_epochs=50,
            logging_dir=f"./logs/fold_{fold+1}",
            logging_strategy="epoch",
            report_to="none",
            save_total_limit=1,

            fp16=use_fp16,
            bf16=use_bf16,

            dataloader_pin_memory=True,
            dataloader_num_workers=2,
            
            # Adicionar para melhor visualização
            logging_steps=10,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=compute_metrics
        )

        # Adiciona callback que grava métricas de TREINO por época
        trainer.add_callback(
            TrainEvalCallback(trainer, train_dataset, suffix=suffix, early_stopping_patience=50)
        )

        print("Treinando modelo...")
        trainer.train()

        # Plota usando validation do trainer e train do CSV gerado pela callback
        plot_training_metrics(trainer, suffix=suffix)

        # Avaliações finais (predict)
        train_acc, val_acc, test_acc = calcular_acuracia(
            trainer, train_dataset, val_dataset, test_dataset, suffix=suffix
        )
        avaliar_modelo(trainer, test_dataset, suffix=suffix)

        resultados_folds.append({
            "fold": fold+1,
            "train_acc": train_acc,
            "val_acc": val_acc,
            "test_acc": test_acc
        })

    df_resultados = pd.DataFrame(resultados_folds)
    df_resultados.to_csv("resultados_kfold.csv", index=False, sep=";", encoding="utf-8-sig")
    print("\n" + "="*60)
    print("[INFO] Resultados salvos em resultados_kfold.csv")
    print("="*60)
    print(df_resultados)

# ================================================================================
# EXECUTAR
# ================================================================================
if __name__ == "__main__":
    MODEL_NAME = "distilbert-base-uncased"
    main()