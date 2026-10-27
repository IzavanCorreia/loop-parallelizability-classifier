"""Baselines of the Array study, re-run under the protocol of this study.

Representation (Array pipeline): Python ``tokenize`` tokens -> integer IDs -> zero padding ->
standardisation -> PCA keeping 100% of the variance. Vocabulary, padding width, scaler and PCA
are fitted on the training portion of each fold only.

Models (architectures and optimiser settings of the Array code):
  lr    LogisticRegression(max_iter=1000), on standardised PCA features
  svm   SVC(kernel="linear"), on standardised PCA features
  dnn   Linear 128-64-32-1, BatchNorm, ReLU, dropout 0.5, sigmoid; Adam lr 1e-3, batch 4, BCE
  cnn   Conv1d 1->2->4 (k=3), BatchNorm, ReLU, dropout 0.6, Linear 4L->4->1, sigmoid; same optimiser
DNN/CNN train for at most 1000 epochs with early stopping on the validation loss (patience 50) and
keep the weights of the best epoch.

Additional lexical reference (not part of the Array study):
  ngram TF-IDF of Python-token 1- to 3-grams (tokens seen in at least 2 training samples, sublinear tf)
        + LogisticRegression(max_iter=2000); default settings, no tuning
"""

import io
import time
import tokenize as pytok

import numpy as np
import torch
import torch.nn as nn
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def py_tokens(code):
    out = []
    try:
        for tok in pytok.generate_tokens(io.StringIO(code).readline):
            if tok.string.strip():
                out.append(tok.string.strip())
    except (pytok.TokenError, IndentationError, SyntaxError):
        out = code.split()
    return out


class ArrayPipeline:
    def fit(self, codes):
        toks = [py_tokens(c) for c in codes]
        self.vocab = {}
        for t in toks:
            for s in t:
                self.vocab.setdefault(s, len(self.vocab) + 1)
        self.width = max(len(t) for t in toks)
        X = self._ids(toks)
        self.scaler = StandardScaler().fit(X)
        self.pca = PCA(n_components=None, svd_solver="full").fit(self.scaler.transform(X))
        return self

    def _ids(self, toks):
        X = np.zeros((len(toks), self.width), dtype=np.float64)
        for i, t in enumerate(toks):
            ids = [self.vocab.get(s, 0) for s in t][: self.width]
            X[i, : len(ids)] = ids
        return X

    def transform(self, codes):
        X = self._ids([py_tokens(c) for c in codes])
        return self.pca.transform(self.scaler.transform(X))


class DNN(nn.Module):
    def __init__(self, n_in):
        super().__init__()
        self.fc1, self.bn1 = nn.Linear(n_in, 128), nn.BatchNorm1d(128)
        self.fc2, self.bn2 = nn.Linear(128, 64), nn.BatchNorm1d(64)
        self.fc3, self.bn3 = nn.Linear(64, 32), nn.BatchNorm1d(32)
        self.fc4 = nn.Linear(32, 1)
        self.drop = nn.Dropout(0.5)

    def forward(self, x):
        x = self.drop(torch.relu(self.bn1(self.fc1(x))))
        x = self.drop(torch.relu(self.bn2(self.fc2(x))))
        x = self.drop(torch.relu(self.bn3(self.fc3(x))))
        return torch.sigmoid(self.fc4(x)).squeeze(1)


class CNN(nn.Module):
    def __init__(self, n_in):
        super().__init__()
        self.conv1, self.bn1 = nn.Conv1d(1, 2, 3, padding=1), nn.BatchNorm1d(2)
        self.conv2, self.bn2 = nn.Conv1d(2, 4, 3, padding=1), nn.BatchNorm1d(4)
        self.drop = nn.Dropout(0.6)
        self.fc1, self.fc2 = nn.Linear(4 * n_in, 4), nn.Linear(4, 1)

    def forward(self, x):
        x = x.unsqueeze(1)
        x = self.drop(torch.relu(self.bn1(self.conv1(x))))
        x = self.drop(torch.relu(self.bn2(self.conv2(x))))
        x = torch.relu(self.fc1(x.flatten(1)))
        return torch.sigmoid(self.fc2(x)).squeeze(1)


