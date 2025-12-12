from McLumk_Wheel_Sports import *
import time,os,subprocess

import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# 注释掉不存在的模块导入
# from car_tts_en import Xinghou_speaktts
# from API_KEY import TTS_IAT_Tongyi

xuanxin = 0 #唤醒标志 Wake up flag
g_fail = 0 #动作执行失败标志 一般是大模型反馈的函数接口

# 设置可以预知的必定失败任务
def Set_Fail_Flag(flag):
    global g_fail
    g_fail = 2
    
def Get_Fail_Falg():
    global g_fail
    return g_fail


def is_mplayer_playing():
    try:
        result = subprocess.check_output(['pgrep', '-l', 'mplayer'])
        if not result:
            return False
        return True
    except subprocess.CalledProcessError:
        return False

#前进 forward
def Car_Forword(speed=40,mytime=1):
    move_forward(speed)
    time.sleep(mytime)
    stop_robot()
    time.sleep(0.2)

    
#后退 back
def Car_back(speed=40,mytime=1):
    move_backward(speed)
    time.sleep(mytime)
    stop_robot()
    time.sleep(0.2)
    

#原地左转 Turn left in place
def Car_left(speed=50,mytime=1):
    rotate_left(speed)
    time.sleep(mytime)
    stop_robot()
    time.sleep(0.2)


#原地右转 Turn right in place
def Car_right(speed=50,mytime=1):
    rotate_right(speed)
    time.sleep(mytime)
    stop_robot()
    time.sleep(0.2)
    
    
#左平移 Left translation
def Car_left_translation(speed=45,mytime=1):
    move_left(speed)
    time.sleep(mytime)
    stop_robot()
    time.sleep(0.2)
    
    
    
#右平移 Right translation
def Car_right_translation(speed=45,mytime=1):
    move_right(speed)
    time.sleep(mytime)
    stop_robot()
    time.sleep(0.2)
    
    
##舵机动作 Servo motor action
#点头 nod
def Car_servo_nod():
    for i in range(2):
        bot.Ctrl_Servo(2, 25)
        time.sleep(0.3)
        bot.Ctrl_Servo(2, 100)
        time.sleep(0.3)
    bot.Ctrl_Servo(2, 25) 


#摇头 sayno
def Car_servo_sayno():
    for i in range(2):
        bot.Ctrl_Servo(1, 60)
        time.sleep(0.3)
        bot.Ctrl_Servo(1, 120)
        time.sleep(0.3)
    bot.Ctrl_Servo(1, 90) 
    

#获取障碍物距离 Obtain obstacle distance
def Get_dis_obstacle():
    time.sleep(1)
    bot.Ctrl_Ulatist_Switch(1) #开启测距 Enable distance measurement
    time.sleep(0.1)
    for i in range(3):
        diss_H =bot.read_data_array(0x1b,1)[0]
        diss_L =bot.read_data_array(0x1a,1)[0]
        dis = diss_H << 8 | diss_L
        time.sleep(0.1)
    bot.Ctrl_Ulatist_Switch(0) #关闭测距 Turn off distance measurement
    
    if dis<250:
        #播报障碍物的距离 Report the distance of obstacles
        tts_text="The distance of the obstacle is:"+str(dis)+"mm"
        print("A:"+tts_text)
        while is_mplayer_playing():  #等待音频播放完成再播放 Wait for the audio playback to complete before playing again
            pass
        Xinghou_speaktts(tts_text)
            
    else:
        while is_mplayer_playing():  
            pass
        os.system("mplayer ./AI_CarAgent_en/noobstacle_en.mp3 < /dev/null > /dev/null 2>1 &")
        print("A:No obstacles detected")
        time.sleep(0.5)
        


#控制RGB灯颜色 Control RGB light color
def Car_RGB_Control(R,G,B):
    bot.Ctrl_WQ2812_brightness_ALL(R,G,B)

#关闭RGB灯 Turn off RGB lights
def Close_RGB():
    bot.Ctrl_WQ2812_ALL(0,7)
    
    
#小车复位操作 Car reset operation
def Car_Reset():
    Close_RGB()
    bot.Ctrl_Ulatist_Switch(0) #关闭测距 #Turn off distance measurement
    bot.Ctrl_Servo(1, 90) 
    bot.Ctrl_Servo(2, 25) 
    stop_robot()
    


import cv2
#打开摄像头，记录图片 Open the camera and record the image
def take_photo_agent():
    time.sleep(1) #1s
    cap=cv2.VideoCapture(0)
    cap.set(3,320*2)
    cap.set(4,240*2)

    path = "./AI_CarAgent_en/"  
    ret, image = cap.read()
    filename = "rec"
    cv2.imwrite(path + filename + ".jpg", image)
    time.sleep(1)
    cap.release()
    print("Photos to record")
    print("camera close")
    

# 跳舞方法 Dance method
# 组合小车的各种动作和RGB灯效果，形成一个跳舞序列
# Combine various actions of the car and RGB light effects to form a dance sequence
# 持续时间至少20秒，包含灯光和摇头效果
# Duration: at least 20 seconds, including lighting and head-shaking effects

