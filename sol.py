import tkinter as tk
import threading
import time
import winsound


def formatear_tiempo(segundos):
    minutos = segundos // 60
    segundos = segundos % 60
    return f"{minutos:02d}:{segundos:02d}"

class Pomodoro:

    # def __init_subclass__(self,frame3,label):
    #     self.frame3 = frame3
    #     self.text = label 
        
    def __init__(self, actualizar_label, mostrar_mensaje):
        self.tiempo_trabajo = 20  # 3 minutos para pruebas
        self.tiempo_descanso = 10  # 2 minutos para pruebas
        self.en_ejecucion = False
        self.en_pausa = False
        self.segundos_restantes = self.tiempo_trabajo
        self.hilo_temporizador = None
        self.actualizar_label = actualizar_label
        self.mostrar_mensaje = mostrar_mensaje

    def iniciar(self):
        if not self.en_ejecucion and not self.en_pausa:
            self.en_ejecucion = True
            self.segundos_restantes = self.tiempo_trabajo
            self.ejecutar_temporizador(self.segundos_restantes, self.callback_trabajo)

    def callback_trabajo(self):
        if self.en_ejecucion:
            self.mostrar_mensaje("¡Hora de \ndescansar!")
            winsound.PlaySound("templates/alarma.wav", winsound.SND_FILENAME)
            self.segundos_restantes = self.tiempo_descanso
            self.ejecutar_temporizador(self.segundos_restantes, self.callback_descanso)

    def callback_descanso(self):
        if self.en_ejecucion:
            self.mostrar_mensaje("Vuelta al trabajo")
            self.segundos_restantes = self.tiempo_trabajo
            self.ejecutar_temporizador(self.segundos_restantes, self.callback_trabajo)

    def ejecutar_temporizador(self, segundos, callback):
        def temporizador():
            nonlocal segundos
            while segundos > 0 and self.en_ejecucion and not self.en_pausa:
                self.actualizar_label(formatear_tiempo(segundos))
                time.sleep(1)
                segundos -= 1
                self.segundos_restantes = segundos
            if self.en_ejecucion and not self.en_pausa:
                callback()

        if self.hilo_temporizador is None or not self.hilo_temporizador.is_alive():
            self.hilo_temporizador = threading.Thread(target=temporizador)
            self.hilo_temporizador.start()

    def pausar(self):
        if self.en_ejecucion:
            self.en_pausa = True
            self.en_ejecucion = False

    def reanudar(self):
        if self.en_pausa:
            self.en_pausa = False
            self.en_ejecucion = True
            self.ejecutar_temporizador(self.segundos_restantes, self.callback_trabajo if self.segundos_restantes > self.tiempo_descanso else self.callback_descanso)

    def reiniciar(self):
        self.detener()
        self.actualizar_label(formatear_tiempo(self.tiempo_trabajo))
        self.actualizar_label(formatear_tiempo(self.segundos_restantes))

    def detener(self):
        self.en_ejecucion = False
        self.en_pausa = False
        if self.hilo_temporizador is not None:
            self.hilo_temporizador.join()

class PomodoroApp:
    def __init__(self, frame3):
        
        
        #Edicion de Botones
        # self.root = root
        # self.root.title("Temporizador Pomodoro")

        self.label = tk.Label(frame3, font=("Helvetica", 15), fg='black',height=3)
        self.label.grid(row=0,column=0)

        self.boton_iniciar = tk.Button(frame3, text="Pomodoro", fg="white", bg='#1f0441',  font=('Arial', 16, 'bold'), width=13, height=1,pady=5, command=self.iniciar_pomodoro)
        self.boton_iniciar.grid(row=1,column=0)

        self.boton_detener = tk.Button(frame3, text="Detener", fg="white", bg='#1f0441', command=self.detener_pomodoro,  font=('Arial', 16, 'bold'), width=13, height=1,pady=6, state=tk.DISABLED)
        self.boton_detener.grid(row=2,column=0)

        self.boton_reanudar = tk.Button(frame3, text="Reanudar", fg="white", bg='#1f0441', command=self.reanudar_pomodoro,  font=('Arial', 16, 'bold'), width=13, height=1,pady=6, state=tk.DISABLED)
        self.boton_reanudar.grid(row=3,column=0)

        self.boton_reiniciar = tk.Button(frame3, text="Reiniciar", fg="white", bg='#1f0441', command=self.reiniciar_pomodoro,  font=('Arial', 16, 'bold'), width=13, height=1,pady=6, state=tk.DISABLED)
        self.boton_reiniciar.grid(row=4,column=0)

        self.pomodoro = Pomodoro(self.actualizar_label, self.mostrar_mensaje)
        
        self.actualizar_label(formatear_tiempo(self.pomodoro.tiempo_trabajo)) 


    def actualizar_label(self, tiempo):
            self.label.config(text=tiempo)
    
    
    
    def mostrar_mensaje(self, mensaje):
        self.label.config(text=mensaje)

    
    def iniciar_pomodoro(self):
        self.pomodoro.iniciar()
        self.boton_iniciar.config(state=tk.DISABLED)
        self.boton_detener.config(state=tk.NORMAL)
        self.boton_reanudar.config(state=tk.DISABLED)
        self.boton_reiniciar.config(state=tk.DISABLED)

    def detener_pomodoro(self):
        self.pomodoro.pausar()
        self.boton_iniciar.config(state=tk.DISABLED)
        self.boton_detener.config(state=tk.DISABLED)
        self.boton_reanudar.config(state=tk.NORMAL)
        self.boton_reiniciar.config(state=tk.NORMAL)

    def reanudar_pomodoro(self):
        self.pomodoro.reanudar()
        self.boton_iniciar.config(state=tk.DISABLED)
        self.boton_detener.config(state=tk.NORMAL)
        self.boton_reanudar.config(state=tk.DISABLED)
        self.boton_reiniciar.config(state=tk.DISABLED)

    def reiniciar_pomodoro(self):
        self.pomodoro.reiniciar()
        self.boton_iniciar.config(state=tk.NORMAL)
        self.boton_detener.config(state=tk.DISABLED)
        self.boton_reanudar.config(state=tk.DISABLED)
        self.boton_reiniciar.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()