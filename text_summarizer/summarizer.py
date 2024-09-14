from underthesea import word_tokenize
import numpy as np
import re
import networkx as nx
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from googletrans import Translator
import requests

def tokenize_sentences(text):
    return [word_tokenize(sentence) for sentence in re.split(r'(?<=[.!?]) +', text) if sentence]

def build_similarity_matrix(sentences):
    matrix = np.zeros((len(sentences), len(sentences)))

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                # Sử dụng sự tương đồng cosine dựa trên từ vựng chung giữa các câu
                words_i = set(sentences[i])
                words_j = set(sentences[j])
                common_words = words_i.intersection(words_j)
                if len(common_words) > 0:
                    matrix[i][j] = len(common_words) / (np.log(len(words_i)) + np.log(len(words_j)))

    return matrix

def summarize_text(text, num_sentences=5):
    sentences = tokenize_sentences(text)

    if not sentences or all(len(sentence) == 0 for sentence in sentences):
        return "Không có đủ dữ liệu để tạo tóm tắt."

    similarity_matrix = build_similarity_matrix(sentences)

    # Chuyển ma trận tương đồng thành đồ thị
    graph = nx.from_numpy_array(similarity_matrix)

    # Áp dụng TextRank để tính toán xếp hạng các câu
    scores = nx.pagerank(graph)

    # Sắp xếp các câu dựa trên điểm số
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    # Chọn các câu có thứ hạng cao nhất
    summary = ' '.join([' '.join(sentence) for _, sentence in ranked_sentences[:num_sentences]])
    return summary

def video_to_audio(video_file, audio_file):
    video = VideoFileClip(video_file)
    video.audio.write_audiofile(audio_file)
    video.close()  # Đảm bảo tệp video được đóng trước khi xóa
    return audio_file

def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language='vi-VN')
        return text
    except sr.UnknownValueError:
        return "Không thể nhận dạng giọng nói trong file âm thanh"
    except sr.RequestError as e:
        return f"Lỗi khi yêu cầu dịch vụ Nhận dạng giọng nói: {e}"

def translate(text,to):
    translator = Translator()
    res = ""
    # Dịch từ tiếng Việt sang tiếng Anh
    if to == "en" :
        translated_text_en = translator.translate(text, src='vi', dest='en')
        res = translated_text_en.text

    # Dịch từ tiếng Anh sang tiếng Việt
    if to == "vi":
        translated_text_vi = translator.translate(text, src='en', dest='vi')
        res = translated_text_vi.text
    return res

def DanhDauCau(text):
    # URL mà bạn muốn gửi yêu cầu POST
    url = 'http://bark.phon.ioc.ee/punctuator'

    # Dữ liệu gửi đi (dưới dạng dictionary)
    data = {
        'text': text
    }

    # Gửi yêu cầu POST
    response = requests.post(url, data=data)

    return response.text