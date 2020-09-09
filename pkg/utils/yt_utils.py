import subprocess


def create_clip(yt_resource, start, duration, output_file):
    resources = str(subprocess.check_output(["youtube-dl", "-g", yt_resource])).split("\\n")
    subprocess.call(['ffmpeg', '-y', '-ss', start, '-i', resources[1], '-t', duration, '-b:a', '192k', output_file])
