import streamlit as st
import simpy
from simulation import DistributedSystem
from deadlock_detection import detect_deadlock
import networkx as nx
import matplotlib.pyplot as plt

st.title("Distributed Deadlock Detection Simulation")

num_sites = st.slider("Number of Sites", 1, 5, 2)
processes_per_site = st.slider("Processes per Site", 1, 5, 2)
sim_time = st.slider("Simulation Time", 5, 50, 20)

if st.button("Run Simulation"):
    env = simpy.Environment()
    system = DistributedSystem(env, num_sites, processes_per_site)

    for i in system.wait_for_graph.keys():
        env.process(system.process(i))

    env.run(until=sim_time)

    st.subheader("Wait-For Graph")
    st.write(system.wait_for_graph)

    # Visualization
    G = nx.DiGraph()
    for p, deps in system.wait_for_graph.items():
        for d in deps:
            G.add_edge(p, d)

    fig, ax = plt.subplots()
    nx.draw(G, with_labels=True, node_color='lightblue', ax=ax)
    st.pyplot(fig)

    # Deadlock Detection
    cycle = detect_deadlock(system.wait_for_graph)

    if cycle:
        st.error(f"Deadlock Detected: {' → '.join(cycle)}")
    else:
        st.success("No Deadlock Detected")