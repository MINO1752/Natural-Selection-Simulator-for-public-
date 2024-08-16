def visualize_graph():
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    # 데이터를 저장할 빈 리스트 초기화
    x_data = []
    y_data = [[] for _ in range(10)]  # 10개의 빈 리스트 생성

    # 그림과 축 객체 생성
    fig, axs = plt.subplots(5, 2, figsize=(12, 20), sharex=True)

    # 각 축 설정 및 이름 설정
    parameters = [
        'PREY WIDTH', 'PREY HEIGHT', 'PREY SPEED', 'PREY ANGLE', 'PREY LIFE',
        'HUNTER WIDTH', 'HUNTER HEIGHT', 'HUNTER SPEED', 'HUNTER ANGLE', 'HUNTER LIFE'
    ]

    lines = []
    for i, ax in enumerate(axs.flat):
        line, = ax.plot([], [], marker='o')
        lines.append(line)
        ax.set_title(f'{parameters[i]}')
        ax.set_xlim(0, 100)  # 초기 설정, 이후 업데이트 시 자동 조정

    plt.subplots_adjust(hspace=0.5)  # 서브플롯 간의 세로 간격 조정

    # 데이터 업데이트 함수
    def update_plots(x, y):
        for i, ax in enumerate(axs.flat):
            lines[i].set_data(x, y[i])
            ax.relim()
            ax.autoscale_view()
        
        plt.pause(0.1)  # 플롯을 업데이트하기 위해 잠시 멈춤

    # 파일 경로 및 이름 변수
    file_path = "C:\\Users\\pc\\Documents\\GitHub\\NSS\\NSS\\DATA.txt"

    # 데이터 업데이트 시뮬레이션
    i = 0
    while True:  # 무한 루프
        try:
            with open(file_path, 'r') as file:
                PREYWIDTH, PREYHEIGHT, PREYSPEED, PREYANGLE, PREYLIFE, HUNTERWIDTH, HUNTERHEIGHT, HUNTERSPEED, HUNTERANGLE, HUNTERLIFE = map(float, file.read().split())
        except Exception as e:
            print(f"Error reading file: {e}")
            continue

        x_data.append(i)
        
        y_data[0].append(PREYWIDTH)
        y_data[1].append(PREYHEIGHT)
        y_data[2].append(PREYSPEED)
        y_data[3].append(PREYANGLE)
        y_data[4].append(PREYLIFE)  
        y_data[5].append(HUNTERWIDTH)
        y_data[6].append(HUNTERHEIGHT)
        y_data[7].append(HUNTERSPEED)
        y_data[8].append(HUNTERANGLE)
        y_data[9].append(HUNTERLIFE)
        
        update_plots(x_data, y_data)
        
        i += 1
        time.sleep(1)  # 실시간 업데이트 딜레이 시뮬레이션

    plt.show()

if __name__ == "__main__":
    visualize_graph()
