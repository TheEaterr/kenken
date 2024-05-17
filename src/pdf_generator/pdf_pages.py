from enum import Enum
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import use
use('Agg')
import os
import sys


class PageType(Enum):
    PUZZLE_PAGE = 1
    SOLUTION_PAGE = 2


class PuzzlePages:
    '''Class to create a PDF with puzzle and solution pages.'''

    def getFilePath() -> str:
        '''Returns the file path of the PDF.'''
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.getcwd()
        puzzles_folder = os.path.join(application_path, 'puzzles')
        if not os.path.exists(puzzles_folder):
            os.mkdir(puzzles_folder)
        i = 1

        def getPDFPath():
            nonlocal i
            return os.path.join(puzzles_folder, f'kenken_{i}.pdf')

        while os.path.exists(
                getPDFPath()) == True:
            i += 1
        return getPDFPath()

    def __init__(self):
        self.puzzle_pages = []
        self.solution_pages = []

    def createPage(self, page_type: PageType):
        page = PuzzlePage(page_type)
        if page_type == PageType.PUZZLE_PAGE:
            page_list = self.puzzle_pages
        elif page_type == PageType.SOLUTION_PAGE:
            page_list = self.solution_pages
        page.index = len(page_list)
        page.setTitles()
        page_list.append(page)
        return page

    def exportToPdf(self) -> str:
        '''Exports the PuzzlePages object as a pdf and opens it.
        
        Returns the path to the created PDF.
        '''
        file_path = PuzzlePages.getFilePath()
        with PdfPages(file_path) as pdf:
            for page in self.puzzle_pages:
                page: PuzzlePage
                pdf.savefig(page.fig)
            for page in self.solution_pages:
                page: PuzzlePage
                pdf.savefig(page.fig)
        plt.close('all')
        if sys.platform == 'win32':
            os.startfile(file_path)
        else:
            os.system('open ' + file_path)
        return file_path


class PuzzlePage:

    def __init__(self, page_type: PageType) -> None:
        self.ax_list: list[Axes] = []
        self.title_format = ''
        self.index = 0
        self.puzzles_on_page = 0
        if page_type == PageType.PUZZLE_PAGE:
            self.fig, self.ax_list = plt.subplots(
                2, 1, figsize=(8.27, 11.69))
            self.title_format = 'Puzzle {}'
            self.puzzles_on_page = 2
        elif page_type == PageType.SOLUTION_PAGE:
            self.fig, ax_list = plt.subplots(
                4, 3, figsize=(8.27, 11.69))
            for ax in ax_list.flatten():
                self.ax_list.append(ax)
            self.title_format = 'Solution {}'
            self.puzzles_on_page = 12

        for index, ax in enumerate(self.ax_list):
            ax: Axes
            ax.set_axis_off()
            ax.axis('equal')

    def setTitles(self):
        for index, ax in enumerate(self.ax_list):
            ax.index = self.index*self.puzzles_on_page + index
            ax.title_info = self.title_format.format(ax.index + 1)