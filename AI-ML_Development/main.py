from KeyFrameExtractorClass import KeyFrameExtractor
from VectorNormalizer import VectorNormalizer
import cv2

videoRute = "C:\\Users\\48519558\\Desktop\\SignAI-ML\\AI-ML_Development\\recursos\\videoprueba2.mp4"
video = cv2.VideoCapture(videoRute)

KFE = KeyFrameExtractor()

handPointsKeyFrames = KFE.extractKeyFrames(False, video, 3)
print(handPointsKeyFrames[0]) # Falta ver
# if handPointsKeyFrames:
#     normalizer = VectorNormalizer(4)
#     for hand_landmarks in handPointsKeyFrames:
#         zPoints = hand_landmarks[:,2]
#         normalizedZPoints = VectorNormalizer.normalizeVector(VectorNormalizer, zPoints)
#         hand_landmarks[:,2] = normalizedZPoints
#         print("Processed Landmarks:")
#         print(hand_landmarks)
