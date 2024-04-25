import os
from glob import glob
from dataclasses import dataclass, field


@dataclass
class ClassificationTrainArguments:

    pretrained_model_name: str = field(
        default="beomi/kcbert-base",
        metadata={"help": "pretrained model name"}
    )
    downstream_task_name: str = field(
        default="document-classification",
        metadata={"help": "The name of the downstream data."}
    )
    downstream_corpus_name: str = field(
        default=None,
        metadata={"help": "The name of the downstream data."}
    )
    downstream_corpus_root_dir: str = field(
        default="/content/Korpora",
        metadata={"help": "The root directory of the downstream data."}
    )
    downstream_model_dir: str = field(
        default=None,
        metadata={"help": "The output model dir."}
    )
    max_seq_length: int = field(
        default=128,
        metadata={
            "help": "The maximum total input sequence length after tokenization. Sequences longer "
                    "than this will be truncated, sequences shorter will be padded."
        }
    )
    save_top_k: int = field(
        default=1,
        metadata={"help": "save top k model checkpoints."}
    )
    monitor: str = field(
        default="min val_loss",
        metadata={"help": "monitor condition (save top k)"}
    )
    seed: int = field(
        default=None,
        metadata={"help": "random seed."}
    )
    overwrite_cache: bool = field(
        default=False,
        metadata={"help": "Overwrite the cached training and evaluation sets"}
    )
    force_download: bool = field(
        default=False,
        metadata={"help": "force to download downstream data and pretrained models."}
    )
    test_mode: bool = field(
        default=False,
        metadata={"help": "Test Mode enables `fast_dev_run`"}
    )
    learning_rate: float = field(
        default=5e-5,
        metadata={"help": "learning rate"}
    )
    epochs: int = field(
        default=3,
        metadata={"help": "max epochs"}
    )
    batch_size: int = field(
        default=32,
        metadata={"help": "batch size. if 0, Let PyTorch Lightening find the best batch size"}
    )
    cpu_workers: int = field(
        default=os.cpu_count(),
        metadata={"help": "number of CPU workers"}
    )
    fp16: bool = field(
        default=False,
        metadata={"help": "Enable train on FP16"}
    )
    tpu_cores: int = field(
        default=0,
        metadata={"help": "Enable TPU with 1 core or 8 cores"}
    )



@dataclass
class ClassificationDeployArguments:

    def __init__(
            self,
            pretrained_model_name=None,
            downstream_model_dir=None,
            downstream_model_checkpoint_fpath=None,
            max_seq_length=128,
    ):
        self.pretrained_model_name = pretrained_model_name
        self.max_seq_length = max_seq_length
        self.downstream_model_dir=downstream_model_dir,
        self.downstream_model_checkpoint_fpath = downstream_model_checkpoint_fpath
        # 없어도됨
        print(f"model is ready")
