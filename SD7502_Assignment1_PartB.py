# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 20:30:23 2020

This script opens a webcam and allows the user to manipulate the output using 
the following keys:
    
    p = pause               b = blue channel  
    s = record video        g = green channel   
    c = canny edges         r = red channel
    d = default BGR
        
@author: Jake Hann, ID: 2173961 & Tasha Vollmer-Selby, ID: 211111
"""

# Import the required packages
import cv2 as cv


mode_to_show = 0        # 0 = Default, 1 = Canny, 2 = blue, 3 = green, 4 = red
video_index = 0         # File name for video recording
saving_video = False    # Triggers recording on/off   
paused = False          # Used to determine if the output is currently paused
out = cv.VideoWriter()  # Used to save video
fourcc = cv.VideoWriter_fourcc('X','V','I','D') # Set codec for video recording

# Open webcam
capture = cv.VideoCapture(0)

# Check camera has opened sucessfully
if capture.isOpened() is False:
    print("Error opening the camera...")
else:
    print("Camera opened sucessfully!")

# Get window dimensions and frame rate
frame_width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
frame_height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
fps = capture.get(cv.CAP_PROP_FPS)

print('Window size: ' + str(frame_width) + " x " + str(frame_height))
print('FPS: ' + str(fps))
            
while capture.isOpened():
    
    # Capture frame-by-frame from the webcam
    ret, frame = capture.read()
    
    if ret is True:
        
        # Display default BGR
        if mode_to_show == 0:
        
            output_frame = frame.copy()
            
        #Display canny edges
        elif mode_to_show == 1:
    
            # Convert frames to grayscale, then to canny edge and back to BGR
            gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            canny_frame = cv.Canny(gray_frame, 100, 100)
            output_frame = cv.cvtColor(canny_frame, cv.COLOR_GRAY2BGR)
           
        # Display blue channel only
        elif mode_to_show == 2:
            
            # Set red and green channels to 0 
            output_frame = frame.copy()
            output_frame[:, :, 1] = 0
            output_frame[:, :, 2] = 0
                      
        # Display green channel only
        elif mode_to_show == 3:
            
            # Set blue and red channels to 0 
            output_frame = frame.copy()
            output_frame[:, :, 0] = 0
            output_frame[:, :, 2] = 0
            
        # Display red channel only
        elif mode_to_show == 4:
            
            # Set blue and green channels to 0 
            output_frame = frame.copy()
            output_frame[:, :, 0] = 0
            output_frame[:, :, 1] = 0
            
        # Show output
        cv.imshow('Assignment 1 Part B', output_frame)
        
        # Save video is triggered by 's' key press
        if saving_video == True:
            out.write(output_frame)
            
        key_pressed = cv.waitKey(20)
        
        # Exit while loop/Close camera
        if key_pressed & 0xFF == ord('q'):
            break
        
        # Pause
        elif key_pressed & 0xFF == ord('p'):
            paused = True
            while paused:
                p_key = cv.waitKey(0)
                if p_key & 0xFF == ord('p'):
                    pause = False
                    break
                
        # Default view
        elif key_pressed & 0xFF == ord('d'):
            mode_to_show = 0
            
        # Canny edges
        elif key_pressed & 0xFF == ord('c'):
            mode_to_show = 1
            
        # Blue channel
        elif key_pressed & 0xFF == ord('b'):
            mode_to_show = 2
            
        # Green channel   
        elif key_pressed & 0xFF == ord('g'):
            mode_to_show = 3
            
        # Red channel
        elif key_pressed & 0xFF == ord('r'):
           mode_to_show = 4
           
        # Save video
        elif key_pressed & 0xFF == ord('s'):
            
            if saving_video == False:
                saving_video = True
                # Parameters: filename, codec, fps, window size (wont work unless hardcoded?)
                out = cv.VideoWriter(str(video_index) + '.avi', fourcc, fps, (640,480))
                
            elif saving_video == True:
                saving_video = False
                video_index += 1
                out.release()    
                
   # Exit the while Loop
    else:
        break

# Release everything
out.release() 
capture.release()
cv.destroyAllWindows()