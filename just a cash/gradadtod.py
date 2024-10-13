import cv2
import mediapipe as mp

# Initialize mediapipe face mesh solution
mp_face_mesh = mp.solutions.face_mesh #face mesh which rich for

face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)  

mp_drawing = mp.solutions.drawing_utils #tool for drawing just part list of landmarks

# Open webcam for video capture
def detection():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Convert frame to RGB which mediapipe expects 
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #throw it to model
        results = face_mesh.process(frame_rgb)

        if results.multi_face_landmarks: #just to make sure that webcam can cap face

            #part of drawing
            #for face_landmarks in results.multi_face_landmarks:
                #mp_drawing.draw_landmarks(frame, face_landmarks)

            face_landmarks = results.multi_face_landmarks
            # Example: Eye blink detection using eye landmarks
            left_eye_blink = abs(face_landmarks.landmark[159].y - face_landmarks.landmark[145].y)
            right_eye_blink = abs(face_landmarks.landmark[386].y - face_landmarks.landmark[374].y)
            if left_eye_blink < 0.015 or right_eye_blink < 0.015 :  # Threshold to detect blink
                return 0

            # Example: Mouth opening detection
            mouth_open = abs(face_landmarks.landmark[13].y - face_landmarks.landmark[14].y)
            if mouth_open > 0.05:  # Threshold to detect mouth open
                return 1

        # Display the frame with landmarks drawn
        cv2.imshow('Gesture Detection', frame)
       

    cap.release()
    cv2.destroyAllWindows()