
"""
Created by Tobs80.
"""

import random
import numpy as np
import math
import prettytable as prettytable
from prettytable import DEFAULT


#Listas que contienen las materias de cada semestre
materias_5to = ["Simulacion","Fisica IV","Fisica V","Informatica","Redaccion","Electronica IV","Vacio"]
materias_6to =["Proyectos VI","Electronica V","Mecanica VI","Mecanica VII","Sistemas","Instrumentacion","Vacio"]
materias_7mo =["E. Renovables","Informatica IV","Mecatronica II","Proyectos II","Electronica II","Microeconomia","Vacio"]
##diccionarios para profesores con sus correspondientes materias y dias de la semana
Profesores_5to = {"Electronica IV":"Grefa","Redaccion":"R. Guachi","Simulacion":"R. Guachi","Fisica IV":"Oscullo","Informatica":"L. Guachi","Fisica V":"Tirira","Vacio":"Vacio"}
Profesores_6to = {"Proyectos VI":"Duchi","Electronica V":"Grefa","Mecanica VI":"Jacome","Mecanica VII":"Jacome","Sistemas":"Velarde","Instrumentacion":"Corrales","Vacio":"Vacio"}
Profesores_7mo = {"E. Renovables":"Oscullo","Informatica IV":"Corrales","Mecatronica II":"Castro","Proyectos II":"Duchi","Electronica II":"Velarde","Microeconomia":"Altamirano","Vacio":"Vacio"}
Dias_semana = {0:"Lunes",1:"Martes",2:"Miercoles",3:"Jueves",4:"Viernes"}
#Ingresar tamaño de la poblacion
poblacion= 8;
#Cantidad de materias
n_materias=len(materias_5to)
#Inicializar vectores del tamao de la poblaciones
Poblaciones =  [0]*poblacion
Fitness_valor=[0]*poblacion
#Cantidad de sujetos a mutar
mutados=4
#Probabilidad de mutacion
prob_mutacion=0.3
#Maximo numero de generaciones
gen_max=100

#Funcion para que los arrays de horario se vean entendibles y lindos.
def imprimir_horario(horario,pob,profes):
  tabla = prettytable.PrettyTable()
  tabla.field_names=["Lunes","Martes","Miercoles","Jueves","Viernes"]
  for day in range(7):
    mate=[" "," "," "," "," " ]
    pro=[" "," "," "," "," " ]
    for x in range(5):
     mate[x]=horario[pob][x][day]
     pro[x]=profes.get(mate[x])
    tabla.add_row(mate)
    tabla.add_row(pro)
    tabla.add_row([" "," "," "," "," " ])
   
  tabla.header=(True)
  tabla.horizontal_char='—'   
  tabla.junction_char=' '
  tabla.add_column("Hora de clase",["7:00 - 9:00"," "," ","9:00 - 11:00"," "," ","11:00 - 12:00 "," "," ","12:00 - 13:00 ",
                                    " "," ","13:00 - 14:00 "," "," ","14:00 - 16:00 "," "," ","16:00 - 18:00 "," "," "])
  print (tabla)

#Se ordena los sujetos de mejor a peor ordenando de menos conflictos a mas conflictos
def Burbuja(unaLista,unaLista2):
    for numPasada in range(len(unaLista)-1,0,-1):
        for i in range(numPasada):
            if unaLista[i]>unaLista[i+1]:
                temp = unaLista[i]
                temp2 = unaLista2[i]
                unaLista[i] = unaLista[i+1]
                unaLista2[i] = unaLista2[i+1]
                unaLista[i+1] = temp
                unaLista2[i+1] = temp2

    return (unaLista,unaLista2)

#Inicializar un horario ingresando las materias que contiene
def Init_Pob(Horario_init,materias):
  for sujeto in range(poblacion):
    for day in range(5):
        Horario_init[sujeto][day]=random.sample(materias,len(materias))
  return Horario_init


def fitness(Horario_5,Horario_6,Horario_7,pob):
  conflictos=0;
  #Hacer un analisis por cada dia
  for dias in range(5):
     #Hacer un analisis por cada materia
    for materia in range(n_materias):
      #Obtener los profesores que estan impartiendo clase simultaneamente
      Profe_5=Profesores_5to.get(Horario_5[pob][dias][materia])
      Profe_6=Profesores_6to.get(Horario_6[pob][dias][materia])
      Profe_7=Profesores_7mo.get(Horario_7[pob][dias][materia])
      #Si alguno de los profesores esta dando 2 clases al mismo tiempo segun el horario, hay un conflicto.
      #Entre mas conflictos tenga, menor puntuacion tiene el sujeto.
      if(Profe_5==Profe_6 or Profe_5==Profe_7 and Profe_5!="Vacio"):
        conflictos+=1
      if(Profe_6==Profe_7  and Profe_6!="Vacio"):
        conflictos+=1
  return(conflictos)

