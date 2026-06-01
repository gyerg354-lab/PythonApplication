# Додаток А. Повний код основного модуля системи
# network_anomaly_detector.py
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
from datetime import datetime
import csv
import os

class NetworkAnomalyDetector:
    def __init__(self):
        self.running = False
        self.anomalies = []
        self.log_file = "anomaly_log.csv"
        self.times = []
        self.scores = []
        self.init_csv()

    def init_csv(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Час", "Тип аномалії", "Оцінка аномальності"])

    def log_anomaly(self, score):
        timestamp = datetime.now().strftime('%H:%M:%S')
        anomaly_type = "Аномалія (симуляція)"
        
        self.anomalies.append({'time': timestamp, 'type': anomaly_type, 'score': score})
        self.times.append(datetime.now())
        self.scores.append(score)
        
        with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, anomaly_type, round(score, 2)])

    def simulate_traffic(self):
        while self.running:
            if np.random.rand() < 0.15:
                score = np.random.uniform(-0.95, -0.25)
                self.log_anomaly(score)
                print(f"⚠️ Аномалія о {datetime.now().strftime('%H:%M:%S')} | Score: {score:.2f}")
            time.sleep(0.7)

    def start(self):
        if self.running: return
        self.running = True
        thread = threading.Thread(target=self.simulate_traffic, daemon=True)
        thread.start()
        print("✅ Моніторинг запущено")

    def stop(self):
        self.running = False
        print("⛔ Моніторинг зупинено")

# ==================== ІНТЕРФЕЙС З ГРАФІКОМ ====================
def main():
    detector = NetworkAnomalyDetector()
    root = tk.Tk()
    root.title("Інтерактивна система виявлення аномалій у мережевому трафіку")
    root.geometry("1300x750")

    tk.Label(root, text="Інтерактивна система виявлення аномалій у мережевому трафіку", 
             font=("Arial", 16, "bold")).pack(pady=10)

    # Кнопки
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=8)
    tk.Button(btn_frame, text="▶ Запустити моніторинг", bg="#28a745", fg="white", 
              font=("Arial", 10, "bold"), width=25, height=2, command=detector.start).pack(side=tk.LEFT, padx=20)
    tk.Button(btn_frame, text="⛔ Зупинити", bg="#dc3545", fg="white", 
              font=("Arial", 10, "bold"), width=25, height=2, command=detector.stop).pack(side=tk.LEFT, padx=20)

    # Графік
    tk.Label(root, text="Графік оцінки аномальності в реальному часі:", 
             font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(15,5))
    
    fig, ax = plt.subplots(figsize=(11, 4))
    canvas = FigureCanvasTkAgg(fig, root)
    canvas.get_tk_widget().pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
    
    ax.set_title("Оцінка аномальності (нижче -0.3 = аномалія)")
    ax.set_xlabel("Час")
    ax.set_ylabel("Оцінка аномальності")
    ax.grid(True, alpha=0.3)
    ax.axhline(y=-0.3, color='red', linestyle='--', alpha=0.7, label="Поріг аномалії")

    # Журнал
    tk.Label(root, text="Журнал аномалій:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(10,5))
    log_text = tk.Text(root, height=8, font=("Consolas", 10))
    log_text.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

    def update_graph():
        while True:
            if detector.scores:
                ax.clear()
                ax.plot(detector.times, detector.scores, 'b-o', linewidth=2, markersize=4)
                ax.axhline(y=-0.3, color='red', linestyle='--', alpha=0.7)
                ax.set_title("Оцінка аномальності в реальному часі")
                ax.set_xlabel("Час")
                ax.set_ylabel("Score")
                ax.grid(True, alpha=0.3)
                canvas.draw()
            time.sleep(1)

    def update_log():
        while True:
            if detector.anomalies:
                anomaly = detector.anomalies.pop(0)
                log_entry = f"[{anomaly['time']}] {anomaly['type']} | Score: {anomaly['score']:.2f}\n"
                log_text.insert(tk.END, log_entry)
                log_text.see(tk.END)
            time.sleep(0.4)

    threading.Thread(target=update_graph, daemon=True).start()
    threading.Thread(target=update_log, daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main()
