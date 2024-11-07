import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox, ttk
class ProgressTracker:
    def GenerateProgressGraph(self, session, goal):
        target_exercises = [exercise for exercise in session if exercise.name==goal.exercise.get()]
        exercise_info = [(exercise.date, exercise.repetitions) for exercise in target_exercises] 
        exercise_info_sorted = sorted(exercise_info)
        if exercise_info_sorted:
            dates, values = zip(*exercise_info_sorted)
        if exercise_info:
            plt.figure(figsize=(10, 5))
            plt.axhline(y=goal.target.get(), color="red", linestyle="--", label="Цель")
            plt.plot(dates, values, marker='o', color='deepskyblue', label="Прогресс упражнения")
            plt.title(f"Прогресс {goal.exercise.get()}")
            plt.xlabel("Дата")
            plt.ylabel("Количество повторений")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.legend()
            plt.show()
        else:
            messagebox.showinfo("Нет данных", f"У вас 0 тренировок упражнения {goal.exercise.get()}")