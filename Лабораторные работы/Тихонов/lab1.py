"""Лабораторная №1. Тихонов Никита Дмитриевич, 24-ВМз."""
import math
from decimal import Decimal, InvalidOperation
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

MAX_POINTS = 10000

def calculate(values):
    """Точки x0 + i*dx, не превышающие xk; аргументы sin в радианах."""
    try:
        v = [Decimal(str(s).strip().replace(',', '.')) for s in values]
    except (InvalidOperation, ValueError):
        raise ValueError('Введите числа во все девять полей.')
    if len(v) != 9 or not all(s.is_finite() for s in v):
        raise ValueError('Нужны девять конечных чисел.')
    a1,b1,a2,b2,a3,b3,x0,xk,dx = v
    if dx <= 0 or xk < x0:
        raise ValueError('Шаг должен быть положительным, конец не меньше начала.')
    n = int((xk-x0)//dx)+1
    if n > MAX_POINTS:
        raise ValueError('Слишком много точек. Увеличьте шаг (максимум 10000 точек).')
    try:
        coefficients = [float(s) for s in v[:6]]
        rows=[]
        for i in range(n):
            x=float(x0+i*dx)
            y=sum(coefficients[j]*math.sin(coefficients[j+1]*x) for j in (0,2,4))
            if not math.isfinite(x) or not math.isfinite(y):
                raise ValueError('Числа слишком велики для расчёта.')
            rows.append((x,y))
        return rows
    except (OverflowError, ValueError):
        raise ValueError('Числа слишком велики для расчёта либо аргументы функции недопустимы.')

def geometry(rows, width, height):
    left,top,right,bottom=70,30,width-25,height-55
    xmin,xmax=min(x for x,y in rows),max(x for x,y in rows)
    ymin,ymax=min(y for x,y in rows),max(y for x,y in rows)
    if xmin==xmax: xmin,xmax=xmin-1,xmax+1
    if ymin==ymax: ymin,ymax=ymin-1,ymax+1
    # Нормализация предотвращает переполнение разности больших значений.
    xs=max(abs(xmin),abs(xmax),1); ys=max(abs(ymin),abs(ymax),1)
    def px(x): return left+(x/xs-xmin/xs)/(xmax/xs-xmin/xs)*(right-left)
    def py(y): return bottom-(y/ys-ymin/ys)/(ymax/ys-ymin/ys)*(bottom-top)
    return left,top,right,bottom,xmin,xmax,ymin,ymax,px,py

def svg(rows):
    l,t,r,b,x0,x1,y0,y1,px,py=geometry(rows,1000,600)
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="600" viewBox="0 0 1000 600">','<rect width="1000" height="600" fill="white"/>']
    for i in range(6):
        x=l+(r-l)*i/5; y=b-(b-t)*i/5
        xv=x0*(1-i/5)+x1*i/5; yv=y0*(1-i/5)+y1*i/5
        parts += [f'<path d="M {x} {t} V {b} M {l} {y} H {r}" stroke="#ddd" fill="none"/>',f'<text x="{x}" y="{b+22}" text-anchor="middle" font-size="12">{xv:.4g}</text>',f'<text x="{l-8}" y="{y+4}" text-anchor="end" font-size="12">{yv:.4g}</text>']
    points=' '.join(f'{px(x):.3f},{py(y):.3f}' for x,y in rows)
    parts += [f'<rect x="{l}" y="{t}" width="{r-l}" height="{b-t}" fill="none" stroke="black"/>',f'<polyline points="{points}" fill="none" stroke="#175bba" stroke-width="2"/>']
    if len(rows)==1: parts.append(f'<circle cx="{px(rows[0][0])}" cy="{py(rows[0][1])}" r="4" fill="#175bba"/>')
    parts+=['<text x="520" y="590" text-anchor="middle">x</text>','<text x="15" y="25">y(x)</text>','</svg>']
    return '\n'.join(parts)

class App:
    def __init__(self, root):
        self.root=root; self.rows=[]
        root.title('МиСОС — лабораторная №1 — Тихонов Н. Д.'); root.geometry('1100x720')
        box=ttk.Frame(root,padding=10); box.pack(fill='x'); self.entries=[]
        for i,(name,default) in enumerate(zip(('a1','b1','a2','b2','a3','b3','x0','xk','Δx'),('1','1','0.5','2','0.25','3','0','6.28','0.1'))):
            ttk.Label(box,text=name).grid(row=0,column=i)
            entry=ttk.Entry(box,width=10); entry.insert(0,default);entry.grid(row=1,column=i,padx=4);self.entries.append(entry)
        ttk.Button(box,text='Рассчитать',command=self.run).grid(row=1,column=9,padx=8)
        ttk.Button(root,text='Сохранить график SVG',command=self.save).pack(anchor='w',padx=14)
        ttk.Label(root,text='y(x) = a1·sin(b1·x) + a2·sin(b2·x) + a3·sin(b3·x)   |   Углы в радианах').pack(pady=6)
        panel=ttk.Panedwindow(root,orient='horizontal');panel.pack(fill='both',expand=True,padx=10,pady=10)
        frame=ttk.Frame(panel);panel.add(frame,weight=1)
        self.table=ttk.Treeview(frame,columns=('x','y'),show='headings');self.table.heading('x',text='x');self.table.heading('y',text='y(x)')
        self.table.column('x',width=115);self.table.column('y',width=135)
        scroll=ttk.Scrollbar(frame,orient='vertical',command=self.table.yview);self.table.configure(yscrollcommand=scroll.set);scroll.pack(side='right',fill='y');self.table.pack(fill='both',expand=True)
        self.canvas=tk.Canvas(panel,background='white');panel.add(self.canvas,weight=3);self.canvas.bind('<Configure>',lambda e:self.draw())
        self.status=ttk.Label(root,text='Введите параметры и нажмите «Рассчитать».');self.status.pack(pady=6)
    def run(self):
        try: rows=calculate([e.get() for e in self.entries])
        except ValueError as e: messagebox.showerror('Ошибка ввода',str(e));return
        self.rows=rows
        self.table.delete(*self.table.get_children())
        for x,y in rows:self.table.insert('', 'end',values=(f'{x:.8g}',f'{y:.8g}'))
        self.status.configure(text=f'Рассчитано точек: {len(rows)}. Последний x: {rows[-1][0]:.8g}')
        self.draw()
    def draw(self):
        c=self.canvas;c.delete('all')
        if not self.rows or c.winfo_width()<160 or c.winfo_height()<130:return
        l,t,r,b,x0,x1,y0,y1,px,py=geometry(self.rows,c.winfo_width(),c.winfo_height())
        for i in range(6):
            f=i/5;x=l+(r-l)*f;y=b-(b-t)*f
            c.create_line(x,t,x,b,fill='#dddddd');c.create_line(l,y,r,y,fill='#dddddd')
            c.create_text(x,b+18,text=f'{x0*(1-f)+x1*f:.3g}');c.create_text(l-8,y,text=f'{y0*(1-f)+y1*f:.3g}',anchor='e')
        c.create_rectangle(l,t,r,b);c.create_text((l+r)/2,b+40,text='x');c.create_text(22,15,text='y(x)')
        if len(self.rows)>1:c.create_line(*[p for x,y in self.rows for p in (px(x),py(y))],fill='#175bba',width=2)
        else:
            x,y=self.rows[0];c.create_oval(px(x)-4,py(y)-4,px(x)+4,py(y)+4,fill='#175bba')
    def save(self):
        if not self.rows:messagebox.showinfo('График','Сначала выполните расчёт.');return
        path=filedialog.asksaveasfilename(defaultextension='.svg',filetypes=[('SVG','*.svg')],initialfile='graph.svg')
        if path:
            try:Path(path).write_text(svg(self.rows),encoding='utf-8')
            except OSError as e:messagebox.showerror('Ошибка сохранения',str(e))

if __name__=='__main__':
    root=tk.Tk();App(root);root.mainloop()
