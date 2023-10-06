#coding=utf-8
import numpy as np
import tkinter as tk
from tkinter import filedialog


#定義活化函數sqn
def sqn(number):
    mean=(max_value-min_value)/2
    if number>=mean:
        return max_value
    else:
        return min_value
    
#定義準確率演算法
def acu(data,target,weight):
    correct_number=0
    for i,row in enumerate(data):
        y=sqn(np.dot(row,weight))
        if(target[i]==y):
            correct_number+=1
    percent=correct_number/len(data)*100
    return percent

#處理資料
def data_process(data_all):
    print(data_all)
    #資料排序
    data_number=len(data_all)#資料數量
    train_number=int(data_number*2/3) #訓練資料數量
    
    global max_value,min_value
    target=data_all[:,-1:].reshape(data_number) #目標張量
    max_value=np.max(target)
    min_value=np.min(target)

    w_0=np.full((data_number,1),-1)#減去神經閥值
    data_all=np.empty((data_number,3),dtype=float) #訓練資料
    data_all=np.hstack((w_0,data_all[:,:2]))
    #隨機選取訓練資料和測試資料
    random_train=np.random.choice(data_number, size=train_number, replace=False)
    data_train=data_all[random_train,:]
    data_test=np.delete(data_all,random_train,axis=0)
    return data_train,data_test,target
        

#跑epoch
def run_epoch(data,target):
    #隨機初始化鍵結值
    weight_key=np.random.uniform(-1,1,size=3)
    for i in range(epoch):
        count=i% len(data)  #正在處理第幾項資料
        y=sqn(np.dot(data[count],weight_key)) #做內積
        if y==target[count]:
            weight_key= weight_key #不做改變
        elif y==max_value and target[count]== min_value:
            weight_key-=learing_rate*data[count] #往負方向校正方向
        elif y==min_value and target[count]== max_value:
            weight_key+=learing_rate*data[count] #往正方向校正方向
        else:
            print("wrong")  #報錯
    
    percent=acu(data,target,weight_key)
    return weight_key,percent


#跑accuracy
def run_accuracy(data,target):
    i=0
    percent=0
    while(percent<accuracy): #大於準確率就跳出函式
        count=i%len(data)  #正在處理第幾項資料
        y=sqn(np.dot(data[count],weight_key)) #做內積
        if y==target[count]:
            weight_key= weight_key #不做改變
        elif y==max_value and target[count]==min_value:
            weight_key-=learing_rate*data[count] #往負方向校正方向
        elif y==min_value and target[count]==max_value:
            weight_key+=learing_rate*data[count] #往正方向校正方向
        else:
            print("wrong")  #報錯
        i+=1
        percent=acu(data,target,weight_key)
    return weight_key,percent

#定義按鈕啟動
def start(): #開始
    global epoch,learing_rate,accuracy
    np.random.seed(1234) #設定種子
    epoch=int(sp_epo.get())
    accuracy=float(sp_acu.get())/100
    learing_rate=float(sp_rate.get())
    data=np.loadtxt(file_path,dtype=float, encoding="utf-8")
    data_train,data_test,target=data_process(data)
    option=var.get()
    if option=="A":
        weight_key,train_percent=run_epoch(data_train,target)
        weight_key,test_percent=run_epoch(data_test,target)
        lb_train.config(text=f"Train accuracy : {train_percent}")
        lb_test.config(text=f"Test accuracy : {test_percent}")
        lb_weight.config(text=f"Weight : {weight_key}")
    else:
        weight_key,train_percent=run_accuracy(data_train,target)
        weight_key,test_percent=run_accuracy(data_test,target)
        lb_train.config(text=f"Train accuracy : {train_percent}")
        lb_test.config(text=f"Test accuracy : {test_percent}")
        lb_weight.config(text=f"Weight : {weight_key}")

def file(): #打開資料
    global file_path
    file_path = filedialog.askopenfilename()
    file_path=file_path.replace("\\","/")
    lb_file.config(text=file_path)
    lb_file.place(x=10,y=335)

def epo_or_acu(): #選擇要用epoch還是acu
    option=var.get()
    if option=="A":
        lb_percent.place_forget()
        sp_epo.place(x=120,y=405)
        sp_acu.place_forget()
        
    else:
        lb_percent.place(x=170,y=428)
        sp_acu.place(x=120,y=428)
        sp_epo.place_forget()

#輸入介面
win=tk.Tk()
win.config(bg="gainsboro")
win.title("Perceptron")
win.geometry("800x600")

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
radio_epo=tk.Radiobutton(text="Epoch",variable=var,value="A",bg="gainsboro",command=epo_or_acu)
radio_acu=tk.Radiobutton(text="Accuracy",variable=var,value="B",bg="gainsboro",command=epo_or_acu)
radio_epo.invoke()

#排版
data_btn.place(x=10,y=300)
radio_epo.place(x=10,y=400)
radio_acu.place(x=10,y=425)
lb_method.place(x=10,y=370)
lb_rate.place(x=10,y=470)
sp_rate.place(x=10,y=495)
btn_start.place(x=360,y=550)
lb_train.place(x=400,y=400)
lb_test.place(x=400,y=440)
lb_weight.place(x=400,y=480)


win.mainloop()



