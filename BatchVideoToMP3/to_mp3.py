from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def batch_convert_to_mp3_moviepy(input_folder, output_folder="."):
    """
    Batch converts all .webm and .mp4 files in the input folder to MP3 files
    in the output folder using moviepy.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    supported_extensions = (".webm", ".mp4")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_extensions):
            input_path = os.path.join(input_folder, filename)
            output_name = os.path.splitext(filename)[0] + ".mp3"
            output_path = os.path.join(output_folder, output_name)

            try:
                video = VideoFileClip(input_path)
                audio = video.audio
                if audio:  # Check if the video has an audio track
                    audio.write_audiofile(output_path)
                    audio.close()
                    video.close()
                    print(f"Successfully converted: {filename} -> {output_name}")
                else:
                    video.close()
                    print(f"Warning: No audio track found in {filename}. Skipping.")
            except Exception as e:
                print(f"Error converting {filename}: {e}")

if __name__ == "__main__":
    input_directory = "F:/FilesHD/_Downloads/templusca2"  # Replace with the actual path
    output_directory = "F:/FilesHD/_Downloads/templusca2/output"    # Optional: Specify an output folder

    batch_convert_to_mp3_moviepy(input_directory, output_directory)