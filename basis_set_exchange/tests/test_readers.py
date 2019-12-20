"""
Tests functions for reading in formatted basis sets
"""

import bz2
import os
import pytest

from basis_set_exchange import curate
from .common_testvars import reader_test_data_dir

subdirs = [x for x in os.listdir(reader_test_data_dir)]
subdirs = [os.path.join(reader_test_data_dir, x) for x in subdirs]
subdirs = [x for x in subdirs if os.path.isdir(x)]

test_files = []
for subdir in subdirs:
    subfiles = os.listdir(subdir)
    subfiles = [os.path.join(subdir, x) for x in subfiles if x.endswith('.bz2')]
    subfiles = [os.path.relpath(x, reader_test_data_dir) for x in subfiles]
    test_files.extend(subfiles)

@pytest.mark.parametrize('file_rel_path', test_files)
def test_reader(file_rel_path):
    file_path = os.path.join(reader_test_data_dir, file_rel_path)
    is_bad = ".bad." in os.path.basename(file_path)
    
    if is_bad:
        # Read the first line of the file. This will contain the string
        # that should match the exception
        with bz2.open(file_path, 'rt', encoding='utf-8') as tf:
            match = tf.readline()

        # Get what we want to match as part of the exception
        match = match[8:].strip()

        with pytest.raises(Exception, match=match):
            curate.read_formatted_basis(file_path)
    else:
        curate.read_formatted_basis(file_path)


def test_reader_equivalent():
    # Test the two dalton formats. These two files are the same basis in the two slightly-different
    # format.
    file1 = os.path.join(reader_test_data_dir, 'dalton', '6-31g.good.1.mol.bz2')
    file2 = os.path.join(reader_test_data_dir, 'dalton', '6-31g.good.2.mol.bz2')
    data1 = curate.read_formatted_basis(file1)
    data2 = curate.read_formatted_basis(file2)

    assert data1 == data2
