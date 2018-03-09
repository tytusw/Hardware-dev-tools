"""
Smart Resistor Finder inspired by Guigui's code
"""
E3 = [1.0, 2.2, 4.7]
E6 = [1.0, 1.5, 2.2, 3.3, 4.7, 6.8]
E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
E48 = [1.0, 1.05, 1.1, 1.15, 1.2, 1.21, 1.27, 1.3, 1.33, 1.4, 1.47, 1.5, 1.54, 1.6, 1.62, 1.69, 1.78, 1.8, 1.87, 1.96, 2.0, 2.05, 2.15, 2.2, 2.26, 2.37, 2.4, 2.49, 2.61, 2.7, 2.74, 2.87, 3.0, 3.01, 3.16, 3.3, 3.32, 3.48, 3.6, 3.65, 3.83, 3.9, 4.02, 4.22, 4.3, 4.42, 4.64, 4.7, 4.87, 5.1, 5.11, 5.36, 5.6, 5.62, 5.9, 6.19, 6.2, 6.49, 6.8, 6.81, 7.15, 7.5, 7.87, 8.2, 8.25, 8.66, 9.09, 9.1, 9.53]
E96 = [1.0, 1.02, 1.05, 1.07, 1.1, 1.13, 1.15, 1.18, 1.2, 1.21, 1.24, 1.27, 1.3, 1.33, 1.37, 1.4, 1.43, 1.47, 1.5, 1.54, 1.58, 1.6, 1.62, 1.65, 1.69, 1.74, 1.78, 1.8, 1.82, 1.87, 1.91, 1.96, 2.0, 2.05, 2.1, 2.15, 2.2, 2.21, 2.26, 2.32, 2.37, 2.4, 2.43, 2.49, 2.55, 2.61, 2.67, 2.7, 2.74, 2.8, 2.87, 2.94, 3.0, 3.01, 3.09, 3.16, 3.24, 3.3, 3.32, 3.4, 3.48, 3.57, 3.6, 3.65, 3.74, 3.83, 3.9, 3.92, 4.02, 4.12, 4.22, 4.3, 4.32, 4.42, 4.53, 4.64, 4.7, 4.75, 4.87, 4.99, 5.1, 5.11, 5.23, 5.36, 5.49, 5.6, 5.62, 5.76, 5.9, 6.04, 6.19, 6.2, 6.34, 6.49, 6.65, 6.8, 6.81, 6.98, 7.15, 7.32, 7.5, 7.68, 7.87, 8.06, 8.2, 8.25, 8.45, 8.66, 8.87, 9.09, 9.1, 9.31, 9.53, 9.76]
E_dico = {"E3":E3,"E6":E6,"E12":E12,"E24":E24,"E48":E48,"E96":E96}
E_list = ["E3","E6","E12","E24","E48","E96"]
"""
Parametres:
 - Input Voltage
 - Output Voltage
 - Calculation tolerance
 - to complet...

 Vout = Vin * (R2 / R1 + R2)
 k = (R2 / R1 + R2) = Vout / Vin
 R2 = R1 * (k / (1 - k))
 R1 = R2 * ((1 - k) / k)
 k < 1 et k > 0

 Mandatary -> Vout < Vin , I > 0, Tol >= 0

"""

def R_compute(Vin,Vout,Tol,E,E_str,Tol_R):
    k = Vout / Vin
    r1 = 0
    r1_tmp = 0
    r2 = 0
    r2_tmp = 0
    j = 0 # set index j
    i = 0 # set index i
    err = 0
    err_prev = Tol
    result = False
    r1_factor = 1

    if 1/k > 10 and 1/k < 100:
        r1_factor = 10
    elif 1/k > 100 and 1/k < 1000:
        r1_factor = 100
    elif 1/k > 1000 and 1/k < 10000:
        r1_factor = 1000
    elif 1/k > 10000:
        r1_factor = 10000

    while i < len(E):
        while j < len(E):
            r1 = E[i] * r1_factor
            r2 = E[j]
            k_temp = r2 / (r1 + r2)
            if k_temp > k * (1 - Tol) and k_temp < k * (1 + Tol):
                err = abs((k-k_temp)/k)
                if err < err_prev:
                    err_prev = err
                    r1_tmp = r1
                    r2_tmp = r2
                    result = True
            j = j + 1
        j = 0
        i = i + 1

    if result == True:
        r1_min = r1_tmp * (1 - Tol_R)
        r1_max = r1_tmp * (1 + Tol_R)
        r2_min = r2_tmp * (1 - Tol_R)
        r2_max = r2_tmp * (1 + Tol_R)
        voutnom = Vin * (r2_tmp / (r1_tmp + r2_tmp))
        voutmin = Vin * (r2_min / (r1_max + r2_min))
        voutmax = Vin * (r2_max / (r1_min + r2_max))
        print("The best result in Serie",E_str,"is -> R1 = %.2f"% r1_tmp,", R2 =%.2f"% r2_tmp,", k =%.4f"% (r2_tmp/(r1_tmp + r2_tmp)),", Error = %.2f" % (err_prev*100),"%")
        print("Vout nominal = %.3f"% voutnom,"V, Vout min = %.3f"% voutmin,"V, Vout max =  %.3f"% voutmax,"V")
        print("")
    else:
        print("No Result in",E_str)
        print("")


#Parameters
Vin = 12 # Voltage input in Volt
Vout = 2.7# Voltage output in Volt
Tol = 0.001 # tolerance sur Vout
Tol_R = 0.001 # Resistor tolerance
#End Parameters

i = 0

print("With following inputs :")
print("Vin =",Vin,"V")
print("Vout =",Vout,"V")
print("kset =",Vout / Vin)
print("Voltage tolerance =",Tol*100,"%")
print("Resistor tolerance =",Tol_R*100,"%")
print("")

while i < len(E_list):
    R_compute(Vin,Vout,Tol,E_dico[E_list[i]],E_list[i],Tol_R)
    i = i + 1





