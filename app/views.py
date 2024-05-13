from flask import Flask, request, render_template, redirect, url_for, flash, session, send_file, jsonify
import os
from app import app
from app.my_rsa import encrypt_file, decrypt_file
from app.my_rc4 import RC4
from datetime import datetime
import time
from memory_profiler import memory_usage
import binascii


app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/rsa', methods=['GET', 'POST'])
def rsa():
    execution_time = 0
    memory_used = 0
    file_size = 0
    word_count = 0
    if request.method == 'POST':
        file = request.files['file']
        action = request.form.get('action')
        if file:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            now = datetime.now()
            formatted_time = now.strftime("%H_%M_%S-%d_%m_%Y")

            start_time = time.time()
            initial_memory_usage = memory_usage(-1, interval=0.1, timeout=1)

            new_filename = f"rsa_{action}-{formatted_time}.txt"
            result_path = os.path.join(UPLOAD_FOLDER, new_filename)
            file.save(result_path)

            if action == 'encrypt':
                result_data = encrypt_file(result_path)
            else:  # decrypt
                result_data = decrypt_file(result_path)

            end_time = time.time()
            final_memory_usage = memory_usage(-1, interval=0.1, timeout=1)

            execution_time = round(end_time - start_time, 4)
            memory_used = round(max(final_memory_usage) - min(initial_memory_usage), 4)

            file_size = os.path.getsize(result_path)
            word_count = len(open(result_path, 'rb').read().split())

            with open(result_path, 'wb') as f:
                f.write(result_data)

            return jsonify({
                    'execution_time': execution_time,
                    'memory_used': memory_used,
                    'file_size': file_size,
                    'word_count': word_count
                })
        
    # Load the initial page with default values
    return render_template('rsa.html')

@app.route('/rc4', methods=['GET', 'POST'])
def rc4():
    execution_time = 0
    memory_used = 0
    file_size = 0
    word_count = 0
    if request.method == 'POST':
        file = request.files['file']
        key = request.form['key'].encode()  # Assuming key is input as a string
        action = request.form.get('action')

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        now = datetime.now()
        formatted_time = now.strftime("%Y%m%d%H%M%S")
        new_filename = f"rc4_{action}-{formatted_time}.txt"
        file_path = os.path.join(UPLOAD_FOLDER, new_filename)
        file.save(file_path)

        start_time = time.time()  # Memulai pengukuran waktu
        initial_memory_usage = memory_usage(max_usage=True)  # Memulai pengukuran memori

        if action == 'encrypt':
            result_data = RC4(file_path, key)
        elif action == 'decrypt':
            result_data = RC4(file_path, key)

        # result_path = os.path.join(UPLOAD_FOLDER, f"rc4_{action}-result-{formatted_time}.txt")

        end_time = time.time()  # Mengakhiri pengukuran waktu
        final_memory_usage = memory_usage(max_usage=True)  # Mengakhiri pengukuran memori

        file_size = os.path.getsize(file_path)
        word_count = len(open(file_path, 'rb').read().split())

        # Menghitung selisih waktu dan penggunaan memori
        execution_time = round(end_time - start_time, 4)
        memory_used = round(final_memory_usage - initial_memory_usage, 4)

        with open(file_path, 'wb') as f:
            f.write(binascii.unhexlify(result_data))

        return jsonify({
                    'execution_time': execution_time,
                    'memory_used': memory_used,
                    'file_size': file_size,
                    'word_count': word_count
                })
    
        response = send_file(file_path, as_attachment=True)
        response.headers['Waktu-eksekusi'] = f"{execution_time} Detik"
        response.headers['Penggunaan-Memori'] = f"{memory_used} MB"
        response.headers['Ukuran-Berkas'] = f"{file_size} bytes"
        response.headers['Jumlah-Kata'] = f"{word_count} kata"

        return response

        # return send_file(file_path, as_attachment=True)
    return render_template('rc4.html')