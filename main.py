import random
import qiskit
import time

import numpy as np
from qiskit import *
# Import Aer
from qiskit import Aer
# %matplotlib inline




import sys, pygame
pygame.init()

RED=(255, 0,0)
GREEN=(0, 255,0)
WHITE=(255,255,255)
GREY=(75,75,75)
DARKGREY=(150,150,150)
BLACK=(0,0,0)
CYAN=(0,255,255)

size = width, height = 600, 800

screen = pygame.display.set_mode(size)
# clock = pygame.time.Clock()

pygame.font.init()
myfont = pygame.font.SysFont("monospace", 100)
kucukFont = pygame.font.SysFont("monospace", 20)

labelSiyah = myfont.render("Siyah", 14, (255,255,0))
labelBeyaz = myfont.render("Beyaz", 14, (255,255,0))
oyunBitti = myfont.render("Tekrar Oyna", 14, (255,255,0))

labelMenu = myfont.render("Menu", 14, BLACK)
labelOynaH = myfont.render("H-Othello", 14, BLACK)
labelOynaX = myfont.render("X-Othello", 14, BLACK)
labelOynaRand = myfont.render("?-Othello", 14, BLACK)
labelOynaSec = myfont.render("#-Othello", 14, BLACK)

labelCPU1 = myfont.render("C1", 14, BLACK)
labelP1 = myfont.render("P1", 14, BLACK)

labelCPU2 = myfont.render("C2", 14, BLACK)
labelP2 = myfont.render("P2", 14, BLACK)

labelHarf = [myfont.render("X", 14, GREY), myfont.render("Z", 14, GREY), myfont.render("H", 14, GREY)]

# labelTry = kucukFont.render("Try Again", 14, BLACK)


# Create a Quantum Circuit acting on a quantum register of three qubits
son = 0
oyunBittiMi = 0

circ = []
for i in range(16):
	circ.append(QuantumCircuit(1))



sifir = QuantumCircuit(1);
backend = Aer.get_backend('statevector_simulator')
job = execute(sifir, backend)
result = job.result()
sifirOutputstate = result.get_statevector(sifir, decimals=3)

bir = QuantumCircuit(1);
bir.x(0);
backend = Aer.get_backend('statevector_simulator')
job = execute(bir, backend)
result = job.result()
birOutputstate = result.get_statevector(bir, decimals=3)


loc = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]

def tumYazdir():
	# i. sistemdeki qbit eger superpos durumundaysa -1 diger turlu durumunu dondurur
	# circ[i].draw(output='mpl', filename="circ" + str(i) + ".png")
	for i in range(4):
		for j in range(4):
			if(qbitBul(i, j) != -1):
				x = qbitBul(i, j)
				backend = Aer.get_backend('statevector_simulator')
				job = execute(circ[x], backend)
				result = job.result()
				outputstate = result.get_statevector(circ[x], decimals=3)
				print(i, j, end = " = ")
				print(outputstate)

def yazdir(i):
	# i. sistemdeki qbit eger superpos durumundaysa -1 diger turlu durumunu dondurur
	# circ[i].draw(output='mpl', filename="circ" + str(i) + ".png")
	backend = Aer.get_backend('statevector_simulator')
	job = execute(circ[i], backend)
	result = job.result()
	outputstate = result.get_statevector(circ[i], decimals=3)
	# print(outputstate)
	if(abs(outputstate[0].real) == abs(sifirOutputstate[0].real) and  abs(outputstate[1].real) == abs(sifirOutputstate[1].real)):
		dondur = 0
	else:
		if(abs(outputstate[0].real) == abs(birOutputstate[0].real) and  abs(outputstate[1].real) == abs(birOutputstate[1].real) ):
			dondur = 1
		else:
			if(outputstate[0].real * outputstate[1].real > 0):
				dondur = -1
			else:
				dondur = -2
	return dondur

def stateYazdir(i):
	# i. sistemdeki qbit eger superpos durumundaysa -1 diger turlu durumunu dondurur
	# circ[i].draw(output='mpl', filename="circ" + str(i) + ".png")
	backend = Aer.get_backend('statevector_simulator')
	job = execute(circ[i], backend)
	result = job.result()
	outputstate = result.get_statevector(circ[i], decimals=3)
	return outputstate
	# # print(outputstate)
	# if(abs(outputstate[0].real) == abs(sifirOutputstate[0].real) and  abs(outputstate[1].real) == abs(sifirOutputstate[1].real)):
	# 	dondur = 0
	# else:
	# 	if(abs(outputstate[0].real) == abs(birOutputstate[0].real) and  abs(outputstate[1].real) == abs(birOutputstate[1].real) ):
	# 		dondur = 1
	# 	else:
	# 		dondur = -1
	# return dondur



