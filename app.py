from flask import Flask, render_template, jsonify, request
from processor import Processor, simulate_code

app = Flask(__name__)
processor = Processor()

@app.route('/')
def index():
    return render_template('index.html', memory=processor.memory, registers=processor.registers, memoria_instructions=processor.memoria_instructions, instruction='None', mpc=processor.mpc)

@app.route('/start_instruction', methods=['POST'])
def start_instruction():
    if len(processor.memoria_instructions) > 1 and processor.mpc < len(processor.memoria_instructions) - 1:
        instruction = processor.memoria_instructions[processor.mpc]
        processor.instructions.update(instruction)

        processor.process_instruction()

        memory, registers = simulate_code(processor)
        return jsonify({'memory': memory, 'registers': registers})
    else:
        return jsonify({''}), 400

@app.route('/reset')
def reset():
    processor.reset()
    memory, registers = simulate_code(processor)
    return jsonify({'memory': memory, 'registers': registers, 'memoria_instructions': processor.memoria_instructions,'instruction': 'None'})

@app.route('/file')
def file():
    processor.load_instructions_from_file('microinstructions.json')
    memory, registers = simulate_code(processor)
    return jsonify({'memory': memory, 'registers': registers, 'memoria_instructions': processor.memoria_instructions,'instruction': 'None'})

@app.route('/store_instruction', methods=['POST'])
def store_instruction():
    new_instruction = {
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
    new_instruction['AMUX'] = int(request.form['amux'])
    new_instruction['COND'] = int(request.form['cond'])
    new_instruction['ALU'] = int(request.form['alu'])
    new_instruction['SH'] = int(request.form['sh'])
    new_instruction['MBR'] = int(request.form['mbr'])
    new_instruction['MAR'] = int(request.form['mar'])
    new_instruction['RD'] = int(request.form['rd'])
    new_instruction['WR'] = int(request.form['wr'])
    new_instruction['ENC'] = int(request.form['enc'])
    new_instruction['C'] = int(request.form['c'])
    new_instruction['B'] = int(request.form['b'])
    new_instruction['A'] = int(request.form['a'])
    new_instruction['ADDR'] = int(request.form['addr'])
    processor.store_instruction(new_instruction)

    memory, registers = simulate_code(processor)
    return jsonify({'memory': memory, 'registers': registers, 'memoria_instructions': processor.memoria_instructions})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)

