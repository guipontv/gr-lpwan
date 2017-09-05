#
# Copyright 2013 Free Software Foundation, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#####################################################################
# Setup python install
#####################################################################
include(GrPython)
if(NOT PYTHONINTERP_FOUND)
    return()
endif()

list(APPEND python_sources
    __init__.py
    dsss_const.py
    dsss_phy.py
    dsss_mod.py
    fsk_lecim_const.py
    fsk_lecim_phy.py
)
GR_PYTHON_INSTALL(
    FILES ${python_sources}
    dsss_preamble_search_cc.py
    message_counter.py
    fsk_lecim_modulator_fc.py
    fsk_lecim_spreading_bb.py
    fsk_lecim_despreading_bb.py
    fsk_lecim_whitening_bb.py
    fsk_lecim_demodulator_cb.py
    fsk_lecim_zero_depadding_bb.py
    fsk_lecim_freq_offset_est_cc.py
    DESTINATION ${GR_PYTHON_DIR}/lpwan
    COMPONENT "lpwan_python"
)

#####################################################################
# Handle the unit tests
#####################################################################
include(GrTest)

set(GR_TEST_TARGET_DEPS gnuradio-lpwan)
set(GR_TEST_PYTHON_DIRS ${CMAKE_BINARY_DIR}/swig)
GR_ADD_TEST(qa_dsss_interleaver_bb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dsss_interleaver_bb.py)
GR_ADD_TEST(qa_dsss_diff_coding_bb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dsss_diff_coding_bb.py)
GR_ADD_TEST(qa_dsss_spreading_bb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dsss_spreading_bb.py)
GR_ADD_TEST(qa_dsss_deinterleaver_ff ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dsss_deinterleaver_ff.py)
GR_ADD_TEST(qa_dsss_diff_decoding_ff ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dsss_diff_decoding_ff.py)
GR_ADD_TEST(qa_dsss_despread_simple_cc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dsss_despread_simple_cc.py)
GR_ADD_TEST(qa_dsss_preamble_search_cc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dsss_preamble_search_cc.py)
GR_ADD_TEST(qa_dsss_preamble_demod_cc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dsss_preamble_demod_cc.py)
GR_ADD_TEST(qa_conj_multiply_delay_ccc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_conj_multiply_delay_ccc.py)
GR_ADD_TEST(qa_dsss_preamble_detector_cc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dsss_preamble_detector_cc.py)
GR_ADD_TEST(qa_dsss_despread_cc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dsss_despread_cc.py)
GR_ADD_TEST(qa_dsss_normalize_ff ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dsss_normalize_ff.py)
GR_ADD_TEST(qa_dsss_fragmentation ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dsss_fragmentation.py)
GR_ADD_TEST(qa_dsss_snr_estimator ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dsss_snr_estimator.py)
GR_ADD_TEST(qa_fsk_lecim_modulator_fc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_modulator_fc.py)
GR_ADD_TEST(qa_fsk_lecim_spreading_bb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_spreading_bb.py)
GR_ADD_TEST(qa_fsk_lecim_despreading_bb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_despreading_bb.py)
GR_ADD_TEST(qa_fsk_lecim_whitening_bb_bb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_whitening_bb_bb.py)
GR_ADD_TEST(qa_fsk_lecim_interleaver ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_dewhitening.py)
GR_ADD_TEST(qa_fsk_lecim_deinterleaver ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_deinterleaver.py)
GR_ADD_TEST(qa_fsk_lecim_demodulator_cb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_demodulator_cb.py)
GR_ADD_TEST(qa_fsk_lecim_phr_pdu_demux ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_phr_pdu_demux.py)
GR_ADD_TEST(qa_fsk_lecim_corr_est ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_corr_est.py)
GR_ADD_TEST(qa_fsk_lecim_phr_parser ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_phr_parser.py)
GR_ADD_TEST(qa_fsk_lecim_zero_depadding_bb_bb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_zero_depadding_bb_bb.py)
GR_ADD_TEST(qa_fsk_lecim_normalize_fcc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_normalize_fcc.py)
GR_ADD_TEST(qa_fsk_lecim_freq_offset_est_cc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_freq_offset_est_cc.py)
GR_ADD_TEST(qa_fsk_lecim_synchronizer_cc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_synchronizer_cc.py)
GR_ADD_TEST(qa_fsk_lecim_time_synchronizer_cc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_time_synchronizer_cc.py)
GR_ADD_TEST(qa_fsk_lecim_correlation_filter ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_correlation_filter.py)
GR_ADD_TEST(qa_fsk_lecim_detector ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fsk_lecim_detector.py)
