from matplotlib.axes import Axes


class PuzzleDrawer:
    LINE_COLOR = 'black'
    BOLD_WIDTH = 3
    DEFAULT_WIDTH = 1
    TITLE_FONT_SIZE = 10

    def __init__(self, ax: Axes) -> None:
        self.ax = ax
        self.ax.set_title(
            self.ax.title_info, fontsize=PuzzleDrawer.TITLE_FONT_SIZE)

    def drawHorizontalLine(self, x, is_bold: bool = False):
        self.drawLine([0, 9], [x, x], is_bold)

    def drawVerticalLine(self, y, is_bold: bool = False):
        self.drawLine([y, y], [0, 9], is_bold)

    def drawLine(self, point_one, point_two, is_bold: bool = False):
        if is_bold:
            line_width = PuzzleDrawer.BOLD_WIDTH
        else:
            line_width = PuzzleDrawer.DEFAULT_WIDTH
        self.ax.plot(
            point_one, point_two,
            color=PuzzleDrawer.LINE_COLOR,
            linewidth=line_width
        )

    def placeTextInCell(self, i, j, text):
        self.ax.text(
            j + 0.5,
            i + 0.4,
            text,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=14
        )

    def placeNoteInCell(self, i, j, note):
        self.ax.text(
            j + 0.1,
            i + 0.9,
            note,
            horizontalalignment='left',
            verticalalignment='top',
            fontsize='xx-small'
        )


class KenkenPuzzleDrawer(PuzzleDrawer):

    def __init__(self, ax) -> None:
        super().__init__(ax)

    def drawClique(self, clique, operation, target):

        def getBorders(cell):
            line = cell[0]
            column = cell[1]
            return [
                [[line, column], [line + 1, column]],
                [[line, column + 1], [line + 1, column + 1]],
                [[line, column], [line, column + 1]],
                [[line + 1, column], [line + 1, column + 1]]
            ]

        region_borders = []

        cell_with_operation_index = 0
        for index, cell in enumerate(clique):
            cell_with_operation = clique[cell_with_operation_index]
            if (cell[1] < cell_with_operation[1] or
                    (cell[0] > cell_with_operation[0] and
                    cell[1] == cell_with_operation[1])):
                cell_with_operation_index = index
            cell_borders = getBorders(cell)
            for border in cell_borders:
                if border in region_borders:
                    region_borders.remove(border)
                else:
                    region_borders.append(border)

        for border in region_borders:
            self.ax.plot(
                [border[0][1],border[1][1]],
                [border[0][0], border[1][0]],
                color='gray',
                linestyle=(0, (0.2, 1)),
                linewidth=5
            )

        cell_with_operation = clique[cell_with_operation_index]
        self.placeNoteInCell(
            cell_with_operation[0],
            cell_with_operation[1],
            f'{target},{operation}'
        )
        
    def drawPuzzle(self, cliques: list, values: "dict[tuple[int, int], int]"):
        for i in range(10):
            is_bold = i%3 == 0
            self.drawHorizontalLine(i, is_bold)
            self.drawVerticalLine(i, is_bold)

        for clique in cliques:
            offset_cell_list = []
            for cell in clique[0]:
                offset_cell_list.append((cell[0] - 1, cell[1] - 1))
            self.drawClique(offset_cell_list, clique[1], clique[2])

        for i in range(10):
            for j in range(10):
                if (i+ 1, j + 1) in values:
                    self.placeTextInCell(i, j, str(values[(i+ 1, j + 1)]))