def _train_torch(model_cls, Xtr, ytr, Xva, yva, max_epochs=1000, patience=50, batch=4, lr=1e-3):
    device = "cpu"          # tiny networks with batch 4 run faster on the CPU than on the GPU
    Xtr_t, ytr_t = torch.tensor(Xtr, dtype=torch.float32), torch.tensor(ytr, dtype=torch.float32)
    Xva_t, yva_t = torch.tensor(Xva, dtype=torch.float32), torch.tensor(yva, dtype=torch.float32)
    model = model_cls(Xtr.shape[1]).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.BCELoss()
    best, best_state, best_epoch, wait = float("inf"), None, 0, 0
    n = len(Xtr_t)
    history = []
    for epoch in range(max_epochs):
        model.train()
        perm = torch.randperm(n)
        for s in range(0, n, batch):
            b = perm[s:s + batch]
            if len(b) < 2:          # BatchNorm needs more than one sample
                continue
            opt.zero_grad()
            loss = loss_fn(model(Xtr_t[b]), ytr_t[b])
            loss.backward()
            opt.step()
        model.eval()
        with torch.no_grad():
            vloss = loss_fn(model(Xva_t).clamp(1e-7, 1 - 1e-7), yva_t).item()
        history.append(vloss)
        if vloss < best - 1e-6:
            best, best_epoch, wait = vloss, epoch, 0
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
        else:
            wait += 1
            if wait >= patience:
                break
    model.load_state_dict(best_state)
    model.eval()
    return model, {"best_epoch": best_epoch + 1, "epochs_run": epoch + 1, "best_val_loss": best,
                   "val_loss_history": history}


def run_ngram(codes_tr, y_tr, codes_va, codes_te, seed):
    """Bag of Python-token n-grams with logistic regression, fitted on the training portion only."""
    t0 = time.time()
    vec = TfidfVectorizer(tokenizer=py_tokens, lowercase=False, token_pattern=None, ngram_range=(1, 3),
                          min_df=2, sublinear_tf=True)
    Xtr = vec.fit_transform(codes_tr)
    m = LogisticRegression(max_iter=2000, random_state=seed).fit(Xtr, y_tr)
    info = {"n_features": int(Xtr.shape[1]), "train_time_s": time.time() - t0}
    t1 = time.time()
    s_va, s_te = m.predict_proba(vec.transform(codes_va))[:, 1], m.predict_proba(vec.transform(codes_te))[:, 1]
    info["infer_time_s"] = time.time() - t1
    info["threshold"] = 0.5
    return s_va, s_te, info


def run(model_name, codes_tr, y_tr, codes_va, y_va, codes_te, seed):
    if model_name == "ngram":
        return run_ngram(codes_tr, y_tr, codes_va, codes_te, seed)
    t0 = time.time()
    pipe = ArrayPipeline().fit(codes_tr)
    Xtr, Xva, Xte = pipe.transform(codes_tr), pipe.transform(codes_va), pipe.transform(codes_te)
    info = {"n_features": int(Xtr.shape[1])}
    if model_name in ("lr", "svm"):
        sc = StandardScaler().fit(Xtr)
        if model_name == "lr":
            m = LogisticRegression(max_iter=1000, random_state=seed).fit(sc.transform(Xtr), y_tr)
            score = lambda X: m.predict_proba(sc.transform(X))[:, 1]
        else:
            m = SVC(kernel="linear", random_state=seed).fit(sc.transform(Xtr), y_tr)
            score = lambda X: m.decision_function(sc.transform(X))        # > 0 means Parallelizable
        info["train_time_s"] = time.time() - t0
        t1 = time.time()
        s_va, s_te = score(Xva), score(Xte)
        info["infer_time_s"] = time.time() - t1
        info["threshold"] = 0.5 if model_name == "lr" else 0.0
        return s_va, s_te, info
    torch.manual_seed(seed)
    torch.set_num_threads(1)          # folds run in parallel processes
    model, hist = _train_torch(DNN if model_name == "dnn" else CNN, Xtr, y_tr, Xva, y_va)
    info.update(hist)
    info["train_time_s"] = time.time() - t0
    info["n_params"] = sum(p.numel() for p in model.parameters())
    t1 = time.time()
    with torch.no_grad():
        s_va = model(torch.tensor(Xva, dtype=torch.float32)).numpy()
        s_te = model(torch.tensor(Xte, dtype=torch.float32)).numpy()
    info["infer_time_s"] = time.time() - t1
    info["threshold"] = 0.5
    return s_va, s_te, info
