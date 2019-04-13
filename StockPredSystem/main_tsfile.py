# coding: utf-8 -*-
from Tkinter import *
# from Tkinter import ttk
# from Tkinter import font
import Tkinter as tk
import tkFont
from ttk import *
import stock_predict
import datetime
import sys
import time
from threading import Timer
import functools

import Adafruit_GPIO as GPIO
import Adafruit_GPIO.FT232H as FT232H


class Page(Frame):
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, bg='grey', *args, **kwargs)

	def show(self):
		self.lift()


class PageTemplate(Frame):
	def __init__(self, *args):
		Frame.__init__(self, *args)

	def main_frame(self, pNum, q, answers, questions, *args):

		if pNum < 15:
			qNum = pNum - 2
			ansX = 400
		elif pNum < 26:
			qNum = pNum - 15
			ansX = 525

		questionFrame = tk.Frame(self, width=1400, height=50, bg='#e6e6e6')
		questionString = tk.Label(questionFrame, bg='#e6e6e6',
		                          font=tkFont.Font(family='Helvetica', size=20, weight='bold'),
		                          fg='black', text=str(qNum) + ". " + q)
		questionFrame.place(x=ansX, y=250)
		questionString.pack(in_=questionFrame, side='left')

		answersFrame = tk.Frame(self, width=1400, height=400, bg='#e6e6e6')

		ansLab1 = tk.Label(answersFrame, bg='#e6e6e6', font=tkFont.Font(family='Helvetica', size=20, weight='bold'),
		                   fg='black', text=answers[0], justify=LEFT)
		ansLab2 = tk.Label(answersFrame, bg='#e6e6e6', font=tkFont.Font(family='Helvetica', size=20, weight='bold'),
		                   fg='black', text=answers[1], justify=LEFT)
		ansLab3 = tk.Label(answersFrame, bg='#e6e6e6', font=tkFont.Font(family='Helvetica', size=20, weight='bold'),
		                   fg='black', text=answers[2], justify=LEFT)
		ansLab4 = tk.Label(answersFrame, bg='#e6e6e6', font=tkFont.Font(family='Helvetica', size=20, weight='bold'),
		                   fg='black', text=answers[3], justify=LEFT)

		ans1 = tk.Button(answersFrame, highlightbackground='#e6e6e6', text="A", width=20,
		                 command=lambda: self.ansSubmit("A. " + answers[0], pNum + 1, questions,
		                                                [questionString, ansLab1, ansLab2, ansLab3, ansLab4, ans1, ans2,
		                                                 ans3, ans4], questionFrame))
		ans2 = tk.Button(answersFrame, highlightbackground='#e6e6e6', text="B", width=20,
		                 command=lambda: self.ansSubmit("B. " + answers[1], pNum + 1, questions,
		                                                [questionString, ansLab1, ansLab2, ansLab3, ansLab4, ans1, ans2,
		                                                 ans3, ans4], questionFrame))
		ans3 = tk.Button(answersFrame, highlightbackground='#e6e6e6', text="C", width=20,
		                 command=lambda: self.ansSubmit("C. " + answers[2], pNum + 1, questions,
		                                                [questionString, ansLab1, ansLab2, ansLab3, ansLab4, ans1, ans2,
		                                                 ans3, ans4], questionFrame))
		ans4 = tk.Button(answersFrame, highlightbackground='#e6e6e6', text="D", width=20,
		                 command=lambda: self.ansSubmit("D. " + answers[3], pNum + 1, questions,
		                                                [questionString, ansLab1, ansLab2, ansLab3, ansLab4, ans1, ans2,
		                                                 ans3, ans4], questionFrame))

		answersFrame.place(x=ansX, y=300)
		ans1.grid(in_=answersFrame, column=0, row=0, padx=20, pady=20)
		ans2.grid(in_=answersFrame, column=0, row=1, padx=20, pady=20)
		ans3.grid(in_=answersFrame, column=0, row=2, padx=20, pady=20)
		ans4.grid(in_=answersFrame, column=0, row=3, padx=20, pady=20)

		ansLab1.grid(in_=answersFrame, column=1, row=0)
		ansLab2.grid(in_=answersFrame, column=1, row=1)
		ansLab3.grid(in_=answersFrame, column=1, row=2)
		ansLab4.grid(in_=answersFrame, column=1, row=3)

	def ansSubmit(self, answer, qNum, questions, itemsList, questionFrame):

		# Response made


		if qNum < 16:
			self.send_timestamp_dom_resp(qNum)
		elif qNum > 16 and qNum < 27:
			self.send_timestamp_alg_resp(qNum)

		if qNum == 15:
			print("Break between Dom & Alg questions")
			self.after(5000, self.ansSubmit, "BREAK", qNum + 1, questions, itemsList, questionFrame)
		# self.after(60000, self.ansSubmit, "BREAK", qNum + 1, questions, itemsList, questionFrame)

		print("qnum-1: " + str(qNum - 1))
		datestr = time.strftime("%m-%d")
		filename = "Output" + datestr + ".txt"

		text_file = open(filename, 'a')
		text_file.write(str(qNum - 1) + ":  ")
		text_file.write(answer + "\n")

		# First Algebra Question
		if qNum == 15:
			questions[qNum - 1].show()
			self.update()
		# self.send_timestamp_alg_app(qNum)
		else:

			try:
				# Algebra Question
				# Functionality for hiding the content after a question during the pause is here as well
				if qNum > 15 and qNum < 27:
					# Set pseudorandom delay after each question
					if qNum == 20 or qNum == 23 or qNum == 25:
						print("Sleep 1 Minute")

						# Hide content
						itemsList[0].pack_forget()
						for item in itemsList:
							item.grid_remove()
						self.update()

						# Pause system
						time.sleep(10)
					# time.sleep(60)

					elif qNum == 21 or qNum == 26:
						print("Sleep 7 seconds")

						itemsList[0].pack_forget()
						for item in itemsList:
							item.grid_remove()
						self.update()

						time.sleep(7)

					elif qNum == 17 or qNum == 22:
						print("Sleep 27 seconds")

						itemsList[0].pack_forget()
						for item in itemsList:
							item.grid_remove()
						self.update()

						time.sleep(10)
					# time.sleep(27)

					elif qNum == 18:
						print("Sleep 17 secs")

						itemsList[0].pack_forget()
						for item in itemsList:
							item.grid_remove()
						self.update()

						time.sleep(10)
					# time.sleep(17)

					elif qNum == 24:
						print("Sleep 30 secs")

						itemsList[0].pack_forget()
						for item in itemsList:
							item.grid_remove()
						self.update()

						time.sleep(10)
					# time.sleep(30)

					elif qNum == 19:
						print("Sleep 13")

						itemsList[0].pack_forget()
						for item in itemsList:
							item.grid_remove()
						self.update()

						time.sleep(10)
					# time.sleep(13)

					if qNum < 26:
						self.send_timestamp_alg_app(qNum)

					questions[qNum - 1].show()
					itemsList[0].pack(in_=questionFrame, side='left')

					# Redraw next question
					for item in itemsList:
						item.grid()
					self.update()

				# Domain Questions
				else:
					questions[qNum - 1].show()
					self.update()

			except IndexError:
				print("Out of bounds")

			print("qnum: " + str(qNum))

	def send_timestamp_alg_app(self, qNum):
		if hardware == True:
			# Send 0110 (6)
			ft232h.output_all(0x600)

			time.sleep(0.3)

			# Reset back to 0000
			ft232h.output_all(0x0000)

		datestr = time.strftime("%m-%d")
		filename = "Output" + datestr + ".txt"
		text_file = open(filename, 'a')
		text_file.write("Algebra Question " + str(qNum - 15) + " Appear (M" + str(6) + "): " +
		                datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))
		text_file.close()

		print("Algebra Question " + str(qNum - 15) + " Appear (M" + str(6) + "): " +
		      datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))

	def send_timestamp_dom_resp(self, qNum):
		dom_q = [[3, 5, 10, 11], [1, 6, 7, 9], [2, 4, 8, 12]]

		if (qNum - 3) in dom_q[0]:
			if hardware == True:
				# Send 0011 (3)
				ft232h.output_all(0x300)

				time.sleep(0.3)

				# Reset back to 0000
				ft232h.output_all(0x0000)

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write("Domain Basic: Question " + str(qNum - 3) + " Response (M" + str(3) + "): " +
			                datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print("Domain Basic")
			print("Question " + str(qNum - 3) + " Response (M" + str(3) + "): " +
			      datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))

		elif (qNum - 3) in dom_q[1]:
			if hardware == True:
				# Send 0100 (4)
				ft232h.output_all(0x400)

				time.sleep(0.3)

				# Reset back to 0000
				ft232h.output_all(0x0000)

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write("Domain Medium: Question " + str(qNum - 3) + " Response (M" + str(4) + "): " +
			                datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print("Domain Medium")
			print("Question " + str(qNum - 3) + " Response (M" + str(4) + "): " +
			      datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))

		elif (qNum - 3) in dom_q[2]:
			if hardware == True:
				# Send 0101 (5)
				ft232h.output_all(0x500)

				time.sleep(0.3)

				# Reset back to 0000
				ft232h.output_all(0x0000)

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write("Domain Advanced: Question " + str(qNum - 3) + " Response (M" + str(5) + "): " +
			                datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print("Domain Advanced")
			print("Question " + str(qNum - 3) + " Response (M" + str(5) + "): " +
			      datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))

	def send_timestamp_alg_resp(self, qNum):
		alg_q = [[2, 3, 7, 10], [1, 6, 9], [4, 5, 8]]

		if (qNum - 16) in alg_q[0]:
			if hardware == True:
				# Send 0111 (7)
				ft232h.output_all(0x700)

				time.sleep(0.3)

				# Reset back to 0000
				ft232h.output_all(0x0000)

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write("Algebra Basic Question " + str(qNum - 16) + " Response (M" + str(7) + "): " +
			                datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print("Algebra Basic")
			print("Algebra Question " + str(qNum - 16) + " Response (M" + str(7) + "): " +
			      datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))

		elif (qNum - 16) in alg_q[1]:
			if hardware == True:
				# Send 1000 (8)
				ft232h.output_all(0x800)

				time.sleep(0.3)

				# Reset back to 0000
				ft232h.output_all(0x0000)

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write("Algebra Medium Question " + str(qNum - 16) + " Response (M" + str(8) + "): " +
			                datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print("Algebra Medium")
			print("Algebra Question " + str(qNum - 16) + " Response (M" + str(8) + "): " +
			      datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))

		elif (qNum - 16) in alg_q[2]:
			if hardware == True:
				# Send 1001 (9)
				ft232h.output_all(0x900)

				time.sleep(0.3)

				# Reset back to 0000
				ft232h.output_all(0x0000)

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write("Algebra Advanced Question " + str(qNum - 16) + " Response (M" + str(9) + "): " +
			                datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print("Algebra Advanced")
			print("Algebra Question " + str(qNum - 16) + " Response (M" + str(9) + "): " +
			      datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))

	def run_delayed(self, q):
		self.send_timestamp3()
		q.show()
		self.update()

	def show(self):
		self.lift()


