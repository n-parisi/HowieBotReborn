import subprocess
from pydub import AudioSegment

def create_clip(yt_resource, start, duration, output_file):
    resources = str(subprocess.check_output(["youtube-dl", "-g", yt_resource])).split("\\n")
    subprocess.call(['ffmpeg', '-y', '-ss', start, '-i', resources[1], '-t', duration, '-b:a', '192k', output_file])

# Delay is in MS. Overlay all audio at interval specified by delay. Save to filesystem.
def splice_clips(clip_paths, delay):
    # Parse all clips
    clips = []
    for path in clip_paths:
        if '.wav' in path:
            clips.append(AudioSegment.from_wav(path))
        elif '.mp3' in path:
            clips.append(AudioSegment.from_mp3(path))

    # Determine duration of new sound
    new_duration = 0
    for i in range(len(clips)):
        clip = clips[i]
        clip_len = len(clip) + delay*i
        if clip_len > new_duration:
            new_duration = clip_len

    # Create silent sound, overlay other sounds on top
    final_sound = AudioSegment.silent(duration=new_duration)
    for i in range(len(clips)):
        clip = clips[i]
        pos = delay*i
        final_sound = final_sound.overlay(clip, position=pos)

    # Save the final result
    final_sound.export('resources/tmp.mp3', format='mp3')



    