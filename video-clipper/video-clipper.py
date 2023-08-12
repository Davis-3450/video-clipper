import os
import random
import string
from moviepy.editor import VideoFileClip

class VideoClipper:
    def __init__(self, video_path, fps, size_scale, clip_length, output_format):
        self.video_path = video_path
        self.fps = fps
        self.size_scale = size_scale
        self.clip_length = clip_length
        self.output_format = output_format

    def random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def check_video_file(self):
        if not os.path.isfile(self.video_path):
            print("The specified video file does not exist.")
            return False
        return True

    def create_output_dir(self):
        base_name = os.path.basename(self.video_path)
        base_name_without_ext = os.path.splitext(base_name)[0]
        self.output_dir = os.path.join(os.path.dirname(self.video_path), base_name_without_ext)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def create_subclips(self):
        clip = VideoFileClip(self.video_path)
        duration = clip.duration
        chunks = duration // self.clip_length
        for i in range(int(chunks)):
            start = i * self.clip_length
            end = start + self.clip_length
            output_filename = self.random_string(10) + '.' + self.output_format
            output_path = os.path.join(self.output_dir, output_filename)
            if end < duration:
                subclip = clip.subclip(start, end)
                subclip_resized = subclip.resize(height=int(subclip.h * self.size_scale))
                if self.output_format == 'gif':
                    subclip_resized.write_gif(output_path, fps=self.fps)
                elif self.output_format == 'mp4':
                    subclip_resized.write_videofile(output_path, fps=self.fps)
                subclip.close()
        clip.close()

    def process_video(self):
        if self.check_video_file():
            self.create_output_dir()
            self.create_subclips()

def main():
    video_path = input("Enter the path to the video file: ")
    fps = int(input("Enter the frame rate: "))
    size_scale = float(input("Enter the size scale (1 for original size, 0.5 for half, etc.): "))
    clip_length = int(input("Enter the clip length in seconds: "))
    output_format = input("Enter the output format (gif or mp4): ")
    clipper = VideoClipper(video_path, fps, size_scale, clip_length, output_format)
    clipper.process_video()

if __name__ == "__main__":
    main()