def Car_dance():
    try:
        start_time = time.time()
        
        # 初始化：RGB灯闪烁三次表示开始跳舞
        # Initialization: RGB light blinks three times to indicate dance start
        for _ in range(3):
            Car_RGB_Control(255, 255, 255)  # 白色
            time.sleep(0.2)
            Close_RGB()
            time.sleep(0.2)
        
        # 第一阶段：基础移动组合 + 彩色灯光变化（4秒）
        # Stage 1: Basic movement combination + color light changes (4 seconds)
        colors = [
            (255, 0, 0),    # 红色
            (0, 255, 0),    # 绿色
            (0, 0, 255),    # 蓝色
            (255, 255, 0),  # 黄色
        ]
        
        for i, color in enumerate(colors):
            Car_RGB_Control(*color)
            if i % 2 == 0:
                Car_Forword(speed=35, mytime=0.5)
                Car_servo_nod()
            else:
                Car_back(speed=35, mytime=0.5)
                Car_servo_sayno()
        
        # 第二阶段：平移与旋转组合 + 彩虹灯光（5秒）
        # Stage 2: Translation and rotation combination + rainbow lights (5 seconds)
        rainbow_colors = [
            (255, 0, 0),    # 红
            (255, 127, 0),  # 橙
            (255, 255, 0),  # 黄
            (0, 255, 0),    # 绿
            (0, 0, 255),    # 蓝
            (75, 0, 130),   # 靛
            (148, 0, 211),  # 紫
        ]
        
        for color in rainbow_colors[:5]:  # 使用前5种颜色
            Car_RGB_Control(*color)
            Car_left_translation(speed=40, mytime=0.4)
            Car_servo_sayno()
            
            Car_RGB_Control(*rainbow_colors[rainbow_colors.index(color) + 1 if color != rainbow_colors[-2] else 0])
            Car_right_translation(speed=40, mytime=0.4)
            Car_servo_nod()
        
        # 第三阶段：快速旋转与点头摇头组合 + 闪烁灯光（3秒）
        # Stage 3: Fast rotation with nodding and head-shaking + flashing lights (3 seconds)
        for _ in range(3):
            Car_RGB_Control(255, 255, 255)  # 白色闪烁
            Car_left(speed=60, mytime=0.3)
            Close_RGB()
            Car_right(speed=60, mytime=0.3)
            
            Car_servo_nod()  # 点头
            time.sleep(0.1)
            Car_servo_sayno()  # 摇头
        
        # 第四阶段：连续前进后退+颜色渐变（4秒）
        # Stage 4: Continuous forward and backward + color gradient (4 seconds)
        for r in range(0, 256, 30):
            Car_RGB_Control(r, 255 - r, 128)
            Car_Forword(speed=30, mytime=0.2)
            Car_back(speed=30, mytime=0.2)
            Car_servo_sayno()  # 持续摇头
        
        # 第五阶段：全方位移动组合 + 随机灯光（4秒）
        # Stage 5: Omnidirectional movement combination + random lights (4 seconds)
        movements = [
            Car_Forword, 
            Car_back, 
            Car_left, 
            Car_right, 
            Car_left_translation, 
            Car_right_translation
        ]
        
        for _ in range(8):
            # 随机颜色
            import random
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            Car_RGB_Control(r, g, b)
            
            # 随机选择移动方式
            movement = random.choice(movements)
            if movement in [Car_left, Car_right]:
                movement(speed=45, mytime=0.3)
            else:
                movement(speed=35, mytime=0.3)
            
            # 交替点头摇头
            if _ % 2 == 0:
                Car_servo_nod()
            else:
                Car_servo_sayno()
        
        # 第六阶段：结束动作 + 渐变灯光（4秒）
        # Stage 6: Ending action + gradient lights (4 seconds)
        Car_RGB_Control(255, 255, 255)  # 白色
        
        # 画圈结束动作
        for _ in range(2):
            Car_Forword(speed=30, mytime=0.5)
            Car_left(speed=30, mytime=0.5)
            Car_servo_nod()
        
        # 灯光逐渐变暗
        for brightness in range(255, -1, -25):
            Car_RGB_Control(brightness, brightness, brightness)
            time.sleep(0.2)
        
        # 跳舞结束，关闭RGB灯，恢复初始状态
        # Dance ends, turn off RGB lights, restore initial state
        Close_RGB()
        
        total_duration = time.time() - start_time
        return f"跳舞完成！Dance completed! 持续时间: {total_duration:.1f}秒"
        
    except Exception as e:
        # 发生错误时，关闭RGB灯，恢复初始状态
        # In case of error, turn off RGB lights, restore initial state
        Close_RGB()
        return f"跳舞时发生错误：{str(e)} Error occurred during dance: {str(e)}"

# def Image_Describe():
#     img = cv2.imread("./AI_CarAgent/rec.jpg")
#     cv2.imshow('image',img)
#     cv2.waitKey(1)
#     time.sleep(3)
#     cv2.destroyAllWindows()
