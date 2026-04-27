# JOB-SCHEDULER-SIMULATOR

OS-Level Priority Job Scheduler

A Python-based simulation of an Operating System task scheduler. This project uses a **Min-Heap** data structure to manage and execute tasks based on their urgency rather than just their arrival time.

## 🚀 Key Features
* **Priority-Based Execution:** Uses a Min-Heap ($O(\log n)$) to ensure high-priority tasks are handled first.
* **Interactive Dashboard:** A clean UI built with **Streamlit** to add, track, and execute jobs.
* **Live Progress:** Visual feedback showing the "processing" time of each task.
* **Execution Logs:** Keeps a history of completed tasks for auditing.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Data Structures:** Heapq (Min-Heap)
* **Frontend:** Streamlit
* **Data Analysis:** Pandas

## 📦 How to Run
1. **Clone the repository:**

         git clone https://github.com/Jasmin-IT/JOB-SCHEDULER-SIMULATOR.git

2.**Install dependencies:**
   
      pip install streamlit pandas
      or 
      pip install r-requirements.txt
      
3.**Run the application:**
  
  streamlit run app.py
