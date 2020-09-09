import numpy as np
import skfuzzy as fuzz
from matplotlib import pyplot as plt

escala_padecimiento = np.linspace(0,10,100)
#Funciones de pertenencia de entrada

# Funciones triangulares y trapezoidales
epf_alta_puntuacion = fuzz.trapmf (escala_padecimiento,[3,7,10,10])
epf_moderada_puntuacion = fuzz.trimf(escala_padecimiento,[3,5,7])
epf_baja_puntuacion = fuzz.trapmf (escala_padecimiento,[0,0,3,7] )

#Funcion en S
epf_alta_puntuacion_s = fuzz.smf(escala_padecimiento,3,7)
epf_baja_puntuacion_s = fuzz.zmf(escala_padecimiento,3,7)
epf_moderada_puntuacion_gauss = fuzz.gbellmf(escala_padecimiento,1,4.5,5)


#Funciones de pertenecia de salida 
egf_leve = fuzz.zmf(escala_padecimiento,2,4)
egf_moderada = fuzz.gbellmf(escala_padecimiento,0.5,2,4)
egf_alta = fuzz.gbellmf(escala_padecimiento,0.5,2,6)
egf_muy_alta = fuzz.smf(escala_padecimiento,6,8)


def fuzzificacion_valor(valor,f_pertenencia):
    valor_fuzz = fuzz.interp_membership(escala_padecimiento,f_pertenencia,valor)
    return valor_fuzz

#fuzzificacion_valor(val_dc)

def cut(value, mf):
    value = float(value)
    aux = np.zeros(mf.size)
    if (type(value) is int) or (type(value) is float):
        for i in range(mf.size):
            aux[i] = min(value, mf[i])
        return aux
    else:
        return -1

def union(data):
    aux = np.zeros(data[0].size)
    for j in range(len(data)):
        for i in range(aux.size):
            aux[i] = max(aux[i], data[j][i])
    return aux 
            

def responder_pregunta():
    respuesta_valida = False
    while(respuesta_valida == False):
        numero = input()
        numero = float(numero)
        if(numero <= 10 and numero >= 0):
            return numero
        print("recuerde responder entre 0 y 10")
    return 0

def registra_temperatura():
    respuesta_valida = False
    numero = ''
    while numero is not float:
        try:
            numero = float(input())
            break
        except ValueError:
            print('Por favor ingrese un valor valido: ')
    return numero


def preguntas_usuario(respuestas):
    print("A continuacion se le consultara por el grado de sus sintomas, debe contestar de 0(ausencia de sintoma) a 10(sintoma muy fuerte), puede responder con decimasles como 1.2 ")
    preguntas = [
        "Nivel de dolor de cabeza: ",
        "Nivel de nauseas",
        "Nivel de dolores musculares",
        "Nivel de fatiga",
        "Nivel congestion nasal",
        "Nivel de escalofrios",
        "Nivel de tos"
    ]
    for pregunta in preguntas:
        print(pregunta)
        print("recuerde responder entre 0 y 10")
        respuesta = responder_pregunta()
        respuestas.append(respuesta)

    print("Ahora ingrese su ultima temperatura registrada")
    temperatura  = registra_temperatura()
    print(temperatura)
    temp_norm = (temperatura - 35) / 5
    if(temp_norm >= 1):
        respuestas.append(1 * 10)
    elif(temp_norm < 0):
        respuestas.append(0)
    else:
        respuestas.append(temp_norm * 10)
    return respuestas


