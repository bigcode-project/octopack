import torch
for idx in ["00001", "00002", "00003", "00004", "00005", "00006", "00007"]:
    x = torch.load(f"/gpfsscratch/rech/ajs/commun/Bigcode-large-megatron_conv/base/shard2/pytorch_model-{idx}-of-00007.bin")
    y = torch.load(f"/gpfsscratch/rech/ajs/commun/starcoderbase/pytorch_model-{idx}-of-00007.bin")
    assert x.keys() == y.keys()
    for k in x.keys():
        if not((x[k] == y[k]).all()):
            print(k)
            print(x[k].shape)
            print(y[k].shape)
            break