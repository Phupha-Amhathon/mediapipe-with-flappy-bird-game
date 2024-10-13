import cv2
import mediapipe as mp



class NoseTracking: # for dog
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces = 1)
        #self.mp_draw = mp.solutions.drawing_utils 
        self.face_landmarks = None
        self.nose_position_x = None
        self.nose_position_y = None 
        self.frame = None

    def process_frame(self,frame):
        frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        self.face_landmarks = results.multi_face_landmarks
        if self.face_landmarks:
            self.nose_position_x = (self.face_landmarks[0].landmark[4].x)*800
            self.nose_position_y = (self.face_landmarks[0].landmark[4].y)*600        
        #return frame
        #no need to use processed frame


class EyesTracking: 
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces = 1)
        self.mp_draw = mp.solutions.drawing_utils
        self.face_landmarks = None
        self.eye_state = None
       
        
    def process_frame(self,frame):
        frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        self.face_landmarks = results.multi_face_landmarks
        if self.face_landmarks:
            top_right_eye_position_y = self.face_landmarks[0].landmark[386].y
            low_right_eye_position_y = self.face_landmarks[0].landmark[374].y
            top_left_eye_position_y = self.face_landmarks[0].landmark[159].y
            low_left_eye_position_y = self.face_landmarks[0].landmark[145].y
            if abs(top_right_eye_position_y - low_right_eye_position_y) <0.02 or abs(top_left_eye_position_y - low_left_eye_position_y) <0.02:
                self.eye_state = 'closed'

            else:
                self.eye_state = 'open'

class MountTracking: #for hippo
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces = 1)
        self.face_landmarks = None
        self.mount_state = None
        
    def process_frame(self,frame):
        frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        self.face_landmarks = results.multi_face_landmarks
        if self.face_landmarks:
            top_lip_position_x = self.face_landmarks[0].landmark[13].y
            low_lip_position_x = self.face_landmarks[0].landmark[14].y
            if abs(top_lip_position_x - low_lip_position_x) <0.01:
                self.mount_state = 'closed'
            else:
                self.mount_state = 'open'
        

class HandTracking: #for capybara
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.hand_landmarks = None
        self.index_finger_position_x = None #return(x,y)
        self.index_finger_position_y = None #return(x,y)

    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        self.hand_landmarks = results.multi_hand_landmarks
        if self.hand_landmarks:
            self.index_finger_position_x = ((self.hand_landmarks[0].landmark[8].x)*800)
            self.index_finger_position_y = ((self.hand_landmarks[0].landmark[8].y)*600)


class PoseTracking: #for bird (demo)
    def __init__(self):
        self.mp_pose = mp.solutions.pose #aceess modul
        self.pose = mp.solutions.pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) #acess class
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.pose_landmarks = None

        self.previous_right_wrist_y = None
        self.previous_left_wrist_y = None
        self.flap_threshold = 0.18  # Adjust this value to fine-tune flapping sensitivity
        
        self.flap_state = 0
    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)
        self.pose_landmarks = results.pose_landmarks

        

        if self.pose_landmarks:
            self.mp_draw.draw_landmarks(
            frame, 
            self.pose_landmarks, 
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
        )
            landmarks = self.pose_landmarks.landmark
            
            
            # Get coordinates of shoulders and wrists
            left_elbow = landmarks[13]
            right_elbow = landmarks[14]
            left_shoulder = landmarks[11]
            right_shoulder = landmarks[12]
            # Step 2: Check if the elbows are raised above the shoulders (y-coordinate check)
            def is_raised(elbow, shoulder):
            # Check if elbow's y-coordinate is above the shoulder's y-coordinate (remember: y=0 is top of the image)
                
                return abs(shoulder.y - elbow.y) < self.flap_threshold
            
            
            left_elbow_raised = is_raised(left_elbow, left_shoulder)
            right_elbow_raised = is_raised(right_elbow, right_shoulder)
            # Final check: Are both elbows raised?
            if left_elbow_raised and right_elbow_raised:
                self.flap_state =  'raise'
            else:
                self.flap_state = 'down'
            

            ############################red################################


'''
puss= PoseTracking()
md = MediapipeThread(puss)
md.start()
'''