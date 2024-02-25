from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'files'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_AUDIO_EXTENSIONS = {'wav'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename, allowed_extensions=ALLOWED_IMAGE_EXTENSIONS):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
def format_size(size):
            units = ['B', 'KB', 'MB', 'GB']
            index = 0
            while size >= 1024 and index < len(units) - 1:
                size /= 1024
                index += 1
            return f"{size:.2f} {units[index]}"

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/image')
def index_image():
    return render_template('image.html')

@app.route('/audio')
def index_audio():
    return render_template('audio.html')

@app.route('/video')
def index_video():
    return render_template('video.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/compress-image', methods=['POST'])
def post_endpoint():
    if 'image' not in request.files:
        return redirect(url_for('index_image'))
    image_file = request.files['image']
    if image_file.filename == '':
        return redirect(url_for('index'))
    image_quality = request.form['quality']
    if image_quality == '':
         image_quality = 50
    else:
        image_quality = int(image_quality)
    if image_file and allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        original_image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        compressed_image = os.path.join(app.config['UPLOAD_FOLDER'], 'compressed_' + filename)
        original_image.save(compressed_image, quality=image_quality)
        original_size = format_size(os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        compressed_size = format_size(os.path.getsize(compressed_image))
        compression_ratio = (1 - (os.path.getsize(compressed_image) / os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename)))) * 100
        compression_ratio = f"{compression_ratio:.2f}"

        return render_template('image.html',
                               original_image=url_for('uploaded_file', filename=filename), 
                               compressed_image=url_for('uploaded_file', filename='compressed_' + filename), 
                               original_size=original_size, 
                               compressed_size=compressed_size, 
                               compression_ratio=compression_ratio)
    else:
        return redirect(url_for('index_image'))
@app.route('/compress-audio', methods=['POST'])
def post_endpoint_audio():
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return redirect(url_for('index'))
    audio_quality = request.form['quality']
    if audio_quality == '':
         audio_quality = 50
    else:
        audio_quality = int(audio_quality)
    if audio_file and allowed_file(audio_file.filename, ALLOWED_AUDIO_EXTENSIONS):
        filename = secure_filename(audio_file.filename)
        audio_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        original_audio = AudioSegment.from_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        compressed_audio = os.path.join(app.config['UPLOAD_FOLDER'], 'compressed_' + filename)
        # convert quality from percentage to kbps
        audio_quality = int((audio_quality / 100) * 320)
        # convert audio to mp3
        original_audio.export(compressed_audio, format='mp3', bitrate=f"{audio_quality}k")
        original_size = format_size(os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        compressed_size = format_size(os.path.getsize(compressed_audio))
        compression_ratio = (1 - (os.path.getsize(compressed_audio) / os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename)))) * 100
        compression_ratio = f"{compression_ratio:.2f}"
        
        return render_template('audio.html',
                                 original_audio=url_for('uploaded_file', filename=filename), 
                                 compressed_audio=url_for('uploaded_file', filename='compressed_' + filename), 
                                 original_size=original_size, 
                                 compressed_size=compressed_size, 
                                 compression_ratio=compression_ratio)
    else:
        return redirect(url_for('index_audio'))
@app.route('/compress-video', methods=['POST'])
def post_endpoint_video():
    video_file = request.files['video']
    if video_file.filename == '':
        return redirect(url_for('index'))
    video_quality = request.form['quality']
    if video_quality == '':
         video_quality = 50
    else:
        video_quality = int(video_quality)
    if video_file and allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
        filename = secure_filename(video_file.filename)
        video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        original_video = VideoFileClip(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        compressed_video = os.path.join(app.config['UPLOAD_FOLDER'], 'compressed_' + filename)
        video_quality = int((video_quality / 100) * 1000)
        # convert video to mp4
        original_video.write_videofile(compressed_video, codec='libx264', audio_codec='aac', bitrate=f"{video_quality}k")
        original_size = format_size(os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        compressed_size = format_size(os.path.getsize(compressed_video))
        compression_ratio = (1 - (os.path.getsize(compressed_video) / os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename)))) * 100
        compression_ratio = f"{compression_ratio:.2f}"
        
        return render_template('video.html',
                                 original_video=url_for('uploaded_file', filename=filename), 
                                 compressed_video=url_for('uploaded_file', filename='compressed_' + filename), 
                                 original_size=original_size, 
                                 compressed_size=compressed_size, 
                                 compression_ratio=compression_ratio)
    else:
        return redirect(url_for('index_video'))
    
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')