import os
import random
import string
from moviepy.editor import VideoFileClip, concatenate_videoclips
from fractions import Fraction

class VideoClipper:
    def __init__(self, video_path, fps, size_scale, clip_length, format):
        self.video_path = video_path
        self.fps = fps
        self.size_scale = size_scale
        self.clip_length = clip_length
        self.format = format

    def process_audio(self, clip, start, end):
        """Process the audio of a clip."""
        if clip.audio:  # if the video has an audio track
            audio_subclip = clip.audio.subclip(start, end)  # get the corresponding audio segment
            return audio_subclip  # return the audio subclip
        return None  # if no audio, return None

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
        clip_rotation = clip.rotation
        chunks = duration // self.clip_length
        original_res = (clip.w, clip.h)
        aspect_ratio = str(Fraction(clip.aspect_ratio))
        target_resolution = (int(clip.w * self.size_scale), int(clip.h * self.size_scale))

        # Extract the original name without its extension
        original_name = os.path.splitext(os.path.basename(self.video_path))[0]

        for i in range(int(chunks)):
            start = i * self.clip_length
            end = start + self.clip_length

            # Update the output filename using the desired format
            output_filename = f"{original_name}_clip_{i}.{self.format}"
            output_path = os.path.join(self.output_dir, output_filename)

            if end < duration:
                subclip = clip.subclip(start, end)
                if clip_rotation in (90, 270):
                    subclip_resized = subclip.resize([target_resolution[1], target_resolution[0]])
                else:
                    subclip_resized = subclip.resize(target_resolution)
                audio_subclip = self.process_audio(clip, start, end)  # process the audio
                if audio_subclip:  # if there is audio
                    subclip_resized = subclip_resized.set_audio(audio_subclip)  # set the audio to the subclip
                if self.format == 'gif':
                    subclip_resized.write_gif(output_path, fps=self.fps)
                elif self.format == 'mp4':
                    subclip_resized.write_videofile(output_path, fps=self.fps, threads=12)

    def process_video(self):
        if self.check_video_file():
            self.create_output_dir()
            self.create_subclips()

def main():
    video_path = input("Enter the path to the video file: ").strip('\"')
    fps = int(input("Enter the frame rate: "))
    size_scale = float(input("Enter the size scale (1 for original size, 0.5 for half, etc.): "))
    clip_length = int(input("Enter the clip length in seconds: "))
    format = input("Enter the output format (gif or mp4): ")
    clipper = VideoClipper(video_path, fps, size_scale, clip_length, format)
    clipper.process_video()

if __name__ == "__main__":
    main()
