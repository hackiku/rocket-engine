
# ulazni podaci

mg = 1  # maseni protok goriva
OF = 5  # odnos mesanja oksidator/gorivo
P = 100 * 10**5  # pritisak u komori
Lkar = 1  # karakteristicna duzina
Cstar = 2376  # (2000) karakteristicna brzina
epsilon_i = 6  # stepen sirenja mlaznika
dkdtkr = 2.5  # odnos precnika komore i grla mlaznika
R = 546  # (546) gasna konstanta
k = 1.2  # (1.2) odnos specificnih toplota pri konstantnom pritisku i zapremini
Pa = 101325  # atmosferski pritisak

# proracun

# Calculations
mox = OF * mg  # maseni protok oksidatora
mox_original = 5
print(f"mox = {mox}", "|", mox_original, "|", mox - mox_original)  # mox = 5

Akr = Cstar * (mg + mox) / P  # kriticni presek mlaznika
Akr_original = 1.2 * 10**-3
print(f"Akr = {Akr:.6f}", "|", f"{Akr_original:.6f}", "|", Akr - Akr_original)  # Akr = 1.2 x 10^-3

d_kr = (Akr * 4 / 3.14159)**0.5  # precnik kriticnog preseka mlaznika
d_kr_original = 0.039
print(f"d_kr = {d_kr:.3f}", "|", d_kr_original, "|", (d_kr - d_kr_original):.3f)  # d_kr = 0.039

V_kom = Lkar * Akr  # zapremina komore
V_kom_original = 1.2 * 10**-3
print(f"V_kom = {V_kom:.6f}", "|", f"{V_kom_original:.6f}", "|", V_kom - V_kom_original)  # V_kom = 1.2 x 10^-3

d_k = dkdtkr * d_kr  # precnik komore
d_k_original = 0.098
print(f"d_k = {d_k:.3f}", "|", d_k_original, "|", d_k - d_k_original)  # d_k = 0.098

l_k = V_kom / (d_k**2 * 3.14159 / 4)  # duzina komore
l_k_original = 0.16
print(f"l_k = {l_k:.2f}", "|", l_k_original, "|", l_k - l_k_original)  # l_k = 0.16

A_i = epsilon_i * Akr  # izlazni presek i precnik mlaznika
A_i_original = 7.2 * 10**-3
print(f"A_i = {A_i:.6f}", "|", f"{A_i_original:.6f}", "|", A_i - A_i_original)  # A_i = 7.2 x 10^-3

d_i = (A_i * 4 / 3.14159)**0.5  # precnik izlaznog preseka mlaznika
d_i_original = 0.096
print(f"d_i = {d_i:.3f}", "|", d_i_original, "|", d_i - d_i_original)  # d_i = 0.096
