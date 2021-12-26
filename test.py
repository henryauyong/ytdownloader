import ffmpeg

input_video = ffmpeg.input('input_video.mp4')

input_audio = ffmpeg.input('input_audio.mp4')

ffmpeg.concat(input_video, input_audio, v=1, a=1).output('finished_video.mp4').run()