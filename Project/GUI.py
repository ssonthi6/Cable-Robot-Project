import easygui
import os.path
import kinematics as k
import centering as c
import cPickle as pickle

msg = "Enter Change in X and Y"
title = "Test"
field_names = ["Change in X","Change in Y",]
input_values = []  # blank values
input_values = easygui.multenterbox(msg,title, field_names)

msg_center = "Center?"
choices = ["Yes", "No"]
default_choice = choices[0]
cancel_choice = choices[1]
center_box = easygui.ynbox(msg_center, title, choices)

if center_box:
    c.write_origin()

else:
    sys.exit(0)

# make sure that none of the fields was left blank
while 1:
    if input_values == None: break
    errmsg = ""
    for i in range(len(field_names)):
      if input_values[i].strip() == "":
        errmsg = errmsg + ('"%s" is a required field.\n\n' % field_names[i])
    if errmsg == "": break # no problems found
    input_values = easygui.multenterbox(errmsg, title, field_names, input_values)


origin = [21.5, 52.0]

#data_file = Path("/home/pi/Documents/RoboClaw/Project/data_pickle.pickle")

try:
    pos = pickle.load(open('data_pickle.pickle', 'rd'))
except (OSError, IOError) as e:
    pos = origin
    pickle.dump(pos, open('data_pickle.pickle', 'wb'))

print pos

k.dist_2D(float(input_values[0]), float(input_values[1]))


x1 = float(pos[0]) + float(input_values[0])
y1 = float(pos[1]) - float(input_values[1])
updated_data = [x1, y1]
pickle.dump(updated_data, open('data_pickle.pickle', 'wb'))

print updated_data
