from transformers import AutoTokenizer, AutoModel
import torch


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask


def getEmb(prompt):
    encoded_input = tokenizer(prompt, padding=True, truncation=True, max_length=24, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    return mean_pooling(model_output, encoded_input['attention_mask'])   


def getAns(inp):
    labels, signs = inp['labels'], inp['signs']
    start = getEmb(labels[0])
    for label, sign in zip(labels[1:], signs):
        label_emb = getEmb(label)
        start += label_emb if sign == '+' else -label_emb
    return tokenizer.decode(start)


tokenizer = AutoTokenizer.from_pretrained("sberbank-ai/sbert_large_nlu_ru")
model = AutoModel.from_pretrained("sberbank-ai/sbert_large_nlu_ru")
