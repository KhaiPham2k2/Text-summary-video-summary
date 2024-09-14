from flask import Flask, render_template, request, redirect, url_for, session, flash
from summarizer import summarize_text, video_to_audio, audio_to_text,translate,DanhDauCau
from users import UserManager
from werkzeug.utils import secure_filename
import os
import tempfile

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'mộichuỗingẫunhiêndàivàan toàn')
app.config['UPLOAD_FOLDER'] = 'D:\\DATN\\pythonProject\\video'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.before_request
def before_request():
    if 'initialized' not in session:
        UserManager.add_user('users', 'password')
        session['initialized'] = True

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    data_folder = 'D:\\DATN\\pythonProject\\text_summarizer\\clusters\\DATA'
    files = [f for f in os.listdir(data_folder) if f.endswith('.txt')]

    if request.method == 'POST':
        choice = request.form['choice']
        if choice == 'reset':
            return render_template('index.html', original_text='', summary='', files=files)
        elif choice == 'direct_input':
            text = request.form['text']
            summarized_text = summarize_text(text)
        elif choice == 'choose_file':
            selected_file = request.form['file_select']
            file_path = os.path.join(data_folder, selected_file)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            summarized_text = summarize_text(text)
        elif choice == 'upload_video':
            video = request.files['video']
            if video:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
                    video_file = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(video.filename))
                    video.save(video_file)
                    audio_file = video_to_audio(video_file, temp_audio_file.name)
                    text = audio_to_text(audio_file)
                    textEn = translate(text,to = "en")
                    textEn = DanhDauCau(textEn)
                    textVi2 =translate(textEn,to= "vi")
                    summarized_text = summarize_text(textVi2)
                    summarized_text = summarize_text(summarized_text)
                    try:
                        os.remove(audio_file)
                        os.remove(video_file)
                    except PermissionError:
                        flash('Không thể xóa tệp âm thanh vì nó đang được sử dụng bởi một tiến trình khác.', 'error')
            else:
                flash('Vui lòng tải lên một file video', 'error')
                return redirect(request.url)

        return render_template('index.html', original_text=text, summary=summarized_text, files=files)

    return render_template('index.html', original_text='', summary='', files=files)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if UserManager.validate_user(username, password):
            session['username'] = username
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not UserManager.validate_user(username, password):
            UserManager.add_user(username, password)
            flash('Chúc mừng bạn, đăng ký thành công!', 'success')

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
