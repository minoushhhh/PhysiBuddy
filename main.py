'''
Ignition Hacks 2022
Idea: An exercise counter that based on body jints determines 
whether or not a repition was performed or not
August 27, 2022
'''
# importing libraries
import cv2
import mediapipe as md

# drawing the lines on the body
md_drawing = md.solutions.drawing_utils
md_drawing_styles = md.solutions.drawing_styles
md_pose = md.solutions.pose

# initializing the exercise counter
push_up_count = 0
squat_count = 0

# initializing the current position of the user
position = None
squat_position = None

# video input from the web camera (0 refers to the web cam)
cap = cv2.VideoCapture(0)

# parameters refers to the accuracy of detection and tracking
with md_pose.Pose(
    min_detection_confidence = 0.7, 
    min_tracking_confidence = 0.7) as pose:

    # while the video cam is opened
    while cap.isOpened():
        sucess, image = cap.read()
        # if the web cam is not returning a video
        if not sucess:
            print("Empty Camera")
            break
        
        # convert to RGB
        image = cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB)
        result = pose.process(image)

        # list contains all the coordinates of the pose model
        imlist = []

        # if a body is present in the video
        if result.pose_landmarks:
            # draws all the lines and dots
            # image where we want to draw, all the points of the pose model, all the lines that connects the dots
            md_drawing.draw_landmarks(
                image, result.pose_landmarks, md_pose.POSE_CONNECTIONS)
            for id, im in enumerate(result.pose_landmarks.landmark):
                h,w,_=image.shape
                X,Y,=int(im.x*w),int(im.y*h)
                imlist.append([id,X,Y])
        if len(imlist) != 0:
                if ((imlist[12][2] - imlist[14][2])>=15 and (imlist[11][2] - imlist[13][2])>=15):
                    position = "down"
                if ((imlist[12][2] - imlist[14][2])<=5 and (imlist[11][2] - imlist[13][2])<=5) and position == "down":
                    position = "up"
                    push_up_count +=1 
                    print("Push-ups performed: ", push_up_count)
                if(imlist[26][2] and imlist[25][2] <= imlist[24][2] and imlist[23][2]):
                    squat_position = "down"
                if(imlist[26][2] and imlist[25][2] >= imlist[24][2] and imlist[23][2]) and squat_position == "down":
                    squat_position = "up"
                    squat_count += 1
                    print("Squats performed: ", squat_count)
                
        cv2.imshow("Exercise Counter", cv2.flip(image,1))
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

cap.release()