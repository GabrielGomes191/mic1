# processor.py
from random import randint

from flask import json
class Processor:
    def __init__(self):
        self.reset()

    def reset(self):
        self.registers = {
            'PC': 0,
            'AC': 0,
            'SP': 0,
            'IR': 0,
            'TIR': 0,
            '0': 0,
            '+1': 1,
            '-1': -1,
            'AMASK': 0,
            'SMASK': 0,
            'A': 0,
            'B': 0,
            'C': 0,
            'D': 0,
            'E': 0,
            'F': 0,
            'MAR': 0,
            'MBR': 0,
            'AMUX': 0,
            'ALU': [0,0],
            'Deslocador': 0,
            'Latch A': 0,
            'Latch B': 0
        }
        self.memory = [0] * 10  # Memory with 16 addresses
        self.instruction_pointer = 0
        self.instructions = {
            'AMUX': 0,
            'COND': 0,
            'ALU': 0,
            'SH': 0,
            'MBR': 0,
            'MAR': 0,
            'RD': 0,
            'WR': 0,
            'ENC': 0,
            'C': 0,
            'B': 0,
            'A': 0,
            'ADDR': 0,
        }
        self.memoria_instructions = [self.instructions.copy()]
        self.x = [randint(0,99) for i in range(0, 12)]

        # Initial values in memory
        self.memory[1:11] = self.x

        self.mpc = 1

    def store_instruction(self, values):
        self.memoria_instructions.append(values)

    def load_instructions_from_file(self, filename):
        self.memory[0] = 6 #n
        self.memory[1] = 3 #i
        self.memory[2] = 10 #y
        with open(filename, 'r') as f:
            data = json.load(f)
            for inst in data['instructions']:
                instruction = {
                    'AMUX': inst['AMUX'],
                    'COND': inst['COND'],
                    'ALU': inst['ALU'],
                    'SH': inst['SH'],
                    'MBR': inst['MBR'],
                    'MAR': inst['MAR'],
                    'RD': inst['RD'],
                    'WR': inst['WR'],
                    'ENC': inst['ENC'],
                    'C': inst['C'],
                    'B': inst['B'],
                    'A': inst['A'],
                    'ADDR': inst['ADDR'],
                }
                self.store_instruction(instruction)


    # mar = pc; rd alu 2 mar 1 rd 1
    def process_instruction(self):
        #controla a entrada esquerda da ALU
        if self.instructions['AMUX'] == 0:
            #latch A
            #colocar os conteúdos dos registradores nos barramentos A e armazena-los nos latches A
            for r,i in  enumerate(self.registers):
                if r == self.instructions['A']:
                    self.registers['Latch A'] = self.registers[i]

            self.registers['ALU'][0] = self.registers['Latch A']
            pass
        else:
            #MBR
            self.registers['ALU'][0] = self.registers['MBR']
            pass     
        #colocar os conteúdos dos registradores nos barramentos B e armazena-los nos latch B
        for r,i in  enumerate(self.registers):
            if r == self.instructions['B']:
                self.registers['Latch B'] = self.registers[i]
        self.registers['ALU'][1] = self.registers['Latch B']

        #função da ALU
        if self.instructions['ALU'] == 0:
            # A + B
            self.registers['Deslocador'] = self.registers['ALU'][0] + self.registers['ALU'][1] #operador de comparação bit a bit

        elif self.instructions['ALU'] == 1:
            # A . B
            self.registers['Deslocador'] = self.registers['ALU'][0] & self.registers['ALU'][1] #operador de comparação bit a bit

        elif self.instructions['ALU'] == 2:
            # A
            self.registers['Deslocador'] = self.registers['ALU'][0]
            pass
        else:
            # !A
            self.registers['Deslocador'] = ~(self.registers['ALU'][0])
            pass

        if self.registers['Deslocador']<0:
            self.registers['N'] = 1
        else:
            self.registers['N'] = 0

        if self.registers['Deslocador'] == 0:
            self.registers['Z'] = 1
        else:
            self.registers['Z'] = 0

        print('Deslocador: ',self.registers['Deslocador'], 'N:', self.registers['N'])

        #COND: diz se vai ocorrer um desvio ou não
        if self.instructions['COND'] == 0:
            #não desvia
            self.mpc+=1
            pass
        elif self.instructions['COND'] == 1:
            if self.registers['N'] == 0:
                self.mpc+=1
                pass
            else:
                #self.instrucoes = self.memoria_instrucoes[self.instructions['ADDR']]
                self.mpc = self.instructions['ADDR']
                pass
        elif self.instructions['COND'] == 2:
            if self.registers['Z'] == 0:
                self.mpc+=1
                pass
            else:
                #self.instrucoes = self.memoria_instrucoes[self.instructions['ADDR']]
                self.mpc = self.instructions['ADDR']
                pass
        else:
            #self.instrucoes = self.memoria_instrucoes[self.instructions['ADDR']]
            self.mpc = self.instructions['ADDR']
            pass

        #função do deslocador
        if self.instructions['SH'] == 0:
            #nenhum deslocamento
            pass
        elif self.instructions['SH'] == 1:
            #deslocamento a direita
            self.registers['Deslocador'] >>= 1
        else:
            #deslocamento a esquerda
            self.registers['Deslocador'] <<= 1

        #carrega MBR a partir do deslocador
        if self.instructions['MBR'] == 0:
            #nao carrega
            pass
        else:
            self.registers['MBR'] = self.registers['Deslocador']

        #carrega MAR a partir do latch B
        if self.instructions['MAR'] == 0:
            #nao carrega
            pass
        else:
            self.registers['MAR'] = self.registers['Latch B']

        #requisita leitura de memória
        if self.instructions['RD'] == 0:
            #nenhuma leitura
            pass
        else:
            #salva o conteudo da memoria no mbr
            self.registers['MBR'] = self.memory[self.registers['MAR']]
            pass

        #requisita escrita na memória
        if self.instructions['WR'] == 0:
            #nenhuma escrita
            pass
        else:
            #escreve o conteúdo de MBR na memória
            self.memory[self.registers['MAR']] = self.registers['MBR']
            

        #controla armazenamento na memória de rascunho
        if self.instructions['ENC'] == 0:
            #nao armazena
            pass
        else:
            #armazenar no registrador com indice do campo c o conteudo do deslocador
            for r,i in  enumerate(self.registers):
                if r == self.instructions['C']:
                    self.registers[i] = self.registers['Deslocador']
        pass
    def update(self, instructions):
        self.instrucoes = instructions

    def step(self):
        pass

    def update_registers(self):
        pass


def simulate_code(processor):
    memory, registers = processor.memory, processor.registers
    return memory, registers
