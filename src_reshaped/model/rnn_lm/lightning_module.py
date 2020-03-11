import pytorch_lightning as pl
from test_tube import HyperOptArgumentParser
from collections import OrderedDict
import torch as t
import numpy as np
from src_reshaped.utils.optimizer import AdamW
from src_reshaped.model.rnn_lm.rnn_lm import ClassifierWithState, RNNLM
from src_reshaped.utils.vocab import Vocab


class LightningModel(pl.LightningModule):
    def __init__(self, hparams):
        super(LightningModel, self).__init__()
        self.hparams = hparams
        self.__build_model()
        self.lr = 0

    def __build_model(self):
        self.vocab = Vocab(self.hparams.vocab_path)
        self.rnn = RNNLM(
            self.vocab.vocab_size, self.hparams.n_layers, n_units=self.hparams.n_units, typ=self.hparams.typ,
            dropout_rate=self.hparams.dropout_rate)
        self.model = ClassifierWithState(self.rnn)

    def train_dataloader(self):

        return dataloader

    def val_dataloader(self):


        return dataloader

    def optimizer_step(self, epoch_nb, batch_nb, optimizer, optimizer_i, second_order_closure=None):
        lr = self.hparams.factor * (
                (self.hparams.model_size ** -0.5) * min(
            (self.global_step + 1) ** -0.5, (self.global_step + 1) * (self.hparams.warm_up_step ** -1.5))
        )
        self.lr = lr
        for pg in optimizer.param_groups:
            pg['lr'] = lr
        optimizer.step()
        optimizer.zero_grad()

    def configure_optimizers(self):
        optimizer = AdamW(self.parameters(), lr=self.hparams.lr, betas=(0.9, 0.999))
        # optimizer = Lookahead(optimizer)
        return optimizer

    @staticmethod
    def add_model_specific_args(parent_parser):
        parser = HyperOptArgumentParser(parents=[parent_parser])
        parser.add_argument('--num_freq_mask', default=2, type=int)
        parser.add_argument('--num_time_mask', default=2, type=int)
        parser.add_argument('--freq_mask_length', default=30, type=int)
        parser.add_argument('--time_mask_length', default=20, type=int)
        parser.add_argument('--feature_dim', default=480, type=int)
        parser.add_argument('--model_size', default=256, type=int)
        parser.add_argument('--feed_forward_size', default=2048, type=int)
        parser.add_argument('--hidden_size', default=64, type=int)
        parser.add_argument('--dropout', default=0.1, type=float)
        parser.add_argument('--num_head', default=4, type=int)
        parser.add_argument('--num_encoder_layer', default=6, type=int)
        parser.add_argument('--num_decoder_layer', default=12, type=int)
        parser.add_argument('--vocab_path', default='testing_vocab.model', type=str)
        parser.add_argument('--max_feature_length', default=1024, type=int)
        parser.add_argument('--max_token_length', default=100, type=int)
        parser.add_argument('--share_weight', default=True, type=bool)
        parser.add_argument('--loss_lambda', default=0.3, type=float)
        parser.add_argument('--smoothing', default=0.1, type=float)

        parser.add_argument('--lr', default=3e-4, type=float)
        parser.add_argument('--warm_up_step', default=25000, type=int)
        parser.add_argument('--factor', default=1, type=int)
        parser.add_argument('--enable_spec_augment', default=True, type=bool)

        parser.add_argument('--train_batch_size', default=32, type=int)
        parser.add_argument('--train_loader_num_workers', default=16, type=int)
        parser.add_argument('--val_batch_size', default=32, type=int)
        parser.add_argument('--val_loader_num_workers', default=16, type=int)

        return parser