#Se reinicia un dia completo en caso de que se cumpla la condicion de mutacion.
def mutar(horario,materias):
  for day in range(5):
        if (random.uniform(0,1)<=prob_mutacion):
          horario[day]=random.sample(materias,len(materias))
  return horario



#Cambio generacional
def cambio(horario,poblaciones,materias_mut):
  #Se inicializa el tamaño de la nueva poblacion (los datos que contieen seran sobre escritos)
  nueva_poblacion=horario
  #elitismo (se eligen los mejores 2)
  nueva_poblacion[0]=horario[poblaciones[0]] 
  nueva_poblacion[1]=horario[poblaciones[1]] 
  #Se lanza un dado, si es 0 se corta en lunes, si es 1 en martes y asi sucesivamente
  #Si el dado es 5, los hijos pasan a la siguiente generacion igual a sus padres
  for sujetos in range(2,len(poblaciones)-1,2):
      punto_corte =math.floor(random.uniform(0,5.9))
      
      padre1=horario[poblaciones[sujetos]]
      padre2=horario[poblaciones[sujetos+1]]

      hijo1=padre1
      hijo2=padre2
      if punto_corte==5:
        hijo1=padre1
        hijo2=padre2
      else:
        dia_=0
        while dia_ <= punto_corte:
          hijo1[dia_]=padre1[dia_]
          hijo2[dia_]=padre2[dia_]
          dia_+=1
        while dia_<5:
          hijo2[dia_]=padre1[dia_]
          hijo1[dia_]=padre2[dia_]
          dia_+=1
      nueva_poblacion[sujetos]=hijo1
      nueva_poblacion[sujetos+1]=hijo2
      #mutar a los peores sujetos
      for mutacion in range(1,mutados):
        nueva_poblacion[-mutacion]=mutar(nueva_poblacion[-mutacion],materias_mut)
 #Regresar nueva poblaacion
  return(nueva_poblacion)   



#Inicializar horarios (dimensiones)
Horario_5to = [ [ "0" for i in range(5) ] for j in range(poblacion) ]
Horario_6to = Horario_5to
Horario_7mo = Horario_5to

#Cargar cada sujeto con una lista de materias diarias y transformarlas a NP array para manejarlas mas facil.
Horario_5to=Init_Pob(Horario_5to,materias_5to)
Horario5= np.array(Horario_5to)
Horario_6to=Init_Pob(Horario_6to,materias_6to)
Horario6=np.array(Horario_6to)
Horario_7mo=Init_Pob(Horario_7mo,materias_7mo)
Horario7=np.array(Horario_7mo)

#Contador que nos indica en que generacion nos encontramos
contador_gen=0
while contador_gen<gen_max:
  #Indicar la generacion si es multiplo de 10
  if contador_gen%10==0:
    print("Generacion N°: ",contador_gen)

 #Hacer una iteracion en cada sujeto de las poblaciones
  for pob in range(poblacion):
    #Evaluar la poblacion
    Fitness_valor[pob] =fitness(Horario5,Horario6,Horario7,pob-1)
    #Esta lista es parasaber que sujeto tiene que valor.
    Poblaciones[pob] = pob 
    #Si un sujeto no tiene conflictos, mostrar como solucion e imprimir cada horario
    if(Fitness_valor[pob]==0):
      print("Solucion encontrada en sujeto:",pob,"\n")
      print("Solucion encontrada en la generacion: ",contador_gen)
      print("Horario 5to semestre\n")
      imprimir_horario(Horario5,pob,Profesores_5to)
      print("Horario 6to semestre\n")
      imprimir_horario(Horario6,pob,Profesores_6to)
      print("Horario 5to semestre\n")
      imprimir_horario(Horario7,pob,Profesores_7mo)

      contador_gen=gen_max
      break

#Ordenar sujetos de mejor a peor.
  Fitness_valor,Poblaciones= Burbuja(Fitness_valor,Poblaciones)
  #Realizar los cambios generacionales
  Horario5=cambio(Horario5,Poblaciones,materias_5to)
  Horario6=cambio(Horario6,Poblaciones,materias_6to)
  Horario7=cambio(Horario7,Poblaciones,materias_7mo)
  contador_gen+=1
  
#Repetir :)
