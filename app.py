#------------------------------------------------------------------Herramientas------------------------------------------------------------------------
from tkinter import *
from animacion import *
from PIL import Image, ImageTk
from conexion_ollama import *
from sol import *
import threading

#-----------------------------------------------------------------------funciones---------------------------------------------------------------------------
def intro():#boton empezar
    boton_init.destroy()
    frame1.grid(row=0,column=0)
    text_input.grid(row=0,column=1)
    boton_buscar.grid(row=0,column=0)
    frame3.grid(row=0,column=2)
    lista_tk = Olaf.imagen_sec(Animacion.saludo)
    Olaf.sec_for(pinguino,lista_tk)

def hablar():
    texto_guardado = StringVar()
    texto_guardado.set(text_input.get("1.0", END).strip())
    t = texto_guardado.get()
    request = conect(texto_guardado.get())

    lista_tk = Olaf.imagen_sec(Animacion.hablar_in)
    Olaf.sec_for(pinguino,lista_tk)

    texto_retorno.config(state="normal")
    texto_retorno.delete("1.0", "end")
    for i in range(len(request)):
        texto_retorno.insert('end',request[i])
        texto_retorno.update()
        texto_retorno.see("end")
        texto_retorno.after(30)
    texto_retorno.config(state="disabled")
    lista_tk = Olaf.imagen_sec(Animacion.hablar_out)
    Olaf.sec_for(pinguino,lista_tk)

def prueba():#testeador de botones
    print('funciona')

#------------------------------------------------------------------------libreria OLAF------------------------------------------------------------------
class Olaf:# Libreria para correr animaciones en Tkinter

    # -------------------------------convertir imagen------------------------------------
    def imagen(ruta, ancho, alto):
        imagen = Image.open(ruta)
        imagen = imagen.resize((ancho,alto))
        imagen_tk = ImageTk.PhotoImage(imagen)
        return imagen_tk
# -------------------------------convertir lista de imagenes--------------------------
    def imagen_sec(lista_img):
        lista_tk = []
        for i in lista_img:
            imagen_tk = Olaf.imagen(i,250,250)
            lista_tk.append(imagen_tk)
        return lista_tk
# -------------------------------animacion for-------------------------------------
    def sec_for(canvas,lista_tk):
        global g_lista
        g_lista = lista_tk
        lbl= canvas
        for i in g_lista:
            lbl.delete("all")
            lbl.create_image(128, 128, image=i) #coordenadas de la imagen
            lbl.update_idletasks()  # Actualizar la interfaz de usuario
            lbl.after(50)  # Pausa


#-------------------------------------------------------------------estructura de interfaz visual--------------------------------------------------------
root = Tk()
root.title('Flipper.ai')
root.attributes('-alpha', .9)
root.config(bg='blue')

frame1 = Frame(root,width=250,height=204)
frame1.grid(row=0,column=0)
frame1.grid_forget()

frame2 = Frame(root)
frame2.grid(row=0,column=1)

frame3 = Frame(root)
frame3.grid(row=0,column=2)
frame3.grid_forget()


# -------------------------------frame1 texto_retorno------------------------------
img_nube = Olaf.imagen('templates/nube_texto.png',350,277)
img_fondo = Label(frame1,image=img_nube,width=350,height=277)
img_fondo.grid(row=0,column=0)
texto_retorno = Text(frame1,width=40,height=15,borderwidth=0,font=("arial", 11))
texto_retorno.grid(row=0,column=0)



#---------------------------------frame2 pinguino-----------------------------------
boton_buscar = Button(frame2,text='buscar',command=lambda:threading.Thread(target=hablar()))
boton_buscar.grid(row=0,column=0)
boton_buscar.grid_forget()

text_input = Text(frame2,width=21,height=1,borderwidth=0,font=("arial", 13))
text_input.grid(row=0,column=1)
text_input.grid_forget()

pinguino = Canvas(frame2,bg='white',width=251,height=251)
pinguino.grid(row=1,column=0,columnspan=2)

img_boton = Olaf.imagen('templates/boton.png',150,150)
boton_init = Button(frame2,borderwidth=0,bg='white',activebackground="white",image=img_boton,command=lambda:intro())
boton_init.grid(row=1,column=0,columnspan=2)



# --------------------------------frame3 botones--------------------------------------
pomodoro = PomodoroApp(frame3)


#----------------------------------------------------------------mainloop para inicializar la app------------------------------------------------------------
root = root
root.mainloop()

