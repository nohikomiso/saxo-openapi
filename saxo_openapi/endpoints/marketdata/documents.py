# -*- encoding: utf-8 -*-

"""Handle market data documents endpoints."""

from ..decorators import endpoint
from ..referencedata.base import ReferenceData


@endpoint("openapi/mkt/v2/instruments/{Uic}/{AssetType}/documents/pdf")
class InstrumentPdfDocument(ReferenceData):
    """Get PDF document for an instrument.

    See: docs/api/marketdata/documents.md#instrumentpdfdocument
    """

    def __init__(self, Uic: int, AssetType: str) -> None:
        super(InstrumentPdfDocument, self).__init__(Uic=Uic, AssetType=AssetType)


@endpoint("openapi/mkt/v2/instruments/{Uic}/{AssetType}/documents/recommended")
class RecommendedInstrumentDocuments(ReferenceData):
    """Get recommended documents for an instrument.

    See: docs/api/marketdata/documents.md#recommendedinstrumentdocuments
    """

    def __init__(self, Uic: int, AssetType: str) -> None:
        super(RecommendedInstrumentDocuments, self).__init__(
            Uic=Uic,
            AssetType=AssetType,
        )
