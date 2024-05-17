from tkinter import *
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
from gui.generator_thread import GeneratorThread

class KenkenGeneratorGUI(ThemedTk):
	def __init__(self, theme) -> None:
		super().__init__(theme=theme)

		self.title("Générateur de Kenken")
		self.geometry(
			"+{}+{}".format(
				int(self.winfo_screenwidth()/2 - self.winfo_reqwidth()/2),
				int(self.winfo_screenheight()/2 - self.winfo_reqheight())
			)
		)
		self.resizable(True, True)
		self.protocol("WM_DELETE_WINDOW", self.onClosing)

		self.label = ttk.Label(
			text='Paramétrage des puzzles', font=('Helvetica', 16))
		self.label.pack(pady=10)

		max_suggestion_label = ttk.Label(
			text='Nombre de suggestions maximum :')
		max_suggestion_label.pack()
		self.max_suggestion_var = IntVar(self, value=81)
		self.max_suggestion_slider = ttk.Scale(
			self,
			from_=0,
			to=81,
			variable=self.max_suggestion_var,
			orient=HORIZONTAL,
			length=200,
			command=self.onSliderChangeMax,
		)
		self.max_suggestion_value_label = ttk.Label(
			text=self.max_suggestion_var.get())
		self.max_suggestion_value_label.pack()
		self.max_suggestion_slider.pack()

		min_suggestion_label = ttk.Label(
			text='Nombre de suggestions minimum :')
		min_suggestion_label.pack()
		self.min_suggestion_var = IntVar(self, value=0)
		self.min_suggestion_slider = ttk.Scale(
			self,
			from_=0,
			to=81,
			variable=self.min_suggestion_var,
			orient=HORIZONTAL,
			length=200,
			command=self.onSliderChangeMin,
		)
		self.min_suggestion_value_label = ttk.Label(
			text=self.min_suggestion_var.get())
		self.min_suggestion_value_label.pack()
		self.min_suggestion_slider.pack()

		operations_label = ttk.Label(
			text='Opérations du puzzle :')
		operations_label.pack()
		self.operation_checkboxes = []
		operations = ['+', '-', '*', '/']
		for i in range(4):
			variable = IntVar(self, value=1)
			self.operation_checkboxes.append(
				{
					'checkbox': ttk.Checkbutton(
						self,
						text=operations[i],
						variable=variable,
					),
					'variable': variable,
					'operation': operations[i],
				}
			)
			self.operation_checkboxes[i]['checkbox'].pack()

		# Spinner for number of puzzles
		self.nb_puzzles_label = ttk.Label(
			text='Nombre de puzzles à générer :')
		self.nb_puzzles_label.pack()
		self.nb_puzzles_var = IntVar(self, value=2)
		self.nb_puzzles_spinner = ttk.Spinbox(
			self,
			from_=1,
			to=100,
			textvariable=self.nb_puzzles_var,
			command=self.onSpinnerChange,
		)
		self.nb_puzzles_value_label = ttk.Label(
			text=self.nb_puzzles_var.get())
		self.nb_puzzles_value_label.pack()
		self.nb_puzzles_spinner.pack()

		self.solution_var = IntVar(self, value=1)
		self.solution_checkbox = ttk.Checkbutton(
			self,
			text='Générer les solutions',
			variable=self.solution_var,
			command=self.onSolutionCheckboxClick,
		)
		self.solution_checkbox.pack()

		self.label = ttk.Label(
			self, 
			text='Génération des puzzles',
			font=('Helvetica', 16)
		)
		self.label.pack(pady=10)

		self.button = ttk.Button(
			self, text="Générer le PDF",
			command=self.startGeneratePDFThread
		)
		self.button.pack()

		self.progressValue = DoubleVar()
		self.progressBar = ttk.Progressbar(
			self, orient="horizontal", length=280, variable=self.progressValue)
		self.progressBar.pack()

		self.infoLabel = Label(self, text="", fg="#3daee9")
		self.infoLabel.pack()

	def onSpinnerChange(self):
		self.nb_puzzles_value_label.config(text=self.nb_puzzles_var.get())

	def onSolutionCheckboxClick(self):
		if self.solution_var.get() == 1:
			self.solution_checkbox.config(text='Générer les solutions')
		else:
			self.solution_checkbox.config(text='Ne pas générer les solutions')

	def onSliderChangeMax(self, value):
		self.max_suggestion_slider.config(
			value = self.max_suggestion_var.get())
		self.max_suggestion_value_label.config(
			text=self.max_suggestion_var.get())

	def onSliderChangeMin(self, value):
		self.min_suggestion_slider.config(
			value = self.min_suggestion_var.get())
		self.min_suggestion_value_label.config(
			text=self.min_suggestion_var.get())

	def setInfoLabelText(self, label):
		self.infoLabel.config(text=label)

	def setProgressBar(self, val):
		self.progressValue.set(val)

	def monitorPDFGenerate(self, thread: GeneratorThread):
		if thread.is_alive():
			# check the thread every 100ms
			self.after(100, lambda: self.monitorPDFGenerate(thread))
			self.setProgressBar(thread.progress)
			self.setInfoLabelText(thread.info_label)

		else:
			thread.join()
			self.setProgressBar(thread.progress)
			self.setInfoLabelText(thread.info_label)
			if thread.error_label != '':
				messagebox.showerror(
					"Erreur",
					thread.error_label
				)
			self.button.config(state=NORMAL)

	def startGeneratePDFThread(self):
		thread = GeneratorThread()
		thread.generate_solutions = self.solution_var.get()
		thread.max_suggestions = self.max_suggestion_var.get()
		thread.min_suggestions = self.min_suggestion_var.get()
		thread.operations = [
			op['operation'] for op in self.operation_checkboxes
			if op['variable'].get() == 1
		]
		thread.nb_puzzles = self.nb_puzzles_var.get()
		if thread.min_suggestions > thread.max_suggestions:
			self.setInfoLabelText(
				"La valeur minimum est supérieure à la valeur maximum.")
			return
		if thread.operations == []:
			self.setInfoLabelText(
				"Veuillez sélectionner au moins une opération.")
			return
		if '+' not in thread.operations and '*' not in thread.operations:
			self.setInfoLabelText(
				"Veuillez sélectionner au moins une opération de type + ou *.")
			return
		if thread.nb_puzzles < 0:
			self.setInfoLabelText(
				"Veuillez entrer un nombre de puzzles strictement positif.")
			return
		thread.start()
		self.monitorPDFGenerate(thread)
		self.button.config(state=DISABLED)

	def onClosing(self):
		if (self.progressBar.cget("value") == 0 or 
				self.progressBar.cget("value") == 100):
			self.quit()
			self.destroy()
		else:
			messagebox.showinfo(
				title="Génération en cours",
				message=(
					"Veuillez attendre que le traitement "
					"soit terminé pour quitter."
				)
			)