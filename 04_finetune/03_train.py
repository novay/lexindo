import mlx_lm
from datasets import load_dataset
from mlx_lm import lora
from mlx_lm.tuner import Trainer

BASE_MODEL_PATH = "./models/llama-3.2-1b-instruct"
DATA_PATH = "./data/regulation_qa.jsonl"
OUTPUT_DIR = "./models/lexindo-1b-kukarkab"

dataset = load_dataset("json", data_files=DATA_PATH, split="train")

trainer = Trainer(
    model=BASE_MODEL_PATH,
    train_dataset=dataset,
    lora_config=lora.LoRAConfig(r=16, alpha=32, dropout=0.05),
    batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    num_epochs=3,
    max_seq_length=2048,
    output_dir=OUTPUT_DIR,
)

trainer.train()
trainer.save_pretrained(OUTPUT_DIR)
