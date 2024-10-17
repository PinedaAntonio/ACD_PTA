# Pedir un número al usuario
num = int(input("Introduce un número entre 1 y 7: "));

if num > 0 and num < 8 :
    if num == 1 :
        print("Es lunes");
    elif num == 2 :
        print("Es martes");
    elif num == 3 :
        print("Es miércoles");
    elif num == 4 :
        print("Es jueves");
    elif num == 5 :
        print("Es viernes");
    elif num == 6 :
        print("Es sábado");
    elif num == 7 :
        print("Es domingo");
else :
    print("El número no está comprendido entre 1 y 7");
        
