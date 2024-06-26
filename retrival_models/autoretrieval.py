from collections import OrderedDict
from .bm25 import build_bm25_fn
from .random_selection import build_random_fn
from .mixed import build_mix_fn

IR_METHOD_MAPPING = OrderedDict(
    [
        ('BM25', build_bm25_fn),
        ('Random', build_random_fn),
        ('Full_Random', build_random_fn),
        ('Mixed', build_mix_fn),
        ('RanBM25', build_bm25_fn)
    ]
)

class AutoRetrieval():

    @classmethod
    def get(self, retrieval_id, config: dict =None):
        assert('task_name' in config.keys())
        if retrieval_id in IR_METHOD_MAPPING:
            return IR_METHOD_MAPPING[retrieval_id](config)
        else:
            return ValueError(
                "The retrieval method does not exist in the produced list."
            )