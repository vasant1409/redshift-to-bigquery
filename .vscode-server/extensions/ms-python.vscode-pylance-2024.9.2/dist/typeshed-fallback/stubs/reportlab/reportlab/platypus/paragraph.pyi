from reportlab.lib.abag import ABag
from reportlab.lib.styles import ParagraphStyle, PropertySet
from reportlab.pdfgen.textobject import PDFTextObject
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.paraparser import ParaFrag

class ParaLines(ABag): ...
class FragLine(ABag): ...

def cleanBlockQuotedText(text: str, joiner: str = " ") -> str: ...

class Paragraph(Flowable):
    text: str
    frags: list[ParaFrag]
    style: ParagraphStyle
    bulletText: str | None
    caseSensitive: int
    encoding: str
    def __init__(
        self,
        text: str,
        # NOTE: This should be a ParagraphStyle
        style: PropertySet | None = None,
        bulletText: str | None = None,
        frags: list[ParaFrag] | None = None,
        caseSensitive: int = 1,
        encoding: str = "utf8",
    ) -> None: ...
    def minWidth(self) -> float: ...
    def draw(self) -> None: ...
    def breakLines(self, width: float | list[float] | tuple[float, ...]) -> ParaLines | ParaFrag: ...
    def breakLinesCJK(self, maxWidths: float | list[float] | tuple[float, ...]) -> ParaLines | ParaFrag: ...
    def beginText(self, x: float, y: float) -> PDFTextObject: ...
    def drawPara(self, debug: int = 0) -> None: ...
    def getPlainText(self, identify: bool | None = None) -> str: ...
    def getActualLineWidths0(self) -> list[float]: ...
    @staticmethod
    def dumpFrags(frags, indent: int = 4, full: bool = False) -> str: ...
