/*
 * Copyright 2013 Free Software Foundation, Inc.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
#define lpwan_API

%include <gnuradio.i>

%include "lpwan_swig_doc.i"

%{
#include "lpwan/dsss_interleaver_bb.h"
#include "lpwan/dsss_codes.h"
#include "lpwan/dsss_diff_coding_bb.h"
#include "lpwan/dsss_spreading_bb.h"
#include "lpwan/dsss_deinterleaver_ff.h"
#include "lpwan/dsss_diff_decoding_ff.h"
#include "lpwan/dsss_despread_simple_cc.h"
#include "lpwan/dsss_preamble_demod_cc.h"
#include "lpwan/conj_multiply_delay_ccc.h"
#include "lpwan/dsss_preamble_detector_cc.h"
#include "lpwan/dsss_despread_cc.h"
#include "lpwan/dsss_normalize_ff.h"
#include "lpwan/dsss_snr_estimator.h"
#include "lpwan/dsss_fragmentation.h"
#include "lpwan/dsss_filter_crc_packets.h"
#include "lpwan/fsk_lecim_interleaver.h"
#include "lpwan/fsk_lecim_deinterleaver.h"
#include "lpwan/fsk_lecim_phr_pdu_demux.h"
#include "lpwan/fsk_lecim_corr_est_cc.h"
#include "lpwan/fsk_lecim_phr_parser.h"
#include "lpwan/fsk_lecim_normalize_fcc.h"
#include "lpwan/fsk_lecim_synchronizer_cc.h"
%}

%include "lpwan/dsss_interleaver_bb.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, dsss_interleaver_bb);
%include "lpwan/dsss_codes.h"
%include "lpwan/dsss_diff_coding_bb.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, dsss_diff_coding_bb);
%include "lpwan/dsss_spreading_bb.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, dsss_spreading_bb);
%include "lpwan/dsss_deinterleaver_ff.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, dsss_deinterleaver_ff);
%include "lpwan/dsss_diff_decoding_ff.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, dsss_diff_decoding_ff);
%include "lpwan/dsss_despread_simple_cc.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, dsss_despread_simple_cc);
%include "lpwan/dsss_preamble_demod_cc.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, dsss_preamble_demod_cc);
%include "lpwan/conj_multiply_delay_ccc.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, conj_multiply_delay_ccc);
%include "lpwan/dsss_preamble_detector_cc.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, dsss_preamble_detector_cc);
%include "lpwan/dsss_despread_cc.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, dsss_despread_cc);
%include "lpwan/dsss_normalize_ff.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, dsss_normalize_ff);
%include "lpwan/dsss_snr_estimator.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, dsss_snr_estimator);
%include "lpwan/dsss_fragmentation.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, dsss_fragmentation);
%include "lpwan/dsss_filter_crc_packets.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, dsss_filter_crc_packets);

%include "lpwan/fsk_lecim_interleaver.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, fsk_lecim_interleaver);
%include "lpwan/fsk_lecim_deinterleaver.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, fsk_lecim_deinterleaver);
%include "lpwan/fsk_lecim_phr_pdu_demux.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, fsk_lecim_phr_pdu_demux);
%include "lpwan/fsk_lecim_corr_est_cc.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, fsk_lecim_corr_est_cc);
%include "lpwan/fsk_lecim_phr_parser.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, fsk_lecim_phr_parser);

%include "lpwan/fsk_lecim_normalize_fcc.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, fsk_lecim_normalize_fcc);

%include "lpwan/fsk_lecim_synchronizer_cc.h"
GR_SWIG_BLOCK_MAGIC2(lpwan, fsk_lecim_synchronizer_cc);
