import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import re
from exercise import Exercise
from goal import Goal
from progress_tracker import ProgressTracker
class FitnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness Tracker")
        self.tracker = ProgressTracker()
        

        self.session_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.exercise_name = tk.StringVar()
        self.repetitions = tk.IntVar()
        self.weight = tk.DoubleVar()
        self.exercise_options = ["Пресс", "Отжимания", "Приседания"]

        self.goal_exercise = tk.StringVar()
        self.goal_target = tk.IntVar()
        self.goal_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.cur_goal = Goal(exercise=self.goal_exercise, target=self.goal_target, date=self.goal_date)
        self.exercises = []

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Arial", 10), padding=6, relief="flat", background="#4CAF50", foreground="white")
        self.style.configure("TLabel", font=("Arial", 10))
        
        self.CreateWidgets()

    def CreateWidgets(self):

        frame = ttk.Frame(self.root, padding="10 10 10 10")
        frame.pack(pady=10)

        ttk.Label(frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
        date_entry = ttk.Entry(frame, textvariable=self.session_date, width=15)
        date_entry.grid(row=0, column=1)
        date_entry.bind("<FocusOut>", lambda event: self.ValidateDate(self.session_date))

        ttk.Label(frame, text="Название Упражнения:").grid(row=1, column=0, sticky="w")
        exercise_combobox = ttk.Combobox(frame, textvariable=self.exercise_name, values=self.exercise_options, state="readonly", width=15)
        exercise_combobox.grid(row=1, column=1)
        exercise_combobox.set("Выберите упражнение") 

        ttk.Label(frame, text="Количество повторений:").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.repetitions, width=15).grid(row=2, column=1)

        ttk.Label(frame, text="Вес (kg):").grid(row=3, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.weight, width=15).grid(row=3, column=1)

        ttk.Button(frame, text="Добавить тренировку", command=self.AddExercise).grid(row=5, column=0, columnspan=2, pady=10)

        columns = ("date", "exercise", "repetitions", "weight")
        self.session_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        self.session_tree.pack(pady=10)

        self.session_tree.heading("date", text="Дата")
        self.session_tree.heading("exercise", text="Упражнение")
        self.session_tree.heading("repetitions", text="Количество повторений")
        self.session_tree.heading("weight", text="Вес")

        self.session_tree.column("date", width=100, anchor="center")
        self.session_tree.column("exercise", width=150, anchor="center")
        self.session_tree.column("repetitions", width=100, anchor="center")
        self.session_tree.column("weight", width=100, anchor="center")

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        delete_button = ttk.Button(self.root, text="Удалить выбранное упражнение", command=self.DeleteExercise)
        delete_button.pack(pady=5)

        frame_goal = ttk.Frame(self.root, padding="10 10 10 10")
        frame_goal.pack(pady=10)

        ttk.Label(frame_goal, text="Название Упражнения:").grid(row=0, column=0, sticky="w")
        goal_exercise_combobox = ttk.Combobox(frame_goal, textvariable=self.goal_exercise, values=self.exercise_options, state="readonly", width=15)
        goal_exercise_combobox.grid(row=0, column=1)
        goal_exercise_combobox.set("Выберите упражнение") 
        
        ttk.Label(frame_goal, text="Количество повтореий:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame_goal, textvariable=self.goal_target, width=15).grid(row=1, column=1)
 

        ttk.Label(frame_goal, text="Дата Выполнения цели (YYYY-MM-DD):").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame_goal, textvariable=self.goal_date, width=15).grid(row=2, column=1)

        ttk.Button(frame_goal, text="Поставить цель", command=self.SetGoal).grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(self.root, text="Посмотреть график прогресса цели", command=self.ShowProgress).pack(pady=10)



    def ValidateDate(self, date_var):
        date_str = date_var.get()
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        
        if re.match(date_pattern, date_str):
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Неверная дата", f"Дата {date_str} некорректна.")
                date_var.set("")
        else:
            messagebox.showerror("Неверный формат", "Пожалуйста, введите дату в формате YYYY-MM-DD.")
            date_var.set("")

    def AddExercise(self):
        if not self.exercise_name.get() or self.exercise_name.get() == "Выберите упражнение":
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите название упражнения.")
            return
        try:
            session_date = datetime.strptime(self.session_date.get(), "%Y-%m-%d")
            today = datetime.today().date()
            if session_date.date() > today:
                messagebox.showerror("Ошибка", "Дата тренировки не может быть позже сегодняшнего дня.")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную дату в формате YYYY-ММ-DD.")
            return

        exercise = Exercise(
            date=self.session_date.get(),
            name=self.exercise_name.get(),
            repetitions=self.repetitions.get(),
            weight=self.weight.get(),
        )

        
        self.exercises.append(exercise)
        self.session_tree.insert(
            "", "end",
            values=(exercise.date, exercise.name, exercise.repetitions, exercise.weight)
        )

    def DeleteExercise(self):

        selected_item = self.session_tree.selection()

        if not selected_item:
            messagebox.showwarning("Выбор элемента", "Пожалуйста, выберите упражнение для удаления.")
            return

        for item in selected_item:
            values = self.session_tree.item(item, "values")
            for exercise in self.exercises:
                exercise_params = (exercise.date, exercise.name, str(exercise.repetitions), str(exercise.weight))
                if(values == exercise_params):
                    self.exercises.remove(exercise)
                    break
            self.session_tree.delete(item)

    def SetGoal(self):
        if not self.goal_exercise.get() or self.goal_exercise.get() == "Выберите упражнение":
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите название упражнения.")
            return 

        self.cur_goal.UpdateGoal(exercise=self.goal_exercise, target=self.goal_target, date=self.goal_date)
        messagebox.showinfo("Цель Поставлена", f"Цель поставлена для упражнения {self.goal_exercise.get()} с количеством повторений {self.goal_target.get()} к {self.goal_date.get()}")

    def ShowProgress(self):
        if not self.goal_exercise.get() or self.goal_exercise.get() == "Выберите упражнение":
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите название упражнения.")
            return
        exercise_name = self.cur_goal.exercise.get()
        if exercise_name:
            self.tracker.GenerateProgressGraph(self.exercises, self.cur_goal)
        else:
            messagebox.showerror("Ошибка", "Выберете цель для просмотра прогресса.")

root = tk.Tk()
app = FitnessApp(root)
root.mainloop()