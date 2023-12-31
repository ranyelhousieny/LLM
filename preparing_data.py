# -*- coding: utf-8 -*-
"""preparing-data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/ranyelhousieny/e75e53936eec8c03a6f9ee0a07958384/preparing-data.ipynb
"""

!pip install datasets

import datasets
from pprint import pprint

lamini_doc = datasets.load_dataset('kotzeje/lamini_docs.jsonl', split='train')

pprint(lamini_doc)

import pandas as pd


lamini_df = pd.DataFrame(lamini_doc)

lamini_df.head()

examples = lamini_df.to_dict()

pprint(f"Question: {examples['question'][0]}")

print()

pprint(f"answer: {examples['answer'][0]}")

prompt_template = """### Question:
{question}

### Answer:
{answer}"""


question = examples["question"][0]
answer = examples['answer'][0]

text = prompt_template.format(question=question, answer=answer)

pprint(text)

prompt_template = """### Question:
{question}

### Answer:"""

num_examples = len(examples["question"])
finetuning_dataset = []
for i in range(num_examples):
  question = examples["question"][i]
  answer = examples["answer"][i]
  text_with_prompt_template = prompt_template.format(question=question)
  finetuning_dataset.append({"question": text_with_prompt_template, "answer": answer})


print("One datapoint in the finetuning dataset:")
pprint(finetuning_dataset[0])

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-70m")

text = finetuning_dataset[0]["question"] + finetuning_dataset[0]["answer"]

pprint(text)

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-70m")

tokenizer.pad_token = tokenizer.eos_token


tokenized_inputs = tokenizer(
    text,
    return_tensors="np",
    padding=True
)

pprint(tokenized_inputs)

pprint(tokenized_inputs)

max_length = 2048
max_length = min(
    tokenized_inputs["input_ids"].shape[1],
    max_length,
)

print(max_length)

def tokenize_function(examples):
    if "question" in examples and "answer" in examples:
      text = examples["question"][0] + examples["answer"][0]
    elif "input" in examples and "output" in examples:
      text = examples["input"][0] + examples["output"][0]
    else:
      text = examples["text"][0]

    tokenizer.pad_token = tokenizer.eos_token
    tokenized_inputs = tokenizer(
        text,
        return_tensors="np",
        padding=True,
    )

    max_length = min(
        tokenized_inputs["input_ids"].shape[1],
        2048
    )
    tokenizer.truncation_side = "left"
    tokenized_inputs = tokenizer(
        text,
        return_tensors="np",
        truncation=True,
        max_length=max_length
    )

    return tokenized_inputs

type(finetuning_dataset)

print

# Restructure data into a dictionary of lists
finetuning_data_dict = {key: [dic[key] for dic in finetuning_dataset] for key in finetuning_dataset[0]}

# Create the Hugging Face Dataset
training_dataset = datasets.Dataset.from_dict(finetuning_data_dict)

print(training_dataset[0])

train_test_split = dataset.train_test_split(test_size=0.2)
train_dataset = dataset['train']

type(train_dataset)

pprint(train_dataset[0])

# Restructure data into a dictionary of lists
finetuning_data_dict = {key: [dic[key] for dic in finetuning_dataset] for key in finetuning_dataset[0]}

# Create the Hugging Face Dataset
training_dataset = datasets.Dataset.from_dict(finetuning_data_dict)

tokenized_dataset = training_dataset.map(
    tokenize_function,
    batched=True,
    batch_size=1,
    drop_last_batch=True
)

print(tokenized_dataset)

pprint(tokenized_dataset['question'][0])

tokenized_dataset = tokenized_dataset.add_column("labels", tokenized_dataset["input_ids"])

print(tokenized_dataset)

pprint(tokenized_dataset['labels'][0])

split_dataset = tokenized_dataset.train_test_split(test_size=0.1, shuffle=True, seed=123)
print(split_dataset)

finetuning_dataset_path2 = "lamini/lamini_docs"
finetuning_dataset2 = datasets.load_dataset(finetuning_dataset_path2, split='train')
pprint(finetuning_dataset2)

pprint(finetuning_dataset2['question'][0])

!pip install huggingface_hub
#

!huggingface-cli login
# split_dataset.push_to_hub(dataset_path_hf)

split_dataset.push_to_hub(tokenized_dataset)

type(tokenized_dataset)

tokenized_dataset.push_to_hub("relhousieny/tokenized_lamini_template")

rany_dataset = datasets.load_dataset("relhousieny/tokenized_lamini_template")

print(rany_dataset)

