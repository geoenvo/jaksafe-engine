# coding = utf-8
__AUTHOR__ = 'Abdul Somat Budiaji'

"""
Custom Exception untuk JakSAFE
"""

class JaksafeError(RuntimeError):

    """
    Base Class untuk Exception buatan dari Jaksafe
    """
    pass

class MultipleJumlahAsetError(JaksafeError):

    """
    Ketika jumlah aset yang diperoleh saat melookup agregat lebih dari dua
    """
    pass

class EmptyJumlahAsetError(JaksafeError):

    """
    Ketika tidak ada aset yang diperoleh saat melookup agregat
    """
    pass

class NoColumnSpecifiedError(JaksafeError):

    """
    Ketika tak ada kolom yang dimasukkan ke parameter
    """
    pass

class InvalidArgumentError(JaksafeError):

    """
    Ketika terdapat argument yang tidak diharapkan
    """
    pass

class NoHazardGeneratedDirError(JaksafeError):

    """
    Ketika tidak terdapat folder hazard yang dihasilkan
    """
    pass

class NoHazardGeneratedFileError(JaksafeError):

    """
    Ketika tidak terdapat file hazard yang dihasilkan
    """
    pass

class NoImpactBuildingError(JaksafeError):

    """
    Ketika tidak ada impact shapefile untuk building
    """
    pass

class NoImpactRoadError(JaksafeError):

    """
    Ketika tidak ada impact shapefile untuk road
    """
    pass

class NoAggregateFileError(JaksafeError):

    """
    Ketika tidak ada file aggregate csv
    """
    pass

class NoImpactOsmError(JaksafeError):
    pass

class NoImpactAggError(JaksafeError):
    pass

class NoAsumsiKerusakanError(JaksafeError):
    pass

class NoAsumsiKerugianError(JaksafeError):
    pass

class NoAsumsiPenetrasiFileError(JaksafeError):
    pass

class NoAsumsiAsuransiFileError(JaksafeError):
    pass

class NoAsumsiAggregatFileError(JaksafeError):
    pass
