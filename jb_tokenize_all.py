from pathlib import Path
import jsonlines

import jb_tokenizer

for p in Path("data/ptt-gossiping").glob("*.jsonl"):
    print(p)
    output_filename = str(p).replace("data", "data-jb-tokenized")
    with jsonlines.open(f'{output_filename}.jsonl', mode='w') as writer:
        for line in jb_tokenizer.tokenize_one_jsonl(p):
            writer.write(line)
