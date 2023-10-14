#coding=utf-8
import numpy as np
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


#定義活化函數sqn
def sqn(number):
    if number>=0:
        return 1
    else:
        return -1
        
#定義準確率演算法
def acu(data,target,weight):
    correct_number=0
    for i,row in enumerate(data):
        y=sqn(np.dot(row,weight.T))
        if(y==1 and target[i]==max_value):
            correct_number+=1
        elif(y==-1 and target[i]==min_value):
            correct_number+=1
    percent=correct_number/len(data)*100
    return percent

#處理資料
def data_process(data_all):
    
    #資料排序
    data_number=len(data_all)#資料數量
    
    train_number=int(data_number*2/3) #訓練資料數量
    
    global max_value,min_value
    target=data_all[:,-1:].reshape(data_number) #目標張量
    
    max_value=np.max(target)
    min_value=np.min(target)

    w_0=np.full((data_number,1),-1)#減去神經閥值
    
    data_all=np.hstack((w_0,data_all[:,:2]))
    #隨機選取訓練資料和測試資料
    random=np.random.choice(data_number, size=train_number, replace=False)
    data_train=data_all[random,:]
    target_train=target[random]
    data_test=np.delete(data_all,random,axis=0)
    target_test=np.delete(target,random)
    
    return data_train,target_train,data_test,target_test
        

#跑epoch
def run_epoch(train_data, target):
    # 隨機初始化鍵結值
    weight_key = np.random.uniform(-1, 1, size=3)
    
    for i in range(epoch):
        
        for number in range(len(train_data)):
            y = sqn(np.dot(train_data[number], weight_key.T))  # 做內積
            
            if y == 1 and target[number] == min_value:
                weight_key -= learing_rate * train_data[number]
            elif y == -1 and target[number] == max_value:
                weight_key += learing_rate * train_data[number]

    percent = acu(train_data, target, weight_key)
    return weight_key, percent




def draw_plot(data):#畫左邊圖
    target=data[0][2]
    one_kind_condition=data[:,2]==target
    one_kind_x=data[one_kind_condition,0]
    one_kind_y=data[one_kind_condition,1]

    two_kind_x=data[~one_kind_condition,0]
    two_kind_y=data[~one_kind_condition,1]
    a1.clear()
    a1.plot(two_kind_x,two_kind_y,'bo')
    a1.plot(one_kind_x,one_kind_y,'go')
    canvas1.draw()

def draw_plot2(data,weight):#畫右邊圖
    target=data[0][2]
    one_kind_condition=data[:,2]==target
    one_kind_x=data[one_kind_condition,0]
    one_kind_y=data[one_kind_condition,1]

    two_kind_x=data[~one_kind_condition,0]
    two_kind_y=data[~one_kind_condition,1]

    x = np.linspace(-10, 10, 100)
    y=weight[0]/weight[2]-weight[1]/weight[2]*x

    a2.clear()
    a2.plot(two_kind_x,two_kind_y,'bo')
    a2.plot(one_kind_x,one_kind_y,'go')
    a2.plot(x,y,'r')

    canvas2.draw()


#定義按鈕啟動
def start(): #開始
    global epoch,learing_rate,accuracy
    np.random.seed(1234) #設定種子
    epoch=int(sp_epo.get())
    accuracy=float(sp_acu.get())
    learing_rate=float(sp_rate.get())

    data_train,target_train,data_test,target_test=data_process(data)
    weight_key,train_percent=run_epoch(data_train,target_train)
    test_percent=acu(data_test,target_test,weight_key)

    draw_plot2(data,weight_key)

    lb_train.config(text=f"Train accuracy : {train_percent}")
    lb_test.config(text=f"Test accuracy : {test_percent}")
    lb_weight.config(text=f"Weight : {weight_key}")


def file(): #打開資料
    global file_path,data
    file_path = filedialog.askopenfilename()
    file_path=file_path.replace("\\","/")
    lb_file.config(text=file_path)
    lb_file.place(x=10,y=335)
    data=np.loadtxt(file_path,dtype=float, encoding="utf-8")
    draw_plot(data)


#輸入介面
win=tk.Tk()
win.config(bg="gainsboro")
win.title("Perceptron")
win.geometry("900x600")
f1 = Figure(figsize=(3.7, 2.9), dpi=100)
a1 = f1.add_subplot(111)
f2 = Figure(figsize=(3.7, 2.9), dpi=100)
a2 = f2.add_subplot(111)
canvas1 = FigureCanvasTkAgg(f1, master=win)
canvas1.draw()
canvas1.get_tk_widget().place(x=50,y=10)
canvas2 = FigureCanvasTkAgg(f2, master=win)
canvas2.draw()
canvas2.get_tk_widget().place(x=450,y=10)

toolbar = NavigationToolbar2Tk(canvas2, win)
toolbar.update()

#定義widget
lb_rate=tk.Label(text="learing rate")
lb_file=tk.Label(text="")
lb_method=tk.Label(text="Method",font=15)
lb_percent=tk.Label(text="%",bg="gainsboro")
lb_train=tk.Label(text="Train accuracy : ")
lb_test=tk.Label(text="Test accuracy : ")
lb_weight=tk.Label(text="Weight : ")
sp_epo=tk.Spinbox(from_=10, to=1000,increment=20,width=5)
sp_acu=tk.Spinbox(from_=0, to=100,increment=10,width=5)
sp_rate=tk.Spinbox(from_=0.05, to=1.0,increment=0.05)
btn_start=tk.Button(text="start",command=start,font=10,width=5)
data_btn=tk.Button(text="Data",command=file)
var = tk.StringVar()
radio_epo=tk.Radiobutton(text="Epoch",variable=var,value="A",bg="gainsboro")
radio_epo.invoke()

#排版
data_btn.place(x=10,y=300)
radio_epo.place(x=10,y=400)
lb_method.place(x=10,y=370)
lb_rate.place(x=10,y=470)
sp_rate.place(x=10,y=495)
btn_start.place(x=360,y=550)
lb_train.place(x=400,y=400)
lb_test.place(x=400,y=440)
lb_weight.place(x=400,y=480)
sp_epo.place(x=120,y=405)


win.mainloop()
