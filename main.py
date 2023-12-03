from tkinter import *
from tkinter import messagebox
import random

fps = 150
single = 20
C = 10
R = 20
width = C * single
height = R * single
fkxz = {"O": [[-1, -1], [0, -1], [-1, 0], [0, 0]],
        "S": [[-1, 0], [0, 0], [0, -1], [1, -1]],
        "T": [[-1, 0], [0, 0], [0, -1], [1, 0]],
        "I": [[0, 1], [0, 0], [0, -1], [0, -2]],
        "L": [[-1, 0], [0, 0], [-1, -1], [-1, -2]],
        "J": [[-1, 0], [0, 0], [0, -1], [0, -2]],
        "Z": [[-1, -1], [0, -1], [0, 0], [1, 0]]}
fkys = {"O": "blue", "S": "red", "T": "yellow", "I": "green", "L": "purple", "J": "orange", "Z": "Cyan"}


def drawfg(mycanvas, c, r, color="#CCCCCC"):
    x0 = c * single
    y0 = r * single
    x1 = x0 + single
    y1 = y0 + single
    mycanvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white")


def drawjm(mycanvas, jm):
    for i in range(R):
        for j in range(C):
            a = jm[i][j]
            if a:
                drawfg(mycanvas, j, i, fkys[a])
            else:
                drawfg(mycanvas, j, i)


def drawfk(mycanvas, c, r, qy, color="#CCCCCC"):
    for a in qy:
        c1 = c + a[0]
        r1 = r + a[1]
        if 0 <= c1 < C and 0 <= r1 < R:
            drawfg(mycanvas, c1, r1, color)


def move(mycanvas, fk, direction=[0, 0]):
    xz = fk["xz"]  # 形状
    c = fk["wz"][0]  # 位置
    r = fk["wz"][1]
    qy = fk["qy"]  # 区域
    drawfk(mycanvas, c, r, qy)
    newc = c + direction[0]
    newr = r + direction[1]
    fk["wz"] = [newc, newr]
    drawfk(mycanvas, newc, newr, qy, fkys[xz])


def ismove(fk, direction=[0, 0]):
    cc = fk["wz"][0]
    rr = fk["wz"][1]
    for i in fk["qy"]:
        c = cc + i[0] + direction[0]
        r = rr + i[1] + direction[1]
        if c < 0 or c >= C or r >= R:
            return False
        if r >= 0 and jm[r][c]:
            return False
    return True


def sjfk():
    xz = random.choice(list(fkxz.keys()))
    wz = [C // 2, 0]
    newfk = {"xz": xz, "qy": fkxz[xz], "wz": wz}
    return newfk


root = Tk()
s = 0
root.title("俄罗斯方块-得分: %s" % s)
mycanvas = Canvas(root, width=width, height=height)
mycanvas.pack()
jm = []
for i in range(R):
    row = ['' for j in range(C)]
    jm.append(row)
drawjm(mycanvas, jm)


def save(fk):
    xz = fk["xz"]
    cc = fk["wz"][0]
    rr = fk["wz"][1]
    for i in fk["qy"]:
        c = cc + i[0]
        r = rr + i[1]
        jm[r][c] = xz


def yidong(event):
    direction = [0, 0]
    if event.keysym == 'Left':
        direction = [-1, 0]
    elif event.keysym == 'Right':
        direction = [1, 0]
    else:
        return
    global currentfk
    if currentfk is not None and ismove(currentfk, direction):
        move(mycanvas, currentfk, direction)


def isfull(row):
    for i in row:
        if i == '':
            return False
    return True


def clear():
    hasfull = False
    for i in range(len(jm)):
        if isfull(jm[i]):
            hasfull = True
            if i > 0:
                for j in range(i, 0, -1):
                    jm[j] = jm[j - 1][:]
                jm[0] = ['' for j in range(C)]
            else:
                jm[i] = ['' for j in range(C)]
            global s
            s += 10
    if hasfull:
        drawjm(mycanvas, jm)
        root.title("俄罗斯方块-得分: %s" % s)


def sxym():
    mycanvas.update()
    global currentfk
    if currentfk is None:
        newfk = sjfk()
        move(mycanvas, newfk)
        currentfk = newfk
        if not ismove(currentfk):
            messagebox.showinfo("Game over!", "Your score is %s" % s)
            root.destroy()
            return
    else:
        if ismove(currentfk, [0, 1]):
            move(mycanvas, currentfk, [0, 1])
        else:
            save(currentfk)
            currentfk = None
            clear()

    mycanvas.after(fps, sxym)


currentfk = None
mycanvas.focus_set()
mycanvas.bind("<KeyPress-Left>", yidong)
mycanvas.bind("<KeyPress-Right>", yidong)
sxym()
root.mainloop()

