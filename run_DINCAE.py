#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import DINCAE

filename = "/path/to/file.nc"
varname = "wind_speed" #Sample variable name
outdir = "/path/to/output/dir"


DINCAE.reconstruct_gridded_nc(
	filename,
	varname,
	outdir,
	epochs=400,
	batch_size=30,
	learning_rate=2e-5,
	learning_rate_decay_epoch=80,
	dropout_rate_train=0.08,
	jitter_std=0.01,
	nepoch_keep_missing=20,
	save_each=25,
	save_model_each=25,
	iseed=42,
)
