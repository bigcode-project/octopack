INPUT=commitpack_cf.jsonl # merge datasets jsonl from commitpack-subset-cf
NAME=commitpack_cf # you want data name
TOKENIZER_FILE=starcoder-tokenizer/tokenizer.json
VOCAD=starcoder-tokenizer/vocab.json

python tools/preprocess_data.py \
    --input $INPUT \
    --output-prefix $NAME \
    --dataset-impl mmap \
    --tokenizer-type TokenizerFromFile  \
    --tokenizer-file $TOKENIZER_FILE \
    --workers 30 \
    --chunk-size 1000