def bastir():
	global hamleKimde
	global oyunBittiMi
	global secilebilirMi
	global hamleKarakteri

	tumYazdir()

	screen.fill(BLACK)
	if oyunBittiMi == 1:
		screen.blit(oyunBitti, (120, 20))
	elif hamleKimde == 1:
		screen.blit(labelSiyah, (120, 20))
	else:
		screen.blit(labelBeyaz, (120, 20))

	renk = GREEN
	for i in range(4):
		for j in range(4):
			if(qbitBul(i, j) == -1):
				renk = GREEN
				print(".", end = '')
			else:
				deneme = yazdir(qbitBul(i, j))
				if deneme < 0:
					print("#", end = '')
					if deneme == -1:
						renk = GREY
					else:
						renk = DARKGREY
				else:
					print(deneme, end = '')
					if deneme == 1:
						renk = BLACK
					else:
						renk = WHITE
			pygame.draw.rect(screen,renk,((j + 1)*100, (i + 1)*100, 95, 95))
			if(qbitBul(i, j) != -1):
				stt = stateYazdir(qbitBul(i, j))
				labelState0 = kucukFont.render(str(stt[0]), 14, GREEN)
				labelState1 = kucukFont.render(str(stt[1]), 14, GREEN)
				screen.blit(labelState0, ((j + 1)*100, (i + 1)*100))
				screen.blit(labelState1, ((j + 1)*100, (i + 1)*100 + 23))

		print(end = '\n')
	if(secilebilirMi == 1):
		hamleler = ['X', 'Z', 'H']
		for i in range(3):
			if(hamleler[i] == hamleKarakteri):
				pygame.draw.rect(screen,CYAN,((i + 1)*100, (4 + 1)*100, 95, 95))
			else:
				pygame.draw.rect(screen,(255, 0, 0),((i + 1)*100, (4 + 1)*100, 95, 95))
			screen.blit(labelHarf[i], ( (i + 1)*100 + 25, (4 + 1)*100 + 20))
		return
		#4 tane kare bastir


	




# for i in range(16):
# 	print(yazdir(i))

def icerdeMi(i, j):
	#verilen kordinatin icerde olup olmadigini kontrol eder
	if(i >= 0 and j >= 0 and i < 4 and j < 4):
		return True
	return False

def qbitBul(i, j):
	if(not icerdeMi(i, j)):
		return -1
	# print(i, j)
	return loc[i][j]

def tasVarMi(i, j):
	# verilen kordinat gridin disindaysa ya da qbit yoksa false dondurur
	# print("tas varmi kontrolu = ", i, j, (icerdeMi(i, j) and qbitBul(i, j) != -1));
	return icerdeMi(i, j) and qbitBul(i, j) != -1

def git(i, j, yon):
	yoni = [0, 0, 1, -1, 1, 1, -1, -1]
	yonj = [1, -1, 0, 0, 1, -1, 1, -1]
	return i + yoni[yon], j + yonj[yon]




def qbitKoy(i, j):
	global son
	loc[i][j] = son
	son += 1

def gateYap(i, j, op):

	if(qbitBul(i, j) == -1):
		print("OLMAYAN YERI DEGISTIRMEYE CALISTIN")

	elif(op == 'X'):
		circ[qbitBul(i, j)].x(0);

	elif(op == 'H'):
		circ[qbitBul(i, j)].h(0);

	elif(op == 'Z'):
		circ[qbitBul(i, j)].z(0);

	# elif(op == 'Y'):
	# 	circ[qbitBul(i, j)].y(0);

	else:
		print("YANLIS OPERATORE GIRDIN")

def begin():
	qbitKoy(1, 1)
	qbitKoy(1, 2)
	qbitKoy(2, 1)
	qbitKoy(2, 2)

	gateYap(1, 1, 'X')
	gateYap(2, 2, 'X')

def yonluHamle(i, j, yon, koy, hamleTipi):
	# print(yon, " icin -> ", end = '')
	fl = 0

	ilki = i
	ilkj = j

	i, j = git(i, j, yon)

	# print("su anki yer = ", i, j);
	while(tasVarMi(i, j)):
		suAnkiDurum = yazdir(qbitBul(i, j))
		if(suAnkiDurum != koy):
			fl = 1
		if(suAnkiDurum == koy):
			fl += 1;
			break
		i, j = git(i, j, yon)
		# print("su anki yer = ", i, j);

	if(fl == 2):
		i = ilki
		j = ilkj

		i, j = git(i, j, yon)
		while(tasVarMi(i, j)):
			suAnkiDurum = yazdir(qbitBul(i, j))
			if(suAnkiDurum != koy):
				gateYap(i, j, hamleTipi)
			if(suAnkiDurum == koy):
				break
			i, j = git(i, j, yon)

		return 1
	else:
		return 0

