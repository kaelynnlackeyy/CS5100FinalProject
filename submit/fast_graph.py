import matplotlib.pyplot as plt
import matplotlib.animation as animation

agent_history=[2091, 2091, 2091, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2108, 2076, 2096, 2096, 2096, 2096, 2096, 2397, 2397, 2397, 2397, 2397, 2487, 2487, 2487, 2487, 2489, 2649, 2681, 2681, 2681, 2681, 2774, 2857, 2857, 2857, 2857, 2857, 2857, 2857, 2857, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2894, 2096, 2096, 2399, 2399, 2399, 2399, 2536, 2536, 2536, 2536, 2536, 2536, 2536, 2536, 2536, 2536, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2586, 2587, 2587, 2587, 2587, 2587, 2587, 2587, 2587, 2587, 2587, 2587, 2587, 2587, 2587, 2587, 2587, 2587, 2587, 2587, 2587, 2644, 2647, 2686, 2686, 2841, 2841, 2841, 2841, 2852, 2852, 2897, 2897, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2993, 2669, 2669, 2669, 2669, 2669, 2669, 2669, 2669, 2669, 2679, 2679, 2679, 2754, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2758, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822, 2822]
generations_history=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]

sl = 0
sub_lists = {0:[], 1:[], 2:[], 3:[], 4:[]}
for i in range(len(agent_history)):
  if i % 100 == 0 and i > 0:
    sl += 1
  sub_lists[sl].append(agent_history[i])

ret_list = []
for j in sub_lists.keys():
  ret_list.append(sub_lists[j])

agent_history = ret_list

y = [
    [3000, 2900, 2800, 2700, 2600],  # Data for Line 1
    [2500, 2400, 2300, 2200, 2100],  # Data for Line 2
    [2000, 2100, 2200, 2300, 2400]   # Data for Line 3
]

x = [1, 2, 3, 4, 5]

def create_graph(x, y):
    x_data, y_data = [], []

    fig, ax = plt.subplots()

    ax.set_xlabel('Generations')
    ax.set_ylabel('Best Agent Score')
    ax.set_title('Generations VS Best Agent Score')
    ax.set_xlim(0, 100)
    ax.set_ylim(2000, 3000)
    lines = []
    for i in range(len(y)):
        line, = ax.plot([], [], label = f'Line {i + 1}', lw = 2)
        lines.append(line)

    def update(frame):
        for i, line in enumerate(lines):
            # Update the data for each line
            line.set_data(x[:frame+1], y[i][:frame+1])

        return lines

    ani = animation.FuncAnimation(fig, update, frames=len(x), interval = 0.5 * 1000, blit = False, repeat = False)
    ax.legend(['2018', '2019', '2020', '2021', '2022'])
    plt.show()
    plt.close(fig)
    return ani

create_graph(generations_history, agent_history)