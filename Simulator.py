import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, RadioButtons
MU_SUN   = 1.32712440018e20
MU_EARTH = 3.986004418e14
AU = 1.495978707e11
R_EARTH_ORBIT = AU
OMEGA_EARTH = np.sqrt(MU_SUN / R_EARTH_ORBIT**3)
deg = np.pi / 180
DAY = 24 * 3600
YEAR = 365.25 * DAY
def solve_kepler(M, e, tol=1e-10):
    E = M
    for _ in range(50):
        dE = (E - e*np.sin(E) - M) / (1 - e*np.cos(E))
        E -= dE
        if abs(dE) < tol:
            break
    return E

def orbital_elements_to_state(a, e, i, Omega, omega, M):
    E = solve_kepler(M, e)

    nu = 2*np.arctan2(
        np.sqrt(1+e)*np.sin(E/2),
        np.sqrt(1-e)*np.cos(E/2)
    )

    r = a * (1 - e*np.cos(E))

    r_pqw = np.array([r*np.cos(nu), r*np.sin(nu), 0.0])
    v_pqw = np.sqrt(MU_SUN/(a*(1-e**2))) * np.array([
        -np.sin(nu),
        e + np.cos(nu),
        0.0
    ])

    cO, sO = np.cos(Omega), np.sin(Omega)
    ci, si = np.cos(i), np.sin(i)
    co, so = np.cos(omega), np.sin(omega)

    R = (
        np.array([[ cO,-sO,0],[ sO, cO,0],[0,0,1]]) @
        np.array([[1,0,0],[0,ci,-si],[0,si,ci]]) @
        np.array([[ co,-so,0],[ so, co,0],[0,0,1]])
    )

    return R @ r_pqw, R @ v_pqw

def earth_position(t):
    return np.array([
        R_EARTH_ORBIT * np.cos(OMEGA_EARTH * t),
        R_EARTH_ORBIT * np.sin(OMEGA_EARTH * t),
        0.0
    ])

def acceleration(r_ast, t):
    r_e = earth_position(t)
    return (
        -MU_SUN * r_ast / np.linalg.norm(r_ast)**3
        -MU_EARTH * (r_ast - r_e) / np.linalg.norm(r_ast - r_e)**3
    )

def simulate(r0, v0, tf, dt, impulse_time=None, delta_v=None):
    t = 0.0
    r = r0.copy()
    v = v0.copy()
    a = acceleration(r, t)

    ast, earth = [], []

    while t < tf:
        if impulse_time and abs(t - impulse_time) < dt/2:
            v += delta_v

        ast.append(r.copy())
        earth.append(earth_position(t))

        r += v*dt + 0.5*a*dt*dt
        a_new = acceleration(r, t+dt)
        v += 0.5*(a + a_new)*dt
        a = a_new

        t += dt

    return np.array(ast), np.array(earth)


r0, v0 = orbital_elements_to_state(
    a=1.379e11,
    e=0.191,
    i=3.34*deg,
    Omega=204.4*deg,
    omega=126.4*deg,
    M=135.0*deg
)

tf =100 * YEAR
dt = 600

impact_time = 0.5 * YEAR
delta_v = 1e-3 * v0 / np.linalg.norm(v0)

traj_base, earth_traj = simulate(r0, v0, tf, dt)
traj_def, _ = simulate(r0, v0, tf, dt, impact_time, delta_v)

fig, ax = plt.subplots(figsize=(9,8))
plt.subplots_adjust(left=0.28, bottom=0.18)

ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.set_aspect('equal')
ax.grid(True)

sun_dot,   = ax.plot(0, 0, 'yo', markersize=12, label='Sun')
earth_dot, = ax.plot([], [], 'bo', markersize=6, label='Earth')
ast_dot,   = ax.plot([], [], 'r.', label='Apophis')

time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)


mode = "Before Impact"

rax = plt.axes([0.05, 0.5, 0.18, 0.15])
radio = RadioButtons(rax, ('Before Impact', 'After Impact'))

def set_mode(label):
    global mode
    mode = label

radio.on_clicked(set_mode)


speed = 1
paused = False
frame = 0

ax_btn = plt.axes([0.4, 0.05, 0.2, 0.07])
btn = Button(ax_btn, 'Fast Forward')

def toggle_fast(event=None):
    global speed
    speed = 100 if speed == 1 else 1

btn.on_clicked(toggle_fast)

# Keyboard shortcuts
def on_key(event):
    global paused, speed
    if event.key == 'g':
        toggle_fast()
    elif event.key == 'p':
        paused = not paused
    elif event.key == 'n':
        speed = 1

fig.canvas.mpl_connect('key_press_event', on_key)


def update(_):
    global frame

    if not paused:
        frame = (frame + speed) % len(traj_base)

    earth_dot.set_data(
        [earth_traj[frame,0]/AU],
        [earth_traj[frame,1]/AU]
    )

    traj = traj_base if mode == "Before Impact" else traj_def

    ast_dot.set_data(
        [traj[frame,0]/AU],
        [traj[frame,1]/AU]
    )

    sim_days = frame * dt / DAY
    time_text.set_text(
        f"Mode: {mode}\nTime: {sim_days:.1f} days\nSpeed: {speed}×"
    )

    return earth_dot, ast_dot, time_text
ax.legend(
    loc='upper right',
    frameon=True,
    fancybox=True,
    framealpha=0.9
)

ani = FuncAnimation(fig, update, interval=30, blit=True)
plt.legend()
plt.title("Apophis Deflection Mission-Team QWERTY")
plt.show()