def yonluKontrol(i, j, yon, koy):
	# print(yon, " icin -> ", end = '')
	fl = 0

	ilki = i
	ilkj = j

	i, j = git(i, j, yon)

	# print("su anki yer = ", i, j);
	while(tasVarMi(i, j)):
		suAnkiDurum = yazdir(qbitBul(i, j))
		if(suAnkiDurum != koy):
			fl = 1
		if(suAnkiDurum == koy):
			fl += 1;
			break
		i, j = git(i, j, yon)
		# print("su anki yer = ", i, j);

	if(fl == 2):
		return 1
	else:
		return 0

def kontrol(i, j, koy):
	fl = 0
	for y in range(8):
		if(yonluKontrol(i, j, y, koy)):
			fl = 1
	if(fl == 0):
		return False
	else:
		return True

def gecerliHamleVarMi():
	global hamleKimde
	fl = 0
	for i in range(4):
		for j in range(4):
			if(tasVarMi(i, j) == False):
				if(kontrol(i, j, hamleKimde)):
					fl = 1;
					print("HAMLE BULUNDU")
					break
		if(fl == 1):
			break
	if(fl == 0):
		return True
	else:
		return False




def hamle(i, j, koy, hamleTipi):

	global hamleKimde


	if(qbitBul(i, j) != -1):
		print("HAMLE GECERSIZZZZ")
		hamleKimde = 1 - hamleKimde
		return 0

	fl = 0
	for y in range(8):
		if(yonluHamle(i, j, y, koy, hamleTipi)):
			fl = 1
	if(fl == 0):
		print("HAMLE GECERSIZ")
		hamleKimde = 1 - hamleKimde
		return 0
	else:
		qbitKoy(i, j)
		if(koy == 1):
			gateYap(i, j, 'X')



def bilgisayarHamleYap():
	hamleler = ["X", "Z", "H"]
	random.shuffle(hamleler)
	global hamleKimde
	fl = 0
	for i in range(4):
		for j in range(4):
			if(tasVarMi(i, j) == False):
				if(kontrol(i, j, hamleKimde)):
					fl = 1;
					if(secilebilirMi == 1 or hamleKarakteri == 'R'):
						hamle(i, j, hamleKimde, randomGateVer())
					else:
						hamle(i, j, hamleKimde, hamleKarakteri)
					break
		if(fl == 1):
			break
	# if(fl == 0):
	# 	print("HAMLE BULUNAMADI\n OYUN BITTI")

hamleKimde = 1


def randomGateVer():
	hamleler = ['X', 'Z', 'H']
	random.shuffle(hamleler)
	print("Secilen hamle :" + str(hamleler[0]))
	return hamleler[0]


oyuncu = [0, 0]

def menuBastir():
	screen.fill(CYAN)
	screen.blit(labelMenu, (120, 20))
	pygame.draw.rect(screen,RED,(120, 120, 320, 70))
	screen.blit(labelOynaH, (120, 120))

	pygame.draw.rect(screen,RED,(120, 210, 320, 70))
	screen.blit(labelOynaX, (120, 210))

	pygame.draw.rect(screen,RED,(120, 300, 320, 70))
	screen.blit(labelOynaRand, (120, 300))

	pygame.draw.rect(screen,RED,(120, 390, 320, 70))
	screen.blit(labelOynaSec, (120, 390))

	pygame.draw.rect(screen,RED,(120, 480, 150, 70))
	if(oyuncu[1] == 0):
		screen.blit(labelP1, (120, 480))
	else:
		screen.blit(labelCPU1, (120, 480))

	pygame.draw.rect(screen,RED,(290, 480, 150, 70))
	if(oyuncu[0] == 0):
		screen.blit(labelP2, (290, 480))
	else:
		screen.blit(labelCPU2, (290, 480))
	# screen.blit(labelCPU2, (290, 480))

	pygame.display.flip()

fl = 0

hamleKarakteri = 'X'
secilebilirMi = 0
# oyuncu = 0

