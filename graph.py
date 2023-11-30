import math
import pygame

# Vcos(wt) = (q1+q2)/C1 + q2_R2 + q2/C2
# Vcos(wt) = (q1+q2)/C1 + q1_R1

class Graph:
    def __init__(self, render, q1, q2):
        self.render = render
        
        self.V = 150
        self.C1 = 1/1000/4000
        self.R1 = 1000
        self.C2 = 1/1000/2000
        self.R2 = 1000
        self.w = 1
        self.t = 0
        self.dt = 1 / (render.FPS*1000)

        
        self.q1 = q1.copy()
        self.q1_ = [self.V/self.R1]
        self.q2 = q2.copy()
        self.q2_ = [self.V/self.R2]
        self.q2w = []
        self.V_ = []

        # 그래프 너비, 높이
        self.graph_width = 0.1
        self.height = 100

        # 그래프의 색깔, 위치
        self.colors = {'1': pygame.Color('red'), '2': pygame.Color('blue')}
        self.positions = {'1': 150, '2': 400}

        self.font = pygame.font.SysFont("Consolas", 15)
        # n 주기까지 그림
        self.graph_len = 8

        for j in range(8000):
            for i in range(8000):
                self.update()
            self.qwupdate()
            self.q1 = q1.copy()
            self.q1_ = [self.V/self.R1]
            self.q2 = q2.copy()
            self.q2_ = [self.V/self.R2]
            self.V_ = []

    def draw(self):
        '''
        모든 데이터를 그리고 극댓값을 표시함
        '''
        for key, data in zip(self.colors.keys(), [self.q2w]):

            max_val = max([abs(value) for value in data]+[0.0001])
            self.draw_line((100, self.positions[key]), max_val)
            scale_factor = self.height / max_val

            for i in range(len(data)):
                # if i != len(data)-1:
                #     if data[i] > data[i-1] and data [i] > data[i+1] and data[i]:
                #         self.render.screen.blit(self.font.render("%.2e"%(data[i]), True, pygame.Color('black')), (70+i*self.graph_width, self.positions[key]-data[i]*scale_factor-20))
                pygame.draw.circle(self.render.screen, self.colors[key], 
                                   (100 + i * self.graph_width, - data[i] * scale_factor + self.positions[key]), 2)
                

    def draw_line(self, pos, max_val):
        '''
        그래프의 틀을 그림
        '''
        x, y = pos
        pygame.draw.line(self.render.screen, pygame.Color('gray'), pos, [x + self.graph_len*100, y], 3)
        for i, v in [(100, -max_val), (50, -max_val/2), (-50, max_val/2), (-100, max_val)]:
            # pygame.draw.line(self.render.screen, pygame.Color('gray'), [x, y+i], [x + self.graph_len*100, y+i], 1)
            self.render.screen.blit(self.font.render("%.2e"%(v), True, pygame.Color("black")), (x-80, y+i-7))
        
        self.render.screen.blit(self.font.render("0", True, pygame.Color("black")), (x-15, y-7))

        pygame.draw.line(self.render.screen, pygame.Color('gray'), [x, y-100], [x, y+100], 3)
        # for i in range(1, self.graph_len+1):
        #     pygame.draw.line(self.render.screen, pygame.Color('gray'), [x+100*i, y-100], [x+100*i, y+100], 1)

    def update(self):
        '''
        시간에 따른 변화를 업데이트함
        '''
        self.V_.append(self.V * math.cos(self.w * self.t))
        self.q1.append(self.q1[-1] + self.q1_[-1]*self.dt)
        self.q2.append(self.q2[-1] + self.q2_[-1]*self.dt)
        self.q1_.append((self.V_[-1]*self.C1-self.q1[-1]-self.q2[-1])/(self.R1*self.C1))
        self.q2_.append((self.V_[-1]*self.C1-(1+self.C1/self.C2)*self.q2[-1]-self.q1[-1])/(self.R2*self.C1))

        self.t += self.dt

    def qwupdate(self):
        self.q2w.append(max(self.q2[4000:8000])/self.V/self.C2)
        self.w += 10
