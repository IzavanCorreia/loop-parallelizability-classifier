"""DistilBERT (distilbert-base-uncased) fine-tuned for binary loop classification.

Source code goes in as plain text through the model's subword tokenizer (max_len 256; every sample
of this study is shorter). AdamW, lr 2e-5, weight decay 0.01, linear schedule with 10% warm-up,
batch 16, mixed precision, at most 10 epochs with early stopping on the validation loss
(patience 3); the weights of the epoch with the lowest validation loss are kept. Validation and test
scores of every epoch are stored for the checkpoint-selection analysis.
"""

import time

import numpy as np
import torch
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

MODEL_NAME = "distilbert-base-uncased"
MAX_LEN = 256
BATCH = 16
LR = 2e-5
MAX_EPOCHS = 10
PATIENCE = 3

_tokenizer = None


def tokenizer():
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    return _tokenizer


def _loader(codes, labels, shuffle, seed=0):
    enc = tokenizer()(list(codes), truncation=True, max_length=MAX_LEN)
    data = [{"input_ids": ids, "attention_mask": m, "labels": int(y)}
            for ids, m, y in zip(enc["input_ids"], enc["attention_mask"], labels)]

    def collate(batch):
        out = tokenizer().pad([{k: b[k] for k in ("input_ids", "attention_mask")} for b in batch],
                              return_tensors="pt")
        out["labels"] = torch.tensor([b["labels"] for b in batch])
        return out

    g = torch.Generator()
    g.manual_seed(seed)
    return DataLoader(data, batch_size=BATCH, shuffle=shuffle, collate_fn=collate, generator=g)


@torch.no_grad()
def _predict(model, loader, device):
    model.eval()
    probs, losses, n = [], 0.0, 0
    for b in loader:
        b = {k: v.to(device) for k, v in b.items()}
        with torch.autocast("cuda", dtype=torch.float16, enabled=device == "cuda"):
            out = model(**b)
        logits = out.logits.float()
        losses += torch.nn.functional.cross_entropy(logits, b["labels"], reduction="sum").item()
        n += len(b["labels"])
        probs.append(torch.softmax(logits, -1)[:, 1].cpu().numpy())
    return np.concatenate(probs), losses / n


def run(codes_tr, y_tr, codes_va, y_va, codes_te, seed):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(seed)
    t0 = time.time()
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2).to(device)
    dl_tr = _loader(codes_tr, y_tr, True, seed)
    dl_va = _loader(codes_va, y_va, False)
    dl_te = _loader(codes_te, np.zeros(len(codes_te), dtype=int), False)
    opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.01)
    total = MAX_EPOCHS * len(dl_tr)
    sched = get_linear_schedule_with_warmup(opt, int(0.1 * total), total)
    scaler = torch.amp.GradScaler(enabled=device == "cuda")
    best, best_state, best_epoch, wait = float("inf"), None, 0, 0
    ep_val_scores, ep_test_scores, ep_val_loss, ep_train_loss = [], [], [], []
    for epoch in range(MAX_EPOCHS):
        model.train()
        tl, tn = 0.0, 0
        for b in dl_tr:
            b = {k: v.to(device) for k, v in b.items()}
            opt.zero_grad()
            with torch.autocast("cuda", dtype=torch.float16, enabled=device == "cuda"):
                loss = model(**b).loss
            scaler.scale(loss).backward()
            scaler.step(opt)
            scaler.update()
            sched.step()
            tl += loss.item() * len(b["labels"])
            tn += len(b["labels"])
        s_va, vloss = _predict(model, dl_va, device)
        s_te, _ = _predict(model, dl_te, device)
        ep_val_scores.append(s_va)
        ep_test_scores.append(s_te)
        ep_val_loss.append(vloss)
        ep_train_loss.append(tl / tn)
        if vloss < best - 1e-6:
            best, best_epoch, wait = vloss, epoch, 0
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
        else:
            wait += 1
            if wait >= PATIENCE:
                break
    train_time = time.time() - t0
    model.load_state_dict(best_state)
    t1 = time.time()
    s_te, _ = _predict(model, dl_te, device)
    infer_time = time.time() - t1
    s_va = ep_val_scores[best_epoch]
    info = {"best_epoch": best_epoch + 1, "epochs_run": epoch + 1, "best_val_loss": best,
            "val_loss_history": ep_val_loss, "train_loss_history": ep_train_loss,
            "train_time_s": train_time, "infer_time_s": infer_time,
            "n_params": sum(p.numel() for p in model.parameters()), "threshold": 0.5,
            "peak_vram_gb": torch.cuda.max_memory_allocated() / 2 ** 30 if device == "cuda" else 0.0}
    extra = {"epoch_val_scores": np.stack(ep_val_scores), "epoch_test_scores": np.stack(ep_test_scores),
             "epoch_val_loss": np.array(ep_val_loss)}
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return s_va, s_te, info, extra
