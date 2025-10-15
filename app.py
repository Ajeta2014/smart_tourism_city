
import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Smart Tourism City 3D", layout="wide")
st.title("🏙️ Smart Tourism City 3D – Urbana + Turística")

fig = go.Figure()

# ------------------------------
# Função para adicionar prédios detalhados
# ------------------------------
def add_building(x, y, width, depth, height, color='lightgray', window_color='yellow'):
    # Corpo do prédio
    X = [x, x+width, x+width, x, x, x+width, x+width, x]
    Y = [y, y, y+depth, y+depth, y, y, y+depth, y+depth]
    Z = [0,0,0,0,height,height,height,height]
    fig.add_trace(go.Mesh3d(x=X, y=Y, z=Z, color=color, opacity=0.9))

    # Janelas (simples faixas horizontais)
    n_floors = int(height/5)
    for f in range(n_floors):
        fig.add_trace(go.Mesh3d(
            x=[x+1, x+width-1, x+width-1, x+1, x+1, x+width-1, x+width-1, x+1],
            y=[y+1, y+1, y+depth-1, y+depth-1, y+1, y+1, y+depth-1, y+depth-1],
            z=[f*5+1, f*5+1, f*5+1, f*5+1, f*5+4, f*5+4, f*5+4, f*5+4],
            color=window_color,
            opacity=0.6
        ))

# ------------------------------
# Função para adicionar casas com telhados
# ------------------------------
def add_house(x, y, width, depth, height, roof_height, wall_color='beige', roof_color='brown', window_color='yellow'):
    # Corpo da casa
    X = [x, x+width, x+width, x, x, x+width, x+width, x]
    Y = [y, y, y+depth, y+depth, y, y, y+depth, y+depth]
    Z = [0,0,0,0,height,height,height,height]
    fig.add_trace(go.Mesh3d(x=X, y=Y, z=Z, color=wall_color, opacity=0.9))

    # Telhado pirâmide
    roof_X = [x, x+width, x+width/2]
    roof_Y = [y, y, y+depth/2]
    roof_Z = [height, height, height+roof_height]
    fig.add_trace(go.Mesh3d(x=roof_X, y=roof_Y, z=roof_Z, color=roof_color, opacity=1.0))

    # Janelas
    fig.add_trace(go.Mesh3d(
        x=[x+1, x+width-1, x+width-1, x+1, x+1, x+width-1, x+width-1, x+1],
        y=[y+1, y+1, y+depth-1, y+depth-1, y+1, y+1, y+depth-1, y+depth-1],
        z=[height/3, height/3, height/3, height/3, 2*height/3, 2*height/3, 2*height/3, 2*height/3],
        color=window_color,
        opacity=0.6
    ))

# ------------------------------
# Função para adicionar árvores estilizadas
# ------------------------------
def add_tree(x, y, trunk_height=3, leaf_height=5):
    fig.add_trace(go.Cone(
        x=[x], y=[y], z=[trunk_height],
        u=[0], v=[0], w=[leaf_height],
        sizemode="absolute", sizeref=2,
        anchor="tip",
        colorscale=[[0, 'green'], [1, 'green']],
        showscale=False
    ))

# ------------------------------
# Gerar a cidade urbana + turística
# ------------------------------
np.random.seed(42)
cols, rows = 12, 10
spacing_x, spacing_y = 30, 25

for i in range(cols):
    for j in range(rows):
        x = i*spacing_x - (cols*spacing_x)/2
        y = j*spacing_y - (rows*spacing_y)/2
        if np.random.rand() < 0.3:
            add_house(x, y, 12, 12, 8+np.random.rand()*5, 5)
        else:
            add_building(x, y, 15, 15, 20+np.random.rand()*40)

# ------------------------------
# Adicionar praia costeira
# ------------------------------
fig.add_trace(go.Mesh3d(
    x=[-200, 200, 200, -200],
    y=[150, 150, 230, 230],
    z=[0,0,0,0],
    color='deepskyblue',
    opacity=0.8
))

# Árvores na praia
for i in range(-180, 181, 20):
    add_tree(i, 190)

# ------------------------------
# Layout final
# ------------------------------
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        aspectmode='manual',
        aspectratio=dict(x=2, y=2, z=1)
    ),
    margin=dict(l=0,r=0,b=0,t=0)
)

st.plotly_chart(fig, use_container_width=True)
