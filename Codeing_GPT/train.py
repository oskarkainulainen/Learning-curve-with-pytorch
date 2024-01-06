

# Read the set to inspect it
with open('input.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print ("length of dataset in charachters:", len(text))

# To see what characters are on th dataset
chars = sorted(list(set(text)))
vocab_size = len(chars)
print(''.join(chars))
print(vocab_size)

# Create a mapping from characters ti integrs
stoi = {ch:i for i, ch in enumerate(chars) }
itois = {i:ch for i, ch in enumerate(chars) }
encode = lambda s: [stoi[c] for c in s] # Encoder: takes a string, output a list of integers
decode = lambda l: ''.join([itois[i] for i in l]) # Decoder: take a list of integers, output a string

print(encode("hii there"))
print(decode(encode("hii there")))

# Encoding the entire dataset and storeing it into torch.Tensor
import torch # useing Pytorch: https://pytorch.org
data = torch.tensor(encode(text), dtype=torch.long)
print(data.shape, data.dtype)
print(data[:1000])

# Splitting the data to train and validations sets
n = int(0.9*len(data)) # first 90% train rest val
train_data = data[:n]
val_data = data[n:]

block_size = 8
train_data[:block_size+1]

x = train_data[:block_size]
y = train_data[1:block_size+1]
for t in range(block_size):
    context = x[:t+1]
    target = y[t]
    print(f"when input is {context} the target: {target} ")

torch.manual_seed(1337)
batch_size = 4 # How many independent sequences will we process in parallel?
block_size = 8 # What is the maximum context lenght for predictions?

def get_batch(split):
    # generate a small batch of data of inputs x and targets y
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    return x, y

xb, yb = get_batch('train')
print('inputs:')
print(xb.shape)
print(xb)
print('targets:')
print(yb.shape)
print(yb)

print('------')

for b in range(batch_size): # batch dimension
    for t in range(block_size): # time dimension
        context = xb[b, :t+1]
        target = yb[b,t]
        print(f"when input is {context.tolist()} the target: {target}")


import torch 
import torch.nn as nn
from torch.nn import functional as F 
torch.manual_seed(1337)

class BigramLanguageModel(nn.Module):

    def __init__(self, vocab_size):
        super().__init__()
        # each token directly reads off the logits for the next token from a lookup table
        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)

        def foward(self, idx, targets=None):

            # idx and targets are bot (B, T) tensor of intergers
            logits = self.token_embedding_table(idx) # (B,T,C)

            if targets is None:
                lose = None
            else:
                B, T, C = logits.shape
                logits = logits.view(B*T, C)
                targets = targets.view(B*T)
                loss = F.cross_entropy(logits, targets)
           
            return logits, loss
        
        def generate(self, idx, max_new_tokens):
            # idx is (B, T) array of indices in the current contexct
            for _ in range(max_new_tokens):
                # get the predictions
                logits, loss = self(idx)
                #focus only on the last time setup
                logits = logits[:, -1, :] # becomes (B, C)
                # apply softmax to get probabilities
                probs = F.softmax(logits, dim=-1) #(B,C)
                # sample from th distribution
                idx_next = torch.multinomial(probs, num_smaple=1) # (B, 1)
                # append sampled index to the running sequnce
                idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)
            return idx
        
m = BigramLanguageModel(vocab_size)
logits, loss = m(xb, yb)
print(logits.shape)
print(loss)

print(decode(m.generate(idx = torch.zeros((1, 1), dtype=torch.long), max_new_tokens=100)[0].tolist()))