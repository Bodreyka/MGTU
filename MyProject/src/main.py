#import 
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
from tensorflow import keras
from numpy import mean
from numpy import std
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras import Sequential # Последовательная архитектура
from tensorflow.keras.layers import Dense, Dropout # Полносвязные слои
from tkinter import * # Добавим для рисования 
from tkinter import messagebox
import re
    
def calculate():
    # Проверка входных данных
    # Шаблон проверки "цЫфра?"
    fu = "^(?:\d+\.?\d+)|(?:\.\d+)|(?:\d+.)|(?:\d+)$"
    dig_l = re.fullmatch(fu, str(IW.get()))
    dig_l  = dig_l and re.fullmatch(fu, str(IF.get()))
    dig_l  = dig_l and re.fullmatch(fu, str(VW.get()))
    dig_l  = dig_l and re.fullmatch(fu, str(FP.get()))
    if not dig_l: # Если не цЫфра то считать не будем
        messagebox.showinfo('Ошибка ввода данных', 'Модель на вход принимает только цифры!')
        return()
    
   # IW	IF	VW	FP	Depth	Width
   # Загрузим датасет

    Xtest['IW'] = float(IW.get())
    Xtest['IF'] = float(IF.get())
    Xtest['VW'] = float(VW.get())
    Xtest['FP'] = float(FP.get())
    # Нормируем входные данные
    names_x =Xtest.columns # Добудем список имен колонок
    Dataset_XtestNorm = std_scaler2_x.transform(np.array(Xtest[names_x]))
    XtestNorm = pd.DataFrame(Dataset_XtestNorm, columns=names_x) 
    # Рассчитаем, используя ранрее обученную нейронную сеть
    #prediction = model.predict(XtestNorm)
    #print(prediction)
    # Конвертируем нормированный результат к физически значимым значениям
    inverse_y = std_scaler2_y.inverse_transform(model.predict(XtestNorm))
    # Выведем результат рассчета модели в окно
    calc = Label(
    frame,
    text="Ширина шва: " + str(round(inverse_y[0,0], 2)) + "мм Глубина шва: " + str(round(inverse_y[0,1], 2)) + "мм"
    )
    calc.grid(row=10, column=1)
#_________________ ну полетаем! _____________
# Все "путем"! 
filename_x = '../model/MinMaxScaler_joblib_x.pkl'
filename_y = '../model/MinMaxScaler_joblib_y.pkl'
model_path = '../model/reg_ney' 

# Загрузим сохраненный ранее объект  MinMaxScaler
std_scaler2_x =  joblib.load(filename_x) 
std_scaler2_y =  joblib.load(filename_y)

# Загрузим модель настроенной нейронной сети
model = keras.models.load_model(model_path)
# model.summary() # При отладке можно убедиться, что модель загрузилась
Ysruc = {'Depth':[], 'Width':[]}
Ytest = pd.DataFrame(Ysruc)
Xsruc = {'IW':[0.1], 'IF':[0.1], 'VW':[0.1], 'FP':[0.1]}
Xtest = pd.DataFrame(Xsruc)
# Определимся с окном ввода и вывода
window = Tk()
window.title('Образовательный центр МГТУ им.Баумана. Курс "Аналитик данных".') # Заголовок окна
window.geometry('600x600')
 

frame = Frame(
   window,
   padx=20,
   pady=120
)
frame.pack(expand=True)
# Добавим текст в окошко 
An = Label(
   frame,
   text="Курс 'Аналитик данных'. Курсовая работа Смыслова А.М"
)
An.grid(row=1, column=1)

# Добавляем описание полей ввода и сами поля ввода
IW = Label(
   frame,
   text="Величина сварочного тока (IW):"
)
 
IW.grid(row=2, column=1)
    
IF = Label(
   frame,
   text="Величина тока фокусировки электронного пучка (IF):",
)
IF.grid(row=3, column=1)

VW = Label(
   frame,
   text="Cкорость сварки (VW):",
)
VW.grid(row=4, column=1)

FP = Label(
   frame,
   text="Расстояние от ЭОП до образца(FP):",
)
FP.grid(row=5, column=1)



IW = Entry(
   frame,
)
IW.grid(row=2, column=2, pady=5)
 
IF = Entry(
   frame,
)
IF.grid(row=3, column=2, pady=5)

VW = Entry(
   frame,
)
VW.grid(row=4, column=2, pady=5)

FP = Entry(
   frame,
)
FP.grid(row=5, column=2, pady=5)



cal_btn = Button(
   frame,
   text='Рассчитать параметры сварочного шва',
   command=calculate
)
cal_btn.grid(row=6, column=1)
 
window.mainloop()