class BreakPage(tk.Frame):
	def __init__(self, *args):
		tk.Frame.__init__(self, bg='#e6e6e6', *args)

	def main_frame(self, pNum, questions, *args):
		if pNum == 15:
			main_text = "Thanks you for completing this series of questions.\nAnother series will now start.  Please answer them.\n" \
			            "A pause will occur after each question, relax until the next question appears."
		elif pNum == 37:
			main_text = "In a few moments you will be asked to predict whether to buy\n or sell the stocks you " \
			            "previously studied in the table."
		elif pNum == 38:
			main_text = "For the next 30 seconds, direct your thoughts completely to\n how willing you feel to " \
			            "participate in the stock prediction mentioned previously."
		elif pNum == 41:
			main_text = "Thank you for participating."

		label = tk.Label(self, bg='#e6e6e6', font=tkFont.Font(family='Helvetica', size=20, weight='bold'),
		                 text=main_text)
		label.place(anchor="c", relx=.5, rely=.5)

		answersFrame = tk.Frame(self, width=300, height=30, bg='#e6e6e6')
		answersFrame.place(x=575, y=500)

		if pNum == 41:
			continueBut = tk.Button(answersFrame, highlightbackground='#e6e6e6', text="Exit", width=20,
			                        command=root.destroy)
			continueBut.grid(in_=answersFrame, column=0, row=0, padx=30, pady=30)

		elif pNum == 38 or pNum == 15:
			print("Placeholder")

		else:
			continueBut = tk.Button(answersFrame, highlightbackground='#e6e6e6', text="Continue", width=20,
			                        command=lambda: self.continueEval(pNum + 1, questions))
			continueBut.grid(in_=answersFrame, column=0, row=0, padx=30, pady=30)

	def continueEval(self, qNum, questions):
		print(qNum - 1)

		# qNum will always be +1 of the actual page index number cause its set to call
		# the next page

		# First Algebra Question
		if qNum == 16:
			self.send_timestamp(qNum)

		try:
			if qNum == 38:
				print("Ponder Willingness")
				# Ponder Willingness Page (30 secs)
				questions[qNum - 1].show()
				self.send_timestamp(qNum)
				self.update()
				# Leading to Stock Interaction Page
				# after 30 secs
				# self.after(30000, self.continueEval, qNum + 1, questions)
				self.after(5000, self.continueEval, qNum + 1, questions)
			elif qNum == 39:
				print("Scale Page")
				# Scale Page
				questions[qNum - 1].show()
				self.send_timestamp(qNum)
				self.update()
			else:
				print("All else")
				questions[qNum - 1].show()
				self.update()

		except IndexError:
			print("Out of bounds")

	def send_timestamp(self, qNum):
		fp = open("marker.txt", "w")

		if qNum == 16:
			if hardware == True:
				# Send 0110 (6)
				ft232h.output_all(0x600)

				time.sleep(0.3)

				# Reset back to 0000
				ft232h.output_all(0x0000)

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write("Algebra Question " + str(1) + " Appear (M" + str(6) + "): " +
			                datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print("Algebra Question " + str(1) + " Appear (M" + str(6) + "): " +
			      datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))

		if qNum == 38:
			if hardware == True:
				# Send 1101 (13)
				ft232h.output_all(0xD17)

				time.sleep(0.3)

				# Reset back to 0000
				ft232h.output_all(0x0000)

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write(
				"Ponder Willigness (M" + str(12) + "): " + datetime.datetime.fromtimestamp(time.time()).strftime(
					'%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print("Ponder Willigness (M" + str(12) + "): " + datetime.datetime.fromtimestamp(time.time()).strftime(
				'%Y-%m-%d %H:%M:%S.%f'))

		if qNum == 39:
			if hardware == True:
				# Send 1110 (14)
				ft232h.output_all(0xE17)

				time.sleep(0.3)

				# Reset back to 0000
				ft232h.output_all(0x0000)

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write("Scale (M" + str(13) + "): " + datetime.datetime.fromtimestamp(time.time()).strftime(
				'%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print("Scale (M" + str(13) + "): " + datetime.datetime.fromtimestamp(time.time()).strftime(
				'%Y-%m-%d %H:%M:%S.%f'))

		fp.close()

	def show(self):
		self.lift()


