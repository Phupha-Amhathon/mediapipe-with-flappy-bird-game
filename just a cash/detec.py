import cv2
import mediapipe as mp
import threading
import pygame
import time

class MediapipeThread01(threading.Thread): #make this to be a children class thread ,for allowing start() to starting a new thread
    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.running = True 
        self.cap = cv2.VideoCapture(0)   
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

    def run(self):  #specific name This f will run when start() was called
        while self.running:
            ret, frame = self.cap.read()
            frame = cv2.flip(frame,1)
            if ret:
                processed_frame = self.mode.process_frame(frame)
                cv2.imshow("Hand Tracking", processed_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False

    def stop(self):
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()

class MediapipeThread(threading.Thread): #make this to be a children class thread ,for allowing start() to starting a new thread
    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.running = True 
        self.cap = cv2.VideoCapture(0)   
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        self.frame_bgr = None
    def run(self):  #specific name This f will run when start() was called
        while self.running:
            ret, frame = self.cap.read()
            frame = cv2.flip(frame,1)
            if ret:
                processed_frame = self.mode.process_frame(frame)
                #self.frame_bgr = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)
                self.frame_bgr =pygame.image.frombuffer(processed_frame.tobytes(), (800,600), "BGR")
                # cv2.imshow("Hand Tracking", processed_frame)
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                    #self.running = False
    def stop(self):
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()

class NoseTracking:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces = 1)
        self.mp_draw = mp.solutions.drawing_utils
        self.face_landmarks = None
        self.nose_position_x = None  
        self.nose_position_y = None
        

    def process_frame(self,frame):
        frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        self.face_landmarks = results.multi_face_landmarks
        if self.face_landmarks:
            self.nose_position_x = (self.face_landmarks[0].landmark[4].x)*800
            self.nose_position_y = (self.face_landmarks[0].landmark[4].y)*600           

        return frame

class EyesTracking:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces = 1)
        self.mp_draw = mp.solutions.drawing_utils
        self.face_landmarks = None
        self.left_eye_state = None
        self.right_eye_state = None
        
    def process_frame(self,frame):
        frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        self.face_landmarks = results.multi_face_landmarks
        if self.face_landmarks:
            top_right_eye_position_y = self.face_landmarks[0].landmark[386].y
            low_right_eye_position_y = self.face_landmarks[0].landmark[374].y
            top_left_eye_position_y = self.face_landmarks[0].landmark[159].y
            low_left_eye_position_y = self.face_landmarks[0].landmark[145].y
            if abs(top_right_eye_position_y - low_right_eye_position_y) <0.02:
                self.right_eye_state = 'closed'

            else:
                self.right_eye_state = 'open'


            if abs(top_left_eye_position_y - low_left_eye_position_y) <0.02:
                self.left_eye_state = 'closed'
            else:
                self.left_eye_state = 'open'
        return frame

class MountTracking:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces = 1)
        self.mp_draw = mp.solutions.drawing_utils
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
        return frame

def MountTracking01():
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces = 1)
    mp_draw = mp.solutions.drawing_utils
    face_landmarks = None
    mount_state = None
        

    def process_frame(frame):
        frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        face_landmarks = results.multi_face_landmarks
        if face_landmarks:
            top_lip_position_x = face_landmarks[0].landmark[13].y
            low_lip_position_x = face_landmarks[0].landmark[14].y
            if abs(top_lip_position_x - low_lip_position_x) <0.01:
                mount_state = 'closed'
            else:
                mount_state = 'open'
        return frame


class HandTracking:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.mp_draw = mp.solutions.drawing_utils
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
            cx =int(self.index_finger_position_x*200/400)
            cy = int(self.index_finger_position_y*240/600)



            ############################red################################
        return frame

class PoseTracking:
    def __init__(self):
        self.mp_pose = mp.solutions.pose #aceess modul
        self.mp_pose = mp.solutions.pose.Pose() #acess class
        self.mp_draw = mp.solutions.drawing_utils
        self.pose_landmarks = None
        
    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_pose.process(frame_rgb)
        self.pose_landmarks = results.pose_landmarks
        if self.pose_landmarks:
            landmark_list  = self.pose_landmarks
            self.mp_draw.draw_landmarks(
            frame,
            landmark_list,
            landmark_drawing_spec = self.mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=3),
            connection_drawing_spec = self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2)
        )


            

            ############################red################################
        return frame


'''
puss= PoseTracking()
md = MediapipeThread(puss)
md.start()
'''