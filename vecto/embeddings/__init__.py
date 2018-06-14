"""Loading and training for embeddings"""
import os
import logging
import numpy as np
import vecto.embeddings.dense
from vecto.vocabulary import Vocabulary

logger = logging.getLogger(__name__)


def load_from_dir(path):
    """Automatically detects embeddings format and loads

    Args:
        path: directory where embeddings are stores

    Returns:
        Instance of appropriate Model-based class
    """
#    if os.path.isfile(os.path.join(path, "cooccurrence_csr.h5p")):
#        logger.info("detected as sparse explicit in hdf5")
#        result = ModelSparse()
#        result.load_from_hdf5(path)
#        result.load_metadata(path)
#        return result
#    if os.path.isfile(os.path.join(path, "bigrams.data.bin")):
#        logger.info("detected as sparse in vecto legacy format")
#        result = ModelSparse()
#        result.load(path)
#        result.load_metadata(path)
#        return result

    if os.path.isfile(os.path.join(path, "vectors.h5p")):
        result = vecto.embeddings.dense.WordEmbeddingsDense()
        logger.info("detected as vecto format ")
        result.load_hdf5(path)
        result.load_metadata(path)
        return result

    result = vecto.embeddings.dense.WordEmbeddingsDense()
    files = os.listdir(path)
    for f in files:
        if f.endswith(".gz") or f.endswith(".bz") or f.endswith(".txt"):
            logger.info(path + "Detected VSM in plain text format")
            result.load_from_text(os.path.join(path, f))
            result.load_metadata(path)
            return result
        if f.endswith(".npy"):
            logger.info("Detected VSM in numpy format")
            result.matrix = np.load(os.path.join(path, f))
            result.vocabulary = Vocabulary()
            result.vocabulary.load(path)
            result.load_metadata(path)
            return result
        if any(file.endswith('bin') for file in os.listdir(path)):
            result = ModelW2V()
            logger.info("Detected VSM in the w2v original binary format")
            result.load_from_dir(path)
            result.load_metadata(path)
            return result

    raise RuntimeError("Cannot detect the format of this VSM")
