from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoModel
from transformers.modeling_outputs import BaseModelOutput
import torch


enc_tokenizer = AutoTokenizer.from_pretrained('cointegrated/LaBSE-en-ru')
encoder = AutoModel.from_pretrained('cointegrated/LaBSE-en-ru')

dec_tokenizer = AutoTokenizer.from_pretrained('cointegrated/rut5-base-labse-decoder')
decoder = AutoModelForSeq2SeqLM.from_pretrained('cointegrated/rut5-base-labse-decoder')

def encode(texts):
    encoded_input = enc_tokenizer(texts, padding=True, truncation=True, max_length=512, return_tensors='pt')
    with torch.no_grad():
        model_output = encoder(**encoded_input.to(encoder.device))
        embeddings = model_output.pooler_output
        embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings

def decode(embeddings, max_length=5, repetition_penalty=3.0, num_beams=3, **kwargs):
    out = decoder.generate(
        encoder_outputs=BaseModelOutput(last_hidden_state=embeddings.unsqueeze(1)), 
        max_length=max_length, 
        num_beams=num_beams,
        repetition_penalty=repetition_penalty,
    )
    return ' '.join([dec_tokenizer.decode(tokens, skip_special_tokens=True) for tokens in out])


def getAns(inp):
    labels, signs = inp['labels'], inp['signs']
    start = encode(labels[0])
    for label, sign in zip(labels[1:], signs):
        label_emb = encode(label)
        start += label_emb if sign == '+' else -1 * label_emb
    return decode(start)


backbone = "cointegrated/rut5-base-labse-decoder"
tokenizer = AutoTokenizer.from_pretrained(backbone)
model = AutoModel.from_pretrained(backbone)
decoder = AutoModelForSeq2SeqLM.from_pretrained(backbone)