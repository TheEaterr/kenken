from pdf_generator.pdf_generator import generatePDF
import threading
from generator.generator import generatePuzzles
from math import ceil
import traceback

class GeneratorThread(threading.Thread):
	'''Le thread générant le PDF.'''

	def __init__(self) -> None:
		super().__init__()
		self.progress = 0
		self.operations = '+/-*'
		self.generate_solutions = True
		self.min_suggestions = 0
		self.max_suggestions = 81
		self.nb_puzzles = 2
		self.info_label = ''
		self.nb_generated_puzzles = 0
		self.nb_generated_pages = 0
		self.error_label = ''

	def run(self):

		try:
			self.nb_pages = ceil(self.nb_puzzles / 2)
			if self.generate_solutions:
				self.nb_pages += ceil(self.nb_puzzles/12)

			self.updatePuzzleInfoLabel()

			puzzles, solutions = generatePuzzles(
				self.nb_puzzles,
				self.min_suggestions,
				self.max_suggestions,
				self.operations,
				self.notifyPuzzleCreated)

			self.progress = 50
			self.updatePDFInfoLabel()
			if self.generate_solutions:
				file_path = generatePDF(
					puzzles, solutions, self.notifyPageCreated)
			else:
				file_path = generatePDF(puzzles, [], self.notifyPageCreated)
			self.progress = 100
			self.info_label = (
				f'Génération terminée !\nPDF '
				f'généré à l\'emplacement:\n{file_path}')
		except:
			self.info_label = 'Erreur lors de la génération !'
			self.error_label = traceback.format_exc()
			self.progress = 100

	def updatePuzzleInfoLabel(self):
		self.info_label = (
			f'Génération des puzzles en cours... '
			f'({self.nb_generated_puzzles}/{self.nb_puzzles})')

	def updatePDFInfoLabel(self):
		self.info_label = (
			f'Génération du PDF en cours... '
			f'({self.nb_generated_pages}/{self.nb_pages})')

	def notifyPuzzleCreated(self):
		self.nb_generated_puzzles += 1
		self.progress += 1 / self.nb_puzzles * 50
		self.updatePuzzleInfoLabel()

	def notifyPageCreated(self):
		self.nb_generated_pages += 1
		self.progress += 1 / self.nb_pages * 50
		self.updatePDFInfoLabel()