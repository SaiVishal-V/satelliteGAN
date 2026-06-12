#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import DINCAE


#filename = "/path/to/file.nc"
#varname = "SST"
#outdir = "/path/to/output/dir"

filename = r"E:\IR_nc_files_fixed_v2\IR_wind_2023_Full_v2_DINCAE_ready.nc"
varname = "wind_speed"
outdir = r"E:\dincaep\Output"


DINCAE.reconstruct_gridded_nc(
	filename,
	varname,
	outdir,
	epochs=600,
	batch_size=30,
	learning_rate=2e-5,
	ntime_win=5,
	learning_rate_decay_epoch=160,
	dropout_rate_train=0.08,
	jitter_std=0.01,
	regularization_L2_beta=1e-7,
	nepoch_keep_missing=20,
	validate_each=1,
	early_stopping_patience=40,
	early_stopping_min_delta=1e-4,
	save_best_model=True,
	save_best_output=True,
	best_output_filename="data-best.nc",
	restore_latest_checkpoint=True,
	save_each=0,
	save_model_each=100,
	iseed=42,
)