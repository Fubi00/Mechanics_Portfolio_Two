import numpy as np
import matplotlib.pyplot as plt

# Globale verdier
A = 0
B = 0.75
x = np.linspace(A, B, 1000)

x1 = x[x < 0.375]
x2 = x[(x >= 0.375) & (x < 0.5)]
x3 = x[x >= 0.5]

vinkel_deg = 20
theta_deg = np.arctan(10 / 0.25) * 180 / np.pi  # ≈ 88.5679
vinkel_rad = np.deg2rad(vinkel_deg)
theta_rad = np.deg2rad(theta_deg)

G = 98.1  # N
L = 0.75  # m
Ax = 101.1081
Ay = 47.4782
Qx = 0.5763
Qy = 1.8015

def P(x):
    return np.piecewise(x,
                        [x < 0.375,
                         (x >= 0.375) & (x < 0.5),
                         x >= 0.5],
                        [lambda x: -101.1081 + (98.1/0.75) * x * np.sin(vinkel_rad),
                         lambda x: -101.6844 + (98.1/0.75) * x * np.sin(vinkel_rad),
                         lambda x: -101.6844 + (98.1/0.75) * x * np.sin(vinkel_rad)])
def V(x):
    return np.piecewise(x,
        [x <= 0.375,
         (x > 0.375) & (x <= 0.5),
         x > 0.5],
        [
            # Cut 1
            lambda x: Ay - (G / L) * x * np.cos(vinkel_rad),

            # Cut 2
            lambda x: (Ay - Qy) - (G / L) * x * np.cos(vinkel_rad),

            # Cut 3 (inkluder F_y)
            lambda x: (
                (Ay - Qy) -
                (G / L) * x * np.cos(vinkel_rad) -
                (5 + (0.75 - x) * np.tan(theta_rad)) * (x - 0.5) -
                0.5 * (10 - (0.75 - x) * np.tan(theta_rad)) * (x - 0.5)
            )
        ])
def M(x):
    return np.piecewise(x,
        [x <= 0.375,
         (x > 0.375) & (x <= 0.5),
         x > 0.5],
        [
            # Cut 1
            lambda x: -(G * np.cos(vinkel_rad)) / (2 * L) * x**2 + Ay * x,

            # Cut 2
            lambda x: (
                - (G * np.cos(vinkel_rad)) / (2 * L) * x**2 +
                Ay * x -
                Qy * (x - 0.375)
            ),

            # Cut 3
            lambda x: (
                - (G * np.cos(vinkel_rad)) / (2 * L) * x**2 +
                Ay * x -
                Qy * (x - 0.375) -
                (5 + (0.75 - x) * np.tan(theta_rad)) * (x - 0.5) * (x - 0.5 - 0.5 * (x - 0.5)) -
                0.5 * (10 - (0.75 - x) * np.tan(theta_rad)) * (x - 0.5) * (x - 0.5 - (1/3) * (x - 0.5))
            )
        ])

# Plotting P(x)
plt.figure(figsize=(10, 6))

plt.plot(x1, P(x1), label='P(x) for x < 0.375', color='slateblue')
plt.plot(x2, P(x2), label='P(x) for 0.375 <= x < 0.5', color='darkorange')
plt.plot(x3, P(x3), label='P(x) for x >= 0.5', color='forestgreen')

# Legg til vertikale hopp-streker
plt.plot([0.375, 0.375], [P(0.375 - 1e-6), P(0.375 + 1e-6)], 'k--')  # Hopp ved 0.375
plt.plot([0.5, 0.5], [P(0.5 - 1e-6), P(0.5 + 1e-6)], 'k--')  # Hopp ved 0.5

plt.title('Plot of P(x)')
plt.xlabel('x (m)')
plt.ylabel('P(x) (N)')
plt.axhline(0, color='black', lw=0.5, ls='--')
plt.legend()
plt.grid(True)
plt.xlim(A-0.05, B+0.05)
plt.ylim(-105, -65)
plt.savefig("Diagram P(x).pdf", format='pdf', bbox_inches='tight')
plt.show()

# Plotting V(x)
plt.figure(figsize=(10, 6))

plt.plot(x1, V(x1), label='V(x) for x < 0.375', color='slateblue')
plt.plot(x2, V(x2), label='V(x) for 0.375 <= x < 0.5', color='darkorange')
plt.plot(x3, V(x3), label='V(x) for x >= 0.5', color='forestgreen')

# Legg til vertikale hopp-streker
plt.plot([0.375, 0.375], [V(0.375 - 1e-6), V(0.375 + 1e-6)], 'k--') # Hopp ved 0.375
plt.plot([0.5, 0.5], [V(0.5 - 1e-6), V(0.5 + 1e-6)], 'k--') # Hopp ved 0.5

plt.title('Plot of V(x)')
plt.xlabel('x (m)')
plt.ylabel('V(x) (N)')
plt.axhline(0, color='black', lw=0.5, ls='--')
plt.legend()
plt.grid(True)
plt.savefig("Diagram V(x).pdf", format='pdf', bbox_inches='tight')
plt.show()

# Plotting M(x)
plt.figure(figsize=(10, 6))

plt.plot(x1, M(x1), label='M(x) for x < 0.375', color='slateblue')
plt.plot(x2, M(x2), label='M(x) for 0.375 <= x < 0.5', color='darkorange')
plt.plot(x3, M(x3), label='M(x) for x >= 0.5', color='forestgreen')

plt.title('Plot of M(x)')
plt.xlabel('x (m)')
plt.ylabel('M(x) (Nm)')
plt.axhline(0, color='black', lw=0.5, ls='--')
plt.legend()
plt.grid(True)
plt.savefig("Diagram M(x).pdf", format='pdf', bbox_inches='tight')
plt.show()