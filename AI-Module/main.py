from Modules.KeyFrameExtractorClass import KeyFrameExtractor
from Modules.Points2VecClass import Point2Vec
import cv2
import os
import subprocess
from pathlib import Path


def main(path:str) -> str:
    return "Hello World"
    path = Path(path)
    kfe = KeyFrameExtractor()
    normalizer = Point2Vec(4)
    
    try:
        #Use ffmpeg to filter video frames
        
        path = ffmpeg_video(path)
        
        #Create video object
        
        video = cv2.VideoCapture(str(path))
        
        #Extract video features
        
        video_features = kfe.extractKeyFrames(return_frame=False, draw=False, video=video)
        
        #Normalize video features
        
        normalized_video_features = normalizer.land2vec(video_features)
        
    except Exception as e:
        return "Error translating"

def ffmpeg_video(path: str) -> Path:
    if path.suffix == ".mp4":
        folder = path.parent
        file_name = path.name
        output_path = folder / f"filtered_{file_name}"
        
        # Comando ffmpeg
        command = [
            "ffmpeg", 
            "-i", str(path), 
            "-vf", r"select=not(mod(n\,3))", 
            "-vsync", "vfr", 
            "-c:v", "libx264", 
            str(output_path)
        ]
        subprocess.run(command, check=True)
        return output_path
    else:
        raise Exception("Invalid file format")

if __name__ == "__main__":
    path = input("Enter the path of the video: ")
    print(main(path))