def fuzzificar_variables_entrada(valores_fuzz, respuestas):
    valores_fuzz["val_dc"][0] = fuzzificacion_valor(respuestas[0],epf_baja_puntuacion_s)
    valores_fuzz["val_dc"][1] = fuzzificacion_valor(respuestas[0],epf_moderada_puntuacion_gauss)
    valores_fuzz["val_dc"][2] = fuzzificacion_valor(respuestas[0],epf_alta_puntuacion_s)

    valores_fuzz["val_na"][0] = fuzzificacion_valor(respuestas[1],epf_baja_puntuacion_s)
    valores_fuzz["val_na"][1] = fuzzificacion_valor(respuestas[1],epf_moderada_puntuacion_gauss)
    valores_fuzz["val_na"][2] = fuzzificacion_valor(respuestas[1],epf_alta_puntuacion_s)

    valores_fuzz["val_dm"][0] = fuzzificacion_valor(respuestas[2],epf_baja_puntuacion_s)
    valores_fuzz["val_dm"][1] = fuzzificacion_valor(respuestas[2],epf_moderada_puntuacion_gauss)
    valores_fuzz["val_dm"][2] = fuzzificacion_valor(respuestas[2],epf_alta_puntuacion_s)

    valores_fuzz["val_fa"][0] = fuzzificacion_valor(respuestas[3],epf_baja_puntuacion_s)
    valores_fuzz["val_fa"][1] = fuzzificacion_valor(respuestas[3],epf_moderada_puntuacion_gauss)
    valores_fuzz["val_fa"][2] = fuzzificacion_valor(respuestas[3],epf_alta_puntuacion_s)

    valores_fuzz["val_cn"][0] = fuzzificacion_valor(respuestas[4],epf_baja_puntuacion_s)
    valores_fuzz["val_cn"][1] = fuzzificacion_valor(respuestas[4],epf_moderada_puntuacion_gauss)
    valores_fuzz["val_cn"][2] = fuzzificacion_valor(respuestas[4],epf_alta_puntuacion_s)

    valores_fuzz["val_esc"][0] = fuzzificacion_valor(respuestas[5],epf_baja_puntuacion_s)
    valores_fuzz["val_esc"][1] = fuzzificacion_valor(respuestas[5],epf_moderada_puntuacion_gauss)
    valores_fuzz["val_esc"][2] = fuzzificacion_valor(respuestas[5],epf_alta_puntuacion_s)

    valores_fuzz["val_tos"][0] = fuzzificacion_valor(respuestas[6],epf_baja_puntuacion_s)
    valores_fuzz["val_tos"][1] = fuzzificacion_valor(respuestas[6],epf_moderada_puntuacion_gauss)
    valores_fuzz["val_tos"][2] = fuzzificacion_valor(respuestas[6],epf_alta_puntuacion_s)

    valores_fuzz["val_fiebre_norm"][0] = fuzzificacion_valor(respuestas[7],epf_baja_puntuacion_s)
    valores_fuzz["val_fiebre_norm"][1] = fuzzificacion_valor(respuestas[7],epf_moderada_puntuacion_gauss)
    valores_fuzz["val_fiebre_norm"][2] = fuzzificacion_valor(respuestas[7],epf_alta_puntuacion_s)

    return valores_fuzz


#SI el dolor de cabeza es leve y las náuseas y vómitos son leves y el dolor muscular es leve y la fatiga es leve y la congestión nasal es moderada ENTONCES la influenza es leve.
def primera_regla_inf(valores_fuzzy):
    valor_min = min(valores_fuzzy["val_dc"][0], valores_fuzzy["val_na"][0],valores_fuzzy["val_dm"][0], valores_fuzzy["val_cn"][1])
    corte_salida = cut(valor_min,egf_leve)
    return corte_salida

#SI el dolor de cabeza es moderado y las náuseas y vómitos son leves y el dolor muscular es moderado y la tos es moderada y la congestión nasal es severa ENTONCES la influenza es moderada.
def segunda_regla_inf(valores_fuzzy):
    valor_min = min(valores_fuzzy["val_dc"][1],valores_fuzzy["val_na"][0],valores_fuzzy["val_dm"][1],valores_fuzzy["val_tos"][1],valores_fuzzy["val_cn"][2])
    corte_salida = cut(valor_min,egf_moderada)
    return corte_salida

#SI fiebre es moderada y el dolor de cabeza es leve y las náuseas y vómitos son moderados y el dolor muscular es moderado y la fatiga es moderada y los escalofríos son moderados y la congestión nasal es severa ENTONCES la influenza es moderada.
def tercera_regla_inf(valores_fuzzy):
    valor_min = min(valores_fuzzy["val_fiebre_norm"][1], valores_fuzzy["val_dc"][0],valores_fuzzy["val_na"][1], valores_fuzzy["val_dm"][1], valores_fuzzy["val_fa"][1], valores_fuzzy["val_esc"][1], valores_fuzzy["val_cn"][1])
    corte_salida = cut(valor_min,egf_moderada)
    return corte_salida

#SI fiebre es alta y el dolor de cabeza es moderado y el dolor muscular es moderado y los escalofríos son altos ENTONCES la influenza es muy alta.
def cuarta_regla_inf(valores_fuzzy):
    valor_min = min(valores_fuzzy["val_fiebre_norm"][2], valores_fuzzy["val_dc"][1],valores_fuzzy["val_dm"][1], valores_fuzzy["val_esc"][2])
    corte_salida = cut(valor_min,egf_muy_alta)
    return corte_salida