while 1:

	hamleKimde = 1
	fl = 0
	hamleKarakteri = 'X'
	secilebilirMi = 0
	loc = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]
	son = 0
	oyunBittiMi = 0

	for i in range(16):
		circ[i] = QuantumCircuit(1)

	don = 1
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		menuBastir()

		if event.type == pygame.MOUSEMOTION:
			don = 1

		if don == 1 and event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			if(pos[0] >= 120 and pos[0] <= 120 + 320 and pos[1] >= 120 and pos[1] <= 120 + 70):
				hamleKarakteri = 'H'
				fl = 1
				break

			if(pos[0] >= 120 and pos[0] <= 120 + 320 and pos[1] >= 210 and pos[1] <= 210 + 70):
				hamleKarakteri = 'X'
				fl = 1
				break

			if(pos[0] >= 120 and pos[0] <= 120 + 320 and pos[1] >= 300 and pos[1] <= 300 + 70):
				hamleKarakteri = 'R'
				fl = 1
				break

			if(pos[0] >= 120 and pos[0] <= 120 + 320 and pos[1] >= 390 and pos[1] <= 390 + 70):
				hamleKarakteri = 'X'
				secilebilirMi = 1
				fl = 1
				break

			if(pos[0] >= 290 and pos[0] <= 290 + 150 and pos[1] >= 480 and pos[1] <= 480 + 70):
				oyuncu[0] = 1 - oyuncu[0]
				don = 0
				menuBastir()
				continue

			if(pos[0] >= 120 and pos[0] <= 120 + 150 and pos[1] >= 480 and pos[1] <= 480 + 70):
				oyuncu[1] = 1 - oyuncu[1]
				don = 0
				menuBastir()
				continue



	begin()
	bastir()


	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		if oyuncu[hamleKimde] == 1:
			bilgisayarHamleYap()
			hamleKimde = 1 - hamleKimde
			bastir()
			time.sleep(1)
			if(gecerliHamleVarMi() == True):
				print("OYUN BITTI")
				oyunBittiMi = 1
				break

		if event.type == pygame.MOUSEMOTION and oyunBittiMi == 0:
			fl = 0

		if fl == 0 and event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			for i in range(1, 5):
				for j in range(1, 6):
					if(i == 4 and j == 5):
						continue
					if(pos[0] >= i*100 and pos[0] <= i*100 + 95 and pos[1] >= j*100 and pos[1] <= j*100 + 95):
						# print(j - 1, i - 1)
						if(secilebilirMi == 1 and j == 5):
							hamleler = ['X', 'Z', 'H']
							hamleKarakteri = hamleler[i - 1]
							print("yeni hamleKarakteri = " + str(hamleKarakteri))
							bastir()
							fl = 1
						else:
							if(hamleKarakteri == 'R'):
								hamle(j - 1, i - 1, hamleKimde, randomGateVer())
							else:
								hamle(j - 1, i - 1, hamleKimde, hamleKarakteri)
							hamleKimde = 1 - hamleKimde
							bastir()

							if(gecerliHamleVarMi() == True):
								print("OYUN BITTI")
								oyunBittiMi = 1
								break

							fl = 1
				if oyunBittiMi == 1:
					break

		if oyunBittiMi == 1:
			break
			# print(pos)
			# clic
		pygame.display.flip()



	bastir()
	pygame.display.flip()


	ans1 = 0;
	ans0 = 0;

	ans1 += 0;
	ans0 += 0;


	for i in range(4):
		for j in range(4):
			# print(type(i))
			# print(type(j))
			x = qbitBul(i, j)
			if(x == -1):
				continue
			print(str(i) + " " + str(j), end = " -> ")
			# tumYazdir()
			# Create a Quantum Circuit
			meas = QuantumCircuit(1, 1)
			meas.barrier(range(1))
			# map the quantum measurement to the classical bits
			meas.measure(range(1),range(1))

			# The Qiskit circuit object supports composition using
			# the addition operator.
			qc = circ[x]+meas

			#drawing the circuit
			# qc.draw(output='mpl', filename='my_circuit.png')


			# Use Aer's qasm_simulator
			backend_sim = Aer.get_backend('qasm_simulator')

			# Execute the circuit on the qasm simulator.
			# We've set the number of repeats of the circuit
			# to be 1024, which is the default.
			job_sim = execute(qc, backend_sim, shots=1024)

			# Grab the results from the job.
			result_sim = job_sim.result()


			counts = result_sim.get_counts(qc)
			print(type(counts))

			ans1 += counts.get("1", 0)
			ans0 += counts.get("0", 0)
			# for k in counts:
				# print(counts[k], end = ' ve ')

	print(ans0, ans1)

	labelans0 = myfont.render("WHITE : " + str(ans0), 14, WHITE)
	labelans1 = myfont.render("BLACK : " + str(ans1), 14, WHITE)
	screen.blit(labelans0, (75, 600))
	screen.blit(labelans1, (75, 700))

	screen.blit(oyunBitti, (120, 20))
	# pygame.draw.rect(screen,WHITE,(500, 20, 95, 95))
	# screen.blit(labelTry, (500, 20))
	pygame.display.flip()


	# {"1" = 1023}
	while 1:
		# fll = 0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				# fll = 1
				# break
				sys.exit()
		

		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			if(pos[0] >= 120 and pos[0] <= 500 and pos[1] >= 20 and pos[1] <= 95):
				fll = 1
				break
