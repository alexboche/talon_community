from talon.voice import Context

from . import config
from .text import shrink

vocab_alternate = config.load_config_json("vocab_alternate.json", dict)

vocab_alternate.update({f"shrink {k}": v for k, v in shrink.shrink_map.items()})
vocab_non_spoken = config.load_config_json("vocab.json", dict)
print(vocab_non_spoken)
ctx = Context("vocab")
# print(config.load_config_json("vocab.json", dict))
# for k in config.load_config_json("vocab.json", dict):
    # print(k)
    # print(config.load_config_json("vocab.json", dict)[k])
    # print(config.load_config_json("vocab.json", dict))

regular_vocab_list = [word for topic in vocab_non_spoken for word in vocab_non_spoken[topic]]
print(regular_vocab_list)
ctx.vocab = regular_vocab_list + list(vocab_alternate.keys())
# ctx.vocab = config.load_config_json("vocab.json", list) + list(vocab_alternate.keys())
ctx.vocab_remove = config.load_config_json("vocab_remove.json", list)
