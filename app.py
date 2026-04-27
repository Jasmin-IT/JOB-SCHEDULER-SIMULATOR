import streamlit as st
import heapq
import time
import pandas as pd

# Page config
st.set_page_config(page_title="Job Scheduler Simulator", page_icon="⏱️", layout="wide")

# Custom CSS for aesthetics (glassmorphism, modern design)
st.markdown("""
<style>
    /* Dark mode aesthetics */
    .stApp {
        /* Removed custom background color as requested */
    }
    
    /* Remove default Streamlit padding to get rid of empty spaces */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* Hide default header and footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Card style for elements */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 15px;
    }
    
    h1, h2, h3, p, label, .stMarkdown {
        /* color removed so it uses default Streamlit colors based on the user's theme */
    }

    /* Style dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
    }

</style>
""", unsafe_allow_html=True)


class Job:
    def __init__(self, job_id, name, priority, duration, arrival_time):
        self.job_id = job_id
        self.name = name
        self.priority = priority
        self.duration = duration
        self.arrival_time = arrival_time

    # Custom less-than operator for the Priority Queue (Min-Heap)
    def __lt__(self, other):
        # Compare by priority first (lower number = higher priority)
        if self.priority != other.priority:
            return self.priority < other.priority
        # If priorities are equal, compare by arrival time (FIFO for ties)
        return self.arrival_time < other.arrival_time

    def to_dict(self):
        return {
            "Priority": self.priority,
            "Job ID": self.job_id,
            "Name": self.name,
            "Duration (s)": self.duration,
            "Arrival Time": time.strftime('%H:%M:%S', time.localtime(self.arrival_time))
        }

# Initialize session state variables
if 'job_counter' not in st.session_state:
    st.session_state.job_counter = 1
if 'priority_queue' not in st.session_state:
    st.session_state.priority_queue = [] # This will be our min-heap
if 'execution_log' not in st.session_state:
    st.session_state.execution_log = []

st.markdown("<h1 style='text-align: center;'>⏱️ OS Job Scheduler Simulator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #a4b0be !important;'>Uses a <strong>Priority Queue (Min-Heap)</strong> Data Structure to simulate how an Operating System schedules tasks. Jobs with higher priority (lower numerical value) are executed first.</p><hr/>", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("➕ Add New Job")
    
    with st.form("add_job_form", clear_on_submit=True):
        job_name = st.text_input("Job Name", placeholder="e.g., Video Render, OS Update")
        # Lower number = higher priority. 1 is highest.
        priority = st.number_input("Priority Level (1=Highest, 5=Lowest)", min_value=1, max_value=5, value=3)
        duration = st.slider("Estimated Duration (seconds)", min_value=1, max_value=10, value=2)
        
        submitted = st.form_submit_button("Submit Job", use_container_width=True)
        if submitted:
            if job_name:
                new_job = Job(
                    job_id=f"J{st.session_state.job_counter:03d}",
                    name=job_name,
                    priority=priority,
                    duration=duration,
                    arrival_time=time.time()
                )
                # Push job to the heap (priority queue)
                heapq.heappush(st.session_state.priority_queue, new_job)
                st.session_state.job_counter += 1
                st.success(f"Job '{job_name}' added to priority queue!")
            else:
                st.error("Please enter a job name.")
    
    # Execution Log
    col_hist1, col_hist2 = st.columns([3, 2])
    with col_hist1:
        st.subheader("✅ Execution Log")
    with col_hist2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.execution_log = []
            st.rerun()

    if st.session_state.execution_log:
        # Reverse to show newest first
        df_log = pd.DataFrame(st.session_state.execution_log[::-1])
        st.dataframe(df_log, use_container_width=True, hide_index=True)
    else:
        st.write("No jobs executed yet.")

with col2:
    st.subheader("📋 Pending Queue (Heap structure)")
    
    if st.session_state.priority_queue:
        # We shouldn't modify the actual heap for display to keep its structure intact.
        # We sort a copy to show the exact execution order for the user.
        queue_copy = list(st.session_state.priority_queue)
        queue_copy.sort() # Uses our custom __lt__ method
        
        df_queue = pd.DataFrame([job.to_dict() for job in queue_copy])
        st.dataframe(df_queue, use_container_width=True, hide_index=True)
        
        col_exec_1, col_exec_2 = st.columns(2)
        with col_exec_1:
            if st.button("🚀 Execute Next Job (Heap Pop)", use_container_width=True, type="primary"):
                if st.session_state.priority_queue:
                    # Pop the highest priority job from the heap
                    executed_job = heapq.heappop(st.session_state.priority_queue)
                    
                    # Log the execution
                    st.session_state.execution_log.append({
                        "Executed At": time.strftime('%H:%M:%S'),
                        "Priority": executed_job.priority,
                        "Job ID": executed_job.job_id,
                        "Name": executed_job.name,
                    })
                    st.rerun()
                    
        with col_exec_2:
            if st.button("⚡ Execute All Jobs", use_container_width=True):
                with st.spinner("Executing all pending jobs..."):
                    while st.session_state.priority_queue:
                        executed_job = heapq.heappop(st.session_state.priority_queue)
                        st.session_state.execution_log.append({
                            "Executed At": time.strftime('%H:%M:%S'),
                            "Priority": executed_job.priority,
                            "Job ID": executed_job.job_id,
                            "Name": executed_job.name,
                        })
                        time.sleep(0.3) # Delay to simulate work
                st.rerun()
    else:
        st.info("The priority queue is empty. Add jobs using the panel on the left.")
