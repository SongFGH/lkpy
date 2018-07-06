"""
Utilities for working with rating matrices.
"""

from collections import namedtuple
import logging

import pandas as pd
import scipy.sparse as sps

_logger = logging.getLogger(__package__)

RatingMatrix = namedtuple('RatingMatrix', ['matrix', 'users', 'items'])


def sparse_ratings(ratings, layout='csr'):
    """
    Convert a rating table to a sparse matrix of ratings.

    Args:
        ratings(pandas.DataFrame): a data table of (user, item, rating) triples.
        layout: the sparse matrix layout to use

    Returns:
        scipy.sparse.spmatrix:
            a sparse matrix with users on the rows and items on the columns.
    """

    uidx = pd.Index(ratings.user.unique())
    iidx = pd.Index(ratings.item.unique())
    _logger.debug('creating matrix with %d ratings for %d items by %d users',
                  len(ratings), len(iidx), len(uidx))

    row_ind = uidx.get_indexer(ratings.user)
    col_ind = iidx.get_indexer(ratings.item)

    if layout == 'csr':
        matrix = sps.csr_matrix((ratings.rating.values, (row_ind, col_ind)),
                                shape=(len(uidx), len(iidx)))
    elif layout == 'csc':
        matrix = sps.csc_matrix((ratings.rating.values, (row_ind, col_ind)),
                                shape=(len(uidx), len(iidx)))
    elif layout == 'coo':
        matrix = sps.coo_matrix((ratings.rating.values, (row_ind, col_ind)),
                                shape=(len(uidx), len(iidx)))

    return RatingMatrix(matrix, uidx, iidx)
