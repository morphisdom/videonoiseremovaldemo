from moviepy.editor import VideoFileClip
from scipy.io import wavfile
import noisereduce as nr
import subprocess

########## download sample video file
!wget https://github.com/morphisdom/videonoiseremovaldemo/raw/main/sample/demovideo.mp4

########### extract audio from video
videoclip = VideoFileClip("./demovideo.mp4")
videoclip.audio.write_audiofile('audio.wav',fps=16000,bitrate='96k',nbytes=2,verbose=False)

########### Remove noise from audio

rate, data = wavfile.read('audio.wav')
if len(data.shape) > 1:
	data = data[:, 0]

reduced_noise = nr.reduce_noise(y=data, sr=rate) ### this consumes lot of memory. You may need to break into chunks for longer duration of audio.
wavfile.write('nraudio.wav', rate, reduced_noise)

########## Merge audio and video
subprocess.call(['ffmpeg','-i',"./demovideo.mp4" , '-i', 'nraudio.wav', '-map', '0:v0', '-map', '1:a:0', '-c:v', 'copy', '-shortest', '-threads','2','outvideo.mp4'])

