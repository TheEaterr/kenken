from math import ceil
from pdf_generator.pdf_pages import PageType, PuzzlePages
from pdf_generator.puzzle_drawer import KenkenPuzzleDrawer


def generatePDF(puzzles, solutions, notifyPageCreated) -> str:
    pages = PuzzlePages()
    for i in range(ceil(len(puzzles)/2)):
        page = pages.createPage(PageType.PUZZLE_PAGE)
        puzzle_drawer = KenkenPuzzleDrawer(page.ax_list[0])
        puzzle_drawer.drawPuzzle(puzzles[2*i][0], puzzles[2*i][1])
        if 2*i+1 < len(puzzles):
            puzzle_drawer = KenkenPuzzleDrawer(page.ax_list[1])
            puzzle_drawer.drawPuzzle(puzzles[2*i + 1][0], puzzles[2*i + 1][1])
        notifyPageCreated()
    
    for i in range(ceil(len(solutions)/12)):
        page = pages.createPage(PageType.SOLUTION_PAGE)
        for j in range(12):
            if i*12 + j < len(solutions):
                puzzle_drawer = KenkenPuzzleDrawer(page.ax_list[j])
                puzzle_drawer.drawPuzzle([], solutions[i*12 + j])
        notifyPageCreated()

    return pages.exportToPdf()