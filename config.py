# used pins

configuration = {
    'DEVEL_LOG' : False,
    'CLEAN_ACTION_TIME_SPAN' : 2
}

motor_conf = {
    'DEVEL_LOG' : False,
    'AUTO_TIME' : .05,
    'ACCELERATION_TIME' : .02,
    'motor_back_left_pin' : 7,
    'motor_back_right_pin' : 13,
    'motor_front_left_pin' : 11,
    'motor_front_right_pin' : 15
}

servo_conf = {
    'DEVEL_LOG' : False,
    'angle1' : 90,
    'angle2' : 90,
    'angle_forward' : 5,
    'angle_backward' : -5,
    'frequency' : 50,
    'servo_1_pin' : 12, 
    'servo_2_pin' : 32
}

distance_conf = {
    'DEVEL_LOG' : False,
    'SAFETY_DISTANCE' : 10, # cm
    'SPEED_OF_SOUND' : 17150, # 34300/2
    'TRIG_SPAN' : .00001, # sec
    'SENSORS_OFF_SPAN' : .5, # sec
    'trig_1_pin' : 16,
    'echo_1_pin' : 18,
    'trig_2_pin' : 37,
    'echo_2_pin' : 22
}

track_conf = {
    'DEVEL_LOG' : False,
    'color' : 0,
    'track_1_pin' : 38,
    'track_2_pin' : 40
}

led_conf = {
    'DEVEL_LOG' : False,
    'red_pin' : 36,
    'green_pin' :  29,
    'blue_pin' :  31
}

# BCM standard
screen_conf = {
    'DEVEL_LOG' : False,
    'lcd_columns' : 16,
    'lcd_rows' : 2,
    'lcd_backlight' : 4,
    'lcd_rs' : 10,  # board: 19
    'lcd_en' : 9,   # board: 21
    'lcd_d4' : 19,  # board: 35
    'lcd_d5' : 8,   # board: 24
    'lcd_d6' : 7,   # board: 26
    'lcd_d7' : 11   # board: 23
}