class ScalePage(tk.Frame):
	def __init__(self, *args):
		tk.Frame.__init__(self, bg='#e6e6e6', *args)

	def main_frame(self, pNum, questions, *args):
		main_text = "Please rate your willingness on the scale provided\n" \
		            "with 1 being not willing at all and 10 being very willing."

		label = tk.Label(self, bg='#e6e6e6', font=tkFont.Font(family='Helvetica', size=20, weight='bold'),
		                 text=main_text)
		label.place(anchor="c", relx=.5, rely=.5)

		answersFrame = tk.Frame(self, width=300, height=30, bg='#e6e6e6')
		answersFrame.place(x=575, y=500)

		score = StringVar()
		scoreBox = Combobox(self, textvariable=score, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
		scoreBox.grid(in_=answersFrame, column=0, row=0, pady=(40, 40))

		continueBut = tk.Button(answersFrame, highlightbackground='#e6e6e6', text="Continue", width=20,
		                        command=lambda: self.continueEval(score.get(), pNum + 1, questions))
		continueBut.grid(in_=answersFrame, column=0, row=1, padx=30, pady=30)

	def continueEval(self, score, qNum, questions):
		print(qNum - 1)

		try:
			print("Stock Interaction Page")
			questions[qNum - 1].show()
			self.send_timestamp(qNum)
			self.update()

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write("Willingness Score: ")
			text_file.write(str(score) + "\n")

		except IndexError:
			print("Out of bounds")

	def send_timestamp(self, qNum):
		if hardware == True:
			# Send 1111 (15)
			ft232h.output_all(0xF17)

			time.sleep(0.3)

			# Reset back to 0000
			ft232h.output_all(0x0000)

		datestr = time.strftime("%m-%d")
		filename = "Output" + datestr + ".txt"
		text_file = open(filename, 'a')
		text_file.write("Start of Prediction Interface (M14): " + datetime.datetime.fromtimestamp(time.time()).strftime(
			'%Y-%m-%d %H:%M:%S.%f'))
		text_file.close()

		print("Start of Prediction Interface (M14): " + datetime.datetime.fromtimestamp(time.time()).strftime(
			'%Y-%m-%d %H:%M:%S.%f'))

	def show(self):
		self.lift()


class InstructPage(tk.Frame):
	def __init__(self, *args):
		tk.Frame.__init__(self, bg='#e6e6e6', *args)

	def main_frame(self, pNum, questions, *args):

		if pNum == 1:
			main_text = "A central crosshair will appear next.  Please keep your gaze on it and rest for 2 minutes."
		else:
			main_text = "A crosshair will appear in the center of the screen and \nmove back and forth to the corners.  " \
			            "Follow it and hold your \ngaze steady on the crosshair.\n" \
			            "After that some stock market data will appear.  Please examine it."

		label = tk.Label(self, bg='#e6e6e6', font=tkFont.Font(family='Helvetica', size=20, weight='bold'),
		                 text=main_text)
		label.place(anchor="c", relx=.5, rely=.5)

		answersFrame = tk.Frame(self, width=300, height=30, bg='#e6e6e6')
		answersFrame.place(x=575, y=500)

		if pNum != 31:
			continueBut = tk.Button(answersFrame, highlightbackground='#e6e6e6', text="Continue", width=20,
			                        command=lambda: self.continueEval(pNum + 1, questions))
		else:
			continueBut = tk.Button(answersFrame, highlightbackground='#e6e6e6', text="Exit", width=20,
			                        command=root.destroy)

		continueBut.grid(in_=answersFrame, column=0, row=0, padx=30, pady=30)

	def continueEval(self, qNum, questions):
		print(qNum)

		# In production, 2 mins.
		if qNum == 2:
			delay = 5000
		# delay = 120000
		else:
			if qNum % 2 == 0:
				delay = 2000
			else:
				delay = 1000

		# In production, 2 mins.
		data_delay = 5000
		# data_delay = 120000

		print(delay)

		if qNum == 36:
			# Stock Data Page
			questions[qNum - 1].show()
			self.update()
			self.send_timestamp(qNum)
			self.after(data_delay, self.continueEval, qNum + 1, questions)

		elif qNum == 37:
			# Prediction Instruction Page
			self.send_timestamp(qNum)
			questions[qNum - 1].show()
			self.update()

		elif qNum == 2:
			# Central Crosshair Page
			try:
				questions[qNum - 1].show()
				self.update()
				self.send_timestamp(qNum)
				self.after(delay, self.continueEval, qNum + 1, questions)

			except IndexError:
				print("Out of bounds")

		elif qNum == 3:
			try:
				questions[qNum - 1].show()
				self.update()
				self.send_timestamp(qNum)

			except IndexError:
				print("Out of bounds")

		else:
			try:
				questions[qNum - 1].show()
				self.update()
				self.send_timestamp(qNum)
				self.after(delay, self.continueEval, qNum + 1, questions)

			except IndexError:
				print("Out of bounds")

	def send_timestamp(self, qNum):

		if qNum == 2:
			if hardware == True:
				# Send 0001 (1)
				ft232h.output_all(0x100)

				time.sleep(0.3)

				# Reset back to 0000
				ft232h.output_all(0x0000)

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write("Central Crosshair (M1): " +
			                datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print("Central Crosshair (M1): " +
			      datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))

		elif qNum == 3:
			if hardware == True:
				# Send 0010 (2)
				ft232h.output_all(0x200)

				time.sleep(0.3)

				# Reset back to 0000
				ft232h.output_all(0x0000)

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write("Domain Question 1 Appearance (M" + str(2) + "): " + datetime.datetime.fromtimestamp(
				time.time()).strftime(
				'%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print(
			"Domain Question 1 Appearance (M" + str(2) + "): " + datetime.datetime.fromtimestamp(time.time()).strftime(
				'%Y-%m-%d %H:%M:%S.%f'))

		elif qNum == 36:
			if hardware == True:
				# Send 1011 (11)
				ft232h.output_all(0xB17)

				time.sleep(0.3)

				# Reset back to 0000
				ft232h.output_all(0x0000)

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write(
				"Stock Data Start (M" + str(11) + "): " + datetime.datetime.fromtimestamp(time.time()).strftime(
					'%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print("Stock Data Start (M" + str(11) + "): " + datetime.datetime.fromtimestamp(time.time()).strftime(
				'%Y-%m-%d %H:%M:%S.%f'))

		elif qNum == 37:
			if hardware == True:
				# Send 1100 (12)
				ft232h.output_all(0xC17)

				time.sleep(0.3)

				# Reset back to 0000
				ft232h.output_all(0x0000)

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write(
				"Stock Data End (M" + str(11) + "): " + datetime.datetime.fromtimestamp(time.time()).strftime(
					'%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print("Stock Data End (M" + str(11) + "): " + datetime.datetime.fromtimestamp(time.time()).strftime(
				'%Y-%m-%d %H:%M:%S.%f'))

		else:
			if hardware == True:
				# Send 1010 (10)
				ft232h.output_all(0xA17)

				time.sleep(0.3)

				# Reset back to 0000
				ft232h.output_all(0x0000)

			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write("Crosshairs (M" + str(10) + "): " + datetime.datetime.fromtimestamp(time.time()).strftime(
				'%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print("Crosshairs (M" + str(10) + "): " + datetime.datetime.fromtimestamp(time.time()).strftime(
				'%Y-%m-%d %H:%M:%S.%f'))

	def show(self):
		self.lift()


class CrosshairPage(tk.Frame):
	def __init__(self, *args):
		tk.Frame.__init__(self, bg='#e6e6e6', *args)

	def main_frame(self, pNum, questions, *args):

		self.crosshair = PhotoImage(file="crosshair.gif")

		if pNum == 2 or pNum == 27 or pNum == 29 or pNum == 31 or pNum == 33 or pNum == 35:
			xnum = 0.5
			ynum = 0.5
		if pNum == 28:
			xnum = 0.01
			ynum = 0.01
		if pNum == 30:
			xnum = 0.95
			ynum = 0.01
		if pNum == 32:
			xnum = 0.01
			ynum = 0.90
		if pNum == 34:
			xnum = 0.95
			ynum = 0.90

		label = tk.Label(self, bg='#e6e6e6', image=self.crosshair, borderwidth=0, highlightthickness=0)
		label.place(anchor=NW, relx=xnum, rely=ynum)

	# center 0.5, 0.5
	# upper left 0.01 , 0.01
	# upper right 0.95, 0.01
	# lower left 0.01, 0.90
	# lower right 0.95, 0.90

	def show(self):
		self.lift()


class PredData(Frame):
	def __init__(self, *args):
		Frame.__init__(self, *args)

	def main_frame(self, pNum, stock_data, pred_results, questions, *args):

		stocks = ['Petroleum Industry Company (BP)', 'Southwestern Energy Company (SWN)', 'SPDR Gold Trust (GLD)',
		          'United States Oil Fund (USO)', 'Dow Jones Industrial Average (DJI)', 'Chevron Corporation (CVX)']

		stocks_sym = ['BP', 'SWN', 'GLD', 'USO', 'CVX', 'DJI']

		# stock_data is a list of dataframes, each one cooresponding to a different stock.
		# 0 = BP, 1 = SWN, 2 = GLD, 3 = USO, 4 = DJI, 5 = CVX

		SMA = self.calculateSMA(stock_data)

		stock_index = stock_data[0].index

		yesterday = stock_index[-1].strftime('%Y-%m-%d')[5:10]
		twodaysago = stock_index[-2].strftime('%Y-%m-%d')[5:10]
		threedaysago = stock_index[-3].strftime('%Y-%m-%d')[5:10]
		fourdaysago = stock_index[-4].strftime('%Y-%m-%d')[5:10]
		fivedaysago = stock_index[-5].strftime('%Y-%m-%d')[5:10]

		dataFrame = tk.Frame(self, width=1300, height=650, bg='white')
		dataFrame.place(anchor="c", relx=.5, rely=.5)

		tree = Treeview(dataFrame, columns=("Day1", "Day2", "Day3", "Day4", "Day5"), height="30")

		style = Style()
		style.configure(".", font=("Helvetica", 20), foreground='black')
		style.configure("Treeview", foreground='black', rowheight=22)
		style.configure("Treeview.Heading", foreground='black', font=("Helvetica", 20))

		tree.column("#0", width=400)
		tree.column("Day1", width=125)
		tree.column("Day2", width=125)
		tree.column("Day3", width=125)
		tree.column("Day4", width=125)
		tree.column("Day5", width=125)

		tree.heading("#0", text="Stock")
		tree.heading("Day1", text=fivedaysago)
		tree.heading("Day2", text=fourdaysago)
		tree.heading("Day3", text=threedaysago)
		tree.heading("Day4", text=twodaysago)
		tree.heading("Day5", text=yesterday)

		# tree.insert(PARENT, ORDER, MAIN COLUMN, SUPP COLUMNS)

		for i in range(6):
			tree.insert("", i, stocks[i], text=stocks[i], open=True)

			tree.insert(stocks[i], "end", str(i) + "High", text="High",
			            values=[round(stock_data[i].iloc[-5]["High"], 2),
			                    round(stock_data[i].iloc[-4]["High"], 2),
			                    round(stock_data[i].iloc[-3]["High"], 2),
			                    round(stock_data[i].iloc[-2]["High"], 2),
			                    round(stock_data[i].iloc[-1]["High"], 2)])
			tree.insert(stocks[i], "end", str(i) + "Low", text="Low",
			            values=[round(stock_data[i].iloc[-5]["Low"], 2),
			                    round(stock_data[i].iloc[-4]["Low"], 2),
			                    round(stock_data[i].iloc[-3]["Low"], 2),
			                    round(stock_data[i].iloc[-2]["Low"], 2),
			                    round(stock_data[i].iloc[-1]["Low"], 2)])
			tree.insert(stocks[i], "end", str(i) + "AdjClose", text="Adj Close",
			            values=[round(stock_data[i].iloc[-5]["Adj Close"], 2),
			                    round(stock_data[i].iloc[-4]["Adj Close"], 2),
			                    round(stock_data[i].iloc[-3]["Adj Close"], 2),
			                    round(stock_data[i].iloc[-2]["Adj Close"], 2),
			                    round(stock_data[i].iloc[-1]["Adj Close"], 2)])
			tree.insert(stocks[i], "end", str(i) + "SMA", text="10 Day Simple Moving Avg",
			            values=["-", "-", "-", "-", round(SMA[i], 2)])

		tree.grid(in_=dataFrame, column=0, row=0)

	def calculateSMA(self, stock_data):
		raw_data = {'BP': [], 'SWN': [], 'GLD': [], 'USO': [], 'DJI': [], 'CVX': []}
		sma = []

		for j in range(1, 11):
			raw_data['BP'].append(round(stock_data[0].iloc[-j]["Adj Close"], 4))
			raw_data['SWN'].append(round(stock_data[1].iloc[-j]["Adj Close"], 4))
			raw_data['GLD'].append(round(stock_data[2].iloc[-j]["Adj Close"], 4))
			raw_data['USO'].append(round(stock_data[3].iloc[-j]["Adj Close"], 4))
			raw_data['DJI'].append(round(stock_data[4].iloc[-j]["Adj Close"], 4))
			raw_data['CVX'].append(round(stock_data[5].iloc[-j]["Adj Close"], 4))

		sma.append(sum(raw_data['BP']) / 10)
		sma.append(sum(raw_data['SWN']) / 10)
		sma.append(sum(raw_data['GLD']) / 10)
		sma.append(sum(raw_data['USO']) / 10)
		sma.append(sum(raw_data['DJI']) / 10)
		sma.append(sum(raw_data['CVX']) / 10)

		return sma

	def show(self):
		self.lift()


class PredInterface(Frame):
	def __init__(self, *args):
		Frame.__init__(self, *args)

	def main_frame(self, pNum, stock_data, pred_results, questions, *args):
		stocks = ['Petroleum Industry Company (BP)', 'Southwestern Energy Company (SWN)', 'SPDR Gold Trust (GLD)',
		          'United States Oil Fund (USO)', 'Dow Jones Industrial Average (DJI)', 'Chevron Corporation (CVX)']

		stocks_sym = ['BP', 'SWN', 'GLD', 'USO', 'CVX', 'DJI']

		# stock_data is a list of dataframes, each one cooresponding to a different stock.
		# 0 = BP, 1 = SWN, 2 = GLD, 3 = USO, 4 = DJI, 5 = CVX

		SMA = self.calculateSMA(stock_data)

		stock_index = stock_data[0].index

		yesterday = stock_index[-1].strftime('%Y-%m-%d')[5:10]
		twodaysago = stock_index[-2].strftime('%Y-%m-%d')[5:10]
		threedaysago = stock_index[-3].strftime('%Y-%m-%d')[5:10]
		fourdaysago = stock_index[-4].strftime('%Y-%m-%d')[5:10]
		fivedaysago = stock_index[-5].strftime('%Y-%m-%d')[5:10]

		dataFrame = tk.Frame(self, width=1300, height=650, bg='white')
		dataFrame.place(x=50, y=75)

		tree = Treeview(dataFrame, columns=("Day1", "Day2", "Day3", "Day4", "Day5"), height="30")

		style = Style()
		style.configure(".", font=("Helvetica", 20), foreground='black')
		style.configure("Treeview", foreground='black', rowheight=22)
		style.configure("Treeview.Heading", foreground='black', font=("Helvetica", 20))

		tree.column("#0", width=400)
		tree.column("Day1", width=125)
		tree.column("Day2", width=125)
		tree.column("Day3", width=125)
		tree.column("Day4", width=125)
		tree.column("Day5", width=125)

		tree.heading("#0", text="Stock")
		tree.heading("Day1", text=fivedaysago)
		tree.heading("Day2", text=fourdaysago)
		tree.heading("Day3", text=threedaysago)
		tree.heading("Day4", text=twodaysago)
		tree.heading("Day5", text=yesterday)

		# tree.insert(PARENT, ORDER, MAIN COLUMN, SUPP COLUMNS)

		for i in range(6):
			tree.insert("", i, stocks[i], text=stocks[i], open=True)

			tree.insert(stocks[i], "end", str(i) + "High", text="High",
			            values=[round(stock_data[i].iloc[-5]["High"], 2),
			                    round(stock_data[i].iloc[-4]["High"], 2),
			                    round(stock_data[i].iloc[-3]["High"], 2),
			                    round(stock_data[i].iloc[-2]["High"], 2),
			                    round(stock_data[i].iloc[-1]["High"], 2)])
			tree.insert(stocks[i], "end", str(i) + "Low", text="Low",
			            values=[round(stock_data[i].iloc[-5]["Low"], 2),
			                    round(stock_data[i].iloc[-4]["Low"], 2),
			                    round(stock_data[i].iloc[-3]["Low"], 2),
			                    round(stock_data[i].iloc[-2]["Low"], 2),
			                    round(stock_data[i].iloc[-1]["Low"], 2)])
			tree.insert(stocks[i], "end", str(i) + "AdjClose", text="Adj Close",
			            values=[round(stock_data[i].iloc[-5]["Adj Close"], 2),
			                    round(stock_data[i].iloc[-4]["Adj Close"], 2),
			                    round(stock_data[i].iloc[-3]["Adj Close"], 2),
			                    round(stock_data[i].iloc[-2]["Adj Close"], 2),
			                    round(stock_data[i].iloc[-1]["Adj Close"], 2)])
			tree.insert(stocks[i], "end", str(i) + "SMA", text="10 Day Simple Moving Avg",
			            values=["-", "-", "-", "-", round(SMA[i], 2)])

		tree.grid(in_=dataFrame, column=0, row=0)

		# Prediction Column

		predFrame = tk.Frame(self, width=300, height=650, bg='white')
		predFrame.grid(in_=dataFrame, column=1, row=0)

		predHeading = tk.Label(self, bg='white', font=tkFont.Font(family='Helvetica', size=20, weight='bold'),
		                       text="Your Predictions")
		predHeading.place(in_=predFrame, x=20, y=-30)

		# BP Prediction Block

		BPLabel = tk.Label(self, bg='white', font=tkFont.Font(family='Helvetica', size=15, weight='bold'),
		                   text="BP")
		BPLabel.grid(in_=predFrame, column=0, row=1, pady=(10, 20))

		BPpred = StringVar()
		BPpred.trace('w', self.box_changed)
		BPbox = Combobox(predFrame, textvariable=BPpred, values=["BUY", "SELL"])
		BPbox.grid(in_=predFrame, column=1, row=1, pady=(10, 20))

		# SWN Prediction Block

		SWNLabel = tk.Label(self, bg='white', font=tkFont.Font(family='Helvetica', size=15, weight='bold'),
		                    text="SWN")
		SWNLabel.grid(in_=predFrame, column=0, row=2)

		SWNpred = StringVar()
		SWNpred.trace('w', self.box_changed)
		SWNbox = Combobox(predFrame, textvariable=SWNpred, values=["BUY", "SELL"])
		SWNbox.grid(in_=predFrame, column=1, row=2, pady=(35, 40))

		# GLD Prediction Block

		GLDLabel = tk.Label(self, bg='white', font=tkFont.Font(family='Helvetica', size=15, weight='bold'),
		                    text="GLD")
		GLDLabel.grid(in_=predFrame, column=0, row=3)

		GLDpred = StringVar()
		GLDpred.trace('w', self.box_changed)
		GLDbox = Combobox(predFrame, textvariable=GLDpred, values=["BUY", "SELL"])
		GLDbox.grid(in_=predFrame, column=1, row=3, pady=(40, 40))

		# USO Prediction Block

		USOLabel = tk.Label(self, bg='white', font=tkFont.Font(family='Helvetica', size=15, weight='bold'),
		                    text="USO")
		USOLabel.grid(in_=predFrame, column=0, row=4)

		USOpred = StringVar()
		USOpred.trace('w', self.box_changed)
		USObox = Combobox(predFrame, textvariable=USOpred, values=["BUY", "SELL"])
		USObox.grid(in_=predFrame, column=1, row=4, pady=(40, 40))

		# DJI Prediction Block

		DJILabel = tk.Label(self, bg='white', font=tkFont.Font(family='Helvetica', size=15, weight='bold'),
		                    text="DJI")
		DJILabel.grid(in_=predFrame, column=0, row=5)

		DJIpred = StringVar()
		DJIpred.trace('w', self.box_changed)
		DJIbox = Combobox(predFrame, textvariable=DJIpred, values=["BUY", "SELL"])
		DJIbox.grid(in_=predFrame, column=1, row=5, pady=(40, 40))

		# CVX Prediction Block

		CVXLabel = tk.Label(self, bg='white', font=tkFont.Font(family='Helvetica', size=15, weight='bold'),
		                    text="CVX")
		CVXLabel.grid(in_=predFrame, column=0, row=6, pady=(40, 40))

		CVXpred = StringVar()
		CVXpred.trace('w', self.box_changed)
		CVXbox = Combobox(predFrame, textvariable=CVXpred, values=["BUY", "SELL"])
		CVXbox.grid(in_=predFrame, column=1, row=6, pady=(40, 40))

		submitBut = tk.Button(predFrame, highlightbackground='white', text="Submit",
		                      command=lambda: self.submitPred(BPpred, SWNpred, GLDpred,
		                                                      USOpred, DJIpred, CVXpred, pred_results, questions))
		submitBut.grid(in_=predFrame, column=0, row=7, columnspan=2)

	def box_changed(self, intvar, iflist, mode):
		self.send_timestamp()

	def send_timestamp(self):
		if hardware == True:
			# Send 10000 (16)
			ft232h.output_all(0x1000)

			time.sleep(0.3)

			# Reset back to 0000
			ft232h.output_all(0x0000)

		datestr = time.strftime("%m-%d")
		filename = "Output" + datestr + ".txt"
		text_file = open(filename, 'a')
		text_file.write(
			"Prediction Change (M" + str(15) + "): " + datetime.datetime.fromtimestamp(time.time()).strftime(
				'%Y-%m-%d %H:%M:%S.%f'))
		text_file.close()

		print("Prediction Change (M" + str(15) + "): " + datetime.datetime.fromtimestamp(time.time()).strftime(
			'%Y-%m-%d %H:%M:%S.%f'))

	def calculateSMA(self, stock_data):
		raw_data = {'BP': [], 'SWN': [], 'GLD': [], 'USO': [], 'DJI': [], 'CVX': []}
		sma = []

		for j in range(1, 11):
			raw_data['BP'].append(round(stock_data[0].iloc[-j]["Adj Close"], 4))
			raw_data['SWN'].append(round(stock_data[1].iloc[-j]["Adj Close"], 4))
			raw_data['GLD'].append(round(stock_data[2].iloc[-j]["Adj Close"], 4))
			raw_data['USO'].append(round(stock_data[3].iloc[-j]["Adj Close"], 4))
			raw_data['DJI'].append(round(stock_data[4].iloc[-j]["Adj Close"], 4))
			raw_data['CVX'].append(round(stock_data[5].iloc[-j]["Adj Close"], 4))

		sma.append(sum(raw_data['BP']) / 10)
		sma.append(sum(raw_data['SWN']) / 10)
		sma.append(sum(raw_data['GLD']) / 10)
		sma.append(sum(raw_data['USO']) / 10)
		sma.append(sum(raw_data['DJI']) / 10)
		sma.append(sum(raw_data['CVX']) / 10)

		return sma

	def submitPred(self, BPpred, SWNpred, GLDpred, USOpred, DJIpred, CVXpred, pred_results, questions):

		datestr = time.strftime("%m-%d")
		filename = "Output" + datestr + ".txt"

		text_file = open(filename, 'a')
		text_file.write("Subject BP: " + BPpred.get() + "\n")
		text_file.write("Subject SWN: " + SWNpred.get() + "\n")
		text_file.write("Subject GLD: " + GLDpred.get() + "\n")
		text_file.write("Subject USO: " + USOpred.get() + "\n")
		text_file.write("Subject DJI: " + DJIpred.get() + "\n")
		text_file.write("Subject CVX: " + CVXpred.get() + "\n")

		for k, v in pred_results.items():
			text_file.write('%s=%s\n' % (k, v))

		text_file.close()

		try:
			questions[40].show()
			self.send_final_timestamp()
		except IndexError:
			print("Out of bounds")

	def send_final_timestamp(self):
		# fp = open("marker.txt", "w")
		# fp.write(str(17))

		datestr = time.strftime("%m-%d")
		filename = "Output" + datestr + ".txt"
		text_file = open(filename, 'a')
		text_file.write("Final Page System End" + datetime.datetime.fromtimestamp(time.time()).strftime(
			'%Y-%m-%d %H:%M:%S.%f'))
		text_file.close()

		print("Final Page System End" + datetime.datetime.fromtimestamp(time.time()).strftime(
			'%Y-%m-%d %H:%M:%S.%f'))

	# fp.close()

	def show(self):
		self.lift()


class TitlePage(Page):
	def __init__(self, *args, **kwargs):
		Frame.__init__(self, *args, **kwargs)
		main_label = tk.Label(self, bg='#e6e6e6', font=tkFont.Font(family='Helvetica', size=20, weight='bold'),
		                      text="The Self-Adaptive Stock Prediction Engine")
		main_label.place(x=500, y=320)


class MainView(Frame):
	def __init__(self, *args, **kwargs):
		Frame.__init__(self, *args, **kwargs)

		global titlePage
		titlePage = TitlePage(self)

		container = tk.Frame(self, width=1400, height=800, bg='grey')
		container.grid(column=0, row=0, sticky=(N, S, E, W))

		titlePage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		first_q = self.create_pages(self, container)

		beginA = tk.Button(titlePage, highlightbackground='#e6e6e6', text="Begin", width=20,
		                   command=lambda: self.create_program(first_q))

		beginA.place(x=600, y=400)

		titlePage.show()
		self.send_timestamp(0)

	def create_program(self, first_q):
		first_q.show()
		self.send_timestamp(1)

	def send_timestamp(self, mark):
		if mark == 0:
			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write("Start: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print("Start: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))
		else:
			datestr = time.strftime("%m-%d")
			filename = "Output" + datestr + ".txt"
			text_file = open(filename, 'a')
			text_file.write("Structured Rest Page: " + datetime.datetime.fromtimestamp(time.time()).strftime(
				'%Y-%m-%d %H:%M:%S.%f'))
			text_file.close()

			print(
			"Structured Rest Page: " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'))

	def create_pages(self, container, *args):
		pages = []

		stock_data, pred_results = self.retrieve_stock_data()

		struct_rest_instruct = InstructPage(self)
		pages.append(struct_rest_instruct)
		struct_rest_instruct.main_frame(1, pages)

		cross0 = CrosshairPage(self)
		pages.append(cross0)
		cross0.main_frame(2, pages)

		dom_q1 = PageTemplate(self)
		pages.append(dom_q1)
		dom_q1.main_frame(3,
		                  "What factor does not affect the stock market?",
		                  ["Natural Disasters", "Labor Strike", "Internal reformation with one company",
		                   "Terrorist Attack"], pages)

		dom_q2 = PageTemplate(self)
		pages.append(dom_q2)
		dom_q2.main_frame(4,
		                  "An 'illiquid market' is also called a thin market and is characterized by?",
		                  ["The lack of buyer and sellers", "The lack of alternative investments",
		                   "The lack of stocks traded", "The lack of profits gained recently"], pages)

		dom_q3 = PageTemplate(self)
		pages.append(dom_q3)
		dom_q3.main_frame(5,
		                  "What is the ratio used to compare a stock's market value to its book value?",
		                  ["Price to book ratio", "Dividend yield ratio",
		                   "Price earning ratio", "Earning per share"], pages)

		dom_q4 = PageTemplate(self)
		pages.append(dom_q4)
		dom_q4.main_frame(6,
		                  "How has Natural Gas correlated with WTI (W&T Offshore Drilling) over the last 20 years?",
		                  ["Positive Correlation", "Negative Correlation", "No Correlation", "Exponential Correlation"],
		                  pages)

		dom_q5 = PageTemplate(self)
		pages.append(dom_q5)
		dom_q5.main_frame(7,
		                  "What does the bear and bull stand for in regards to the market?",
		                  ["The bear means stock prices are falling\n and the bull means stock prices are rising.",
		                   "They are signs that the stock market opened and closed.",
		                   "The bear means stock prices are rising\n and the bull means stock prices are falling.",
		                   "They are signs that the stock market is fluxuating very quickly "], pages)

		dom_q6 = PageTemplate(self)
		pages.append(dom_q6)
		dom_q6.main_frame(8,
		                  "What is a company that usually has a positive correlation to the prices of Natural Gas?",
		                  ["Southwestern Energy Company", "Ford", "Apple", "Amazon"], pages)

		dom_q7 = PageTemplate(self)
		pages.append(dom_q7)
		dom_q7.main_frame(9,
		                  "What is a company with market capitalization of $5,000,000,000 is considered to be?",
		                  ["Small Cap", "Mid Cap", "Large Cap", "Mega Cap"], pages)

		dom_q8 = PageTemplate(self)
		pages.append(dom_q8)
		dom_q8.main_frame(10,
		                  "What natural resource does fracking help to keep prices lower by increasing the \navailable supply to consumers?",
		                  ["Oil", "Natural Gas", "Steel", "Gold"], pages)

		dom_q9 = PageTemplate(self)
		pages.append(dom_q9)
		dom_q9.main_frame(11,
		                  "Which of the following is least likely to occur from/during a short selling strategy?",
		                  ["You receive a margin call order", "You may end up with very high losses",
		                   "You may have to come up with money if share prices increase",
		                   "The bank holding your mortgage may not agree"], pages)

		dom_q10 = PageTemplate(self)
		pages.append(dom_q10)
		dom_q10.main_frame(12,
		                   "What is a Santa Claus rally?",
		                   ["A rise in stock prices in January", "A rise in stock prices in December",
		                    "A drop in stock prices in January", "A drop in stock prices in December"], pages)

		dom_q11 = PageTemplate(self)
		pages.append(dom_q11)
		dom_q11.main_frame(13,
		                   "How many companies make up the Dow Jones Industrial Average (DJIA)?",
		                   ["10 Companies", "20 Companies", "30 Companies", "50 Companies"], pages)

		dom_q12 = PageTemplate(self)
		pages.append(dom_q12)
		dom_q12.main_frame(14,
		                   "What type of correlation has been shown to exist between GLD (SPDR Gold Shares) \nand DJIA (Dow Jones Industrial Average)?",
		                   ["Positive Correlation", "Negative Correlation", "No Correlation",
		                    "Exponential Correlation"], pages)

		breakPage = BreakPage(self)
		pages.append(breakPage)
		breakPage.main_frame(15, pages)

		alg_q1 = PageTemplate(self)
		pages.append(alg_q1)
		alg_q1.main_frame(16, "Solve for x:   5x - 10 = 110 + 7x",
		                  ["x = -60", "x = -20", "x = 20", "x = 60"],
		                  pages)

		alg_q2 = PageTemplate(self)
		pages.append(alg_q2)
		alg_q2.main_frame(17, u"Solve:   100 - 4(7-4)\u00b2",
		                  ["925", "64", "-44", "969"],
		                  pages)

		alg_q3 = PageTemplate(self)
		pages.append(alg_q3)
		alg_q3.main_frame(18, u"Solve:  (9x\u00b2 + 6x + 4) - (6x\u00b2 + 2)",
		                  [u"3x\u00b2 + 6x + 4", u"9x\u00b2 + 3x + 3", u"3x\u00b2 + 6x + 2", u"6x\u00b2 + 3x + 2"],
		                  pages)

		alg_q4 = PageTemplate(self)
		pages.append(alg_q4)
		alg_q4.main_frame(19, "Solve:  (2y + 3)(y + 1)",
		                  [u"4y\u00b2 + 8y + 6", u"2y\u00b2 + 5y + 3", u"2y\u00b2 + 10y + 6", u"2y\u00b2 + 5y + 6"],
		                  pages)

		alg_q5 = PageTemplate(self)
		pages.append(alg_q5)
		alg_q5.main_frame(20, "What is the non-zero solution to:  6g(2g + 5) = 0",
		                  [u"12g\u00b2 + 30", u"12g\u00b2 + 5", "-3/2", "-5/2"],
		                  pages, breakPage)

		alg_q6 = PageTemplate(self)
		pages.append(alg_q6)
		alg_q6.main_frame(21, "Solve:  3y + 2 > 12 - y",
		                  ["y > 2/5", "y < 5/2", "y < 2/5", "y > 5/2"],
		                  pages)

		alg_q7 = PageTemplate(self)
		pages.append(alg_q7)
		alg_q7.main_frame(22, u"Solve:  (5g + 8) + (2g\u00b2 + 5g + 1)",
		                  [u"2g\u00b2 + 5g + 3", u"2g\u00b2 + 10g + 9", u"10g\u00b2 + 5g + 3", u"10g\u00b2 + 10g + 9"],
		                  pages)

		alg_q8 = PageTemplate(self)
		pages.append(alg_q8)
		alg_q8.main_frame(23, u"Solve:  -6√2 - 10√2",
		                  [u"-16√2", u"8√2", u"-4√2", u"16√2"],
		                  pages)

		alg_q9 = PageTemplate(self)
		pages.append(alg_q9)
		alg_q9.main_frame(24, u"Solve and simplify the answer:  6(q\u00b2 - 9) = -q\u00b2 + 9",
		                  ["9", "3", "-9", "0"],
		                  pages)

		alg_q10 = PageTemplate(self)
		pages.append(alg_q10)
		alg_q10.main_frame(25, u"Simplify:  2x + 3x\u00b2 + 5x\u00b3 - 2x\u00b2 - 3x - 1",
		                   [u"5x\u00b3 + 2x\u00b2 - x - 1", u"5x\u00b3 + x\u00b2 - x - 1",
		                    u"5x\u00b3 + 2x\u00b2 - x - 1", u"5x\u00b3 + 2x\u00b2 - x - 2"],
		                   pages)

		instPage = InstructPage(self)
		pages.append(instPage)
		instPage.main_frame(26, pages)

		cross1 = CrosshairPage(self)
		pages.append(cross1)
		cross1.main_frame(27, pages)

		cross2 = CrosshairPage(self)
		pages.append(cross2)
		cross2.main_frame(28, pages)

		cross3 = CrosshairPage(self)
		pages.append(cross3)
		cross3.main_frame(29, pages)

		cross4 = CrosshairPage(self)
		pages.append(cross4)
		cross4.main_frame(30, pages)

		cross5 = CrosshairPage(self)
		pages.append(cross5)
		cross5.main_frame(31, pages)

		cross6 = CrosshairPage(self)
		pages.append(cross6)
		cross6.main_frame(32, pages)

		cross7 = CrosshairPage(self)
		pages.append(cross7)
		cross7.main_frame(33, pages)

		cross8 = CrosshairPage(self)
		pages.append(cross8)
		cross8.main_frame(34, pages)

		cross9 = CrosshairPage(self)
		pages.append(cross9)
		cross9.main_frame(35, pages)

		pred_data = PredData(self)
		pages.append(pred_data)
		pred_data.main_frame(36, stock_data, pred_results, pages)

		pred_instruct = BreakPage(self)
		pages.append(pred_instruct)
		pred_instruct.main_frame(37, pages)

		ponder_will = BreakPage(self)
		pages.append(ponder_will)
		ponder_will.main_frame(38, pages)

		scale_page = ScalePage(self)
		pages.append(scale_page)
		scale_page.main_frame(39, pages)

		pred_interface = PredInterface(self)
		pages.append(pred_interface)
		pred_interface.main_frame(40, stock_data, pred_results, pages)

		final_page = BreakPage(self)
		pages.append(final_page)
		final_page.main_frame(41, pages)

		struct_rest_instruct.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		cross0.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		dom_q1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		dom_q2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		dom_q3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		dom_q4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		dom_q5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		dom_q6.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		dom_q7.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		dom_q8.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		dom_q9.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		dom_q10.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		dom_q11.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		dom_q12.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		breakPage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		alg_q1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		alg_q2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		alg_q3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		alg_q4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		alg_q5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		alg_q6.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		alg_q7.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		alg_q8.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		alg_q9.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		alg_q10.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		instPage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		cross1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		cross2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		cross3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		cross4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		cross5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		cross6.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		cross7.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		cross8.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		cross9.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		pred_data.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		pred_instruct.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		ponder_will.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		scale_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		pred_interface.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		final_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		return struct_rest_instruct

	def retrieve_stock_data(self):

		stock_data, pred_results = stock_predict.run_predict()

		return stock_data, pred_results


if __name__ == "__main__":

	reload(sys)
	sys.setdefaultencoding('utf-8')

	global hardware
	hardware = True

	if hardware == True:
		# Code for Adafruit Board

		# Temporarily disable FTDI serial drivers.
		FT232H.use_FT232H()

		# Create an FT232H object that grabs the first available FT232H device found.
		ft232h = FT232H.FT232H()

		# Initialize the output pins
		ft232h.setup(8, GPIO.OUT)  # Make pin C0 a digital output.
		ft232h.setup(9, GPIO.OUT)  # Make pin C1 a digital output.
		ft232h.setup(10, GPIO.OUT)  # Make pin C2 a digital output.
		ft232h.setup(11, GPIO.OUT)  # Make pin C3 a digital output.
		ft232h.setup(12, GPIO.OUT)  # Make pin C3 a digital output.
		print("initialized pins")

		# Set to 0000
		ft232h.output_all(0x0000)

	root = Tk()
	root.configure(bg='grey')
	main = MainView(root)

	main.pack(side="top", fill="both", expand=True)
	root.wm_geometry("1400x800")

	root.mainloop()