#SI el dolor de cabeza es moderado y el dolor muscular es alto y la fatiga es moderada y la tos es leve y la congestión nasal es leve ENTONCES la influenza es moderada.
def quinta_regla_inf(valores_fuzzy):
    valor_min = min(valores_fuzzy["val_dc"][1], valores_fuzzy["val_dm"][2],valores_fuzzy["val_fa"][1], valores_fuzzy["val_tos"][0], valores_fuzzy["val_cn"][0])
    corte_salida = cut(valor_min,egf_moderada)
    return corte_salida

#SI el dolor de cabeza es alto y las náuseas y vómitos son altos y el dolor muscular es moderado y la tos es leve y la congestión nasal es moderada ENTONCES la influenza es alta.
def sexta_regla_inf(valores_fuzzy):
    valor_min = min(valores_fuzzy["val_dc"][2], valores_fuzzy["val_na"][2],valores_fuzzy["val_dm"][1], valores_fuzzy["val_tos"][0],valores_fuzzy["val_cn"][1])
    corte_salida = cut(valor_min,egf_alta)
    return corte_salida

def sis_inferencia(valores_fuzzy):
    regla_1 = primera_regla_inf(valores_fuzzy)
    regla_2 = segunda_regla_inf(valores_fuzzy)
    regla_3 = tercera_regla_inf(valores_fuzzy)
    regla_4 = cuarta_regla_inf(valores_fuzzy)
    regla_5 = quinta_regla_inf(valores_fuzzy)
    regla_6 = sexta_regla_inf(valores_fuzzy)
    resultados = [regla_1,regla_2,regla_3,regla_4,regla_5,regla_6]
    union_resultados = union(resultados)
    return union_resultados

def main():
    valores_usuario = []
    valores_fuzzy = {
        "val_dc" : [0,0,0], # valor asociado al dolor de cabeza
        "val_na" : [0,0,0], # valor asociado al nivel de nauseas
        "val_dm" : [0,0,0], # valor asociado a los dolores musculares
        "val_fa" : [0,0,0], # valor asociado a la fatiga
        "val_cn" : [0,0,0], # valor asociado a la congestion nasal
        "val_esc" : [0,0,0], # valor asociado a los escalofrios
        "val_tos" : [0,0,0], # valor asociado a la tos
        "val_fiebre_norm" : [0,0,0], # valor asociado a la fiebre despues de normalizar
    }

    valores_usuario = preguntas_usuario(valores_usuario)# funcion que le pregunta al usuario sus sintomas
    valores_fuzzy = fuzzificar_variables_entrada(valores_fuzzy, valores_usuario)# se fusifican los valores de entrada
    sistema_i = sis_inferencia(valores_fuzzy)# los valores se pasan por un sistema de inferencia y salen los valores despues de ña inferencia de madmani y la union
    salida = fuzz.defuzz(escala_padecimiento,sistema_i,'centroid')# Este valor es el resultado de la desfusificacion y este hay que interpretarlo para dar un veredicto al paciente

    print(salida) 

    fig, entradas = plt.subplots(2, sharex=True, sharey=True)
    entradas[0].plot(escala_padecimiento,sistema_i,label = 'baja')
    entradas[1].plot(escala_padecimiento,egf_leve,label = 'alta')
    entradas[1].plot(escala_padecimiento,egf_moderada,label = 'moderada')
    entradas[1].plot(escala_padecimiento,egf_alta,label = 'baja')
    entradas[1].plot(escala_padecimiento,egf_muy_alta,label = 'baja')
    plt.show()


    return 0


main()


#entradas[0].plot(escala_padecimiento,epf_alta_puntuacion,label = 'alta')
#entradas[0].plot(escala_padecimiento,epf_moderada_puntuacion,label = 'moderada')
#entradas[0].plot(escala_padecimiento,epf_baja_puntuacion,label = 'baja')
#entradas[0].plot(escala_padecimiento,epf_baja_puntuacion_s,label = 'baja')
#entradas[0].plot(escala_padecimiento,epf_alta_puntuacion_s,label = 'baja')
#entradas[0].plot(escala_padecimiento,epf_moderada_puntuacion_gauss,label = 'baja')
#entradas[0].plot(escala_padecimiento,x,label = 'baja')
""" entradas[1].plot(escala_padecimiento,egf_leve,label = 'alta')
entradas[1].plot(escala_padecimiento,egf_moderada,label = 'moderada')
entradas[1].plot(escala_padecimiento,egf_grave,label = 'baja')
entradas[1].plot(escala_padecimiento,egf_muy_grave,label = 'baja') """

#entradas.xlabel('Nivel')
#entradas.ylabel('$\mu(nivel)$')
