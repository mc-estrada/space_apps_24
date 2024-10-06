from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.offline as pyo

app = Flask(__name__)

@app.route('/')
def index():
    # Load NEOs from the CSV file
    neo_data = pd.read_csv('NEO.csv')

    # Load NECs (Comets) from the CSV file
    nec_data = pd.read_csv('NEC.csv')

    # Load planet data from the CSV file
    planet_data = pd.read_csv('planets.csv')

    # Constants
    AU_to_km = 149597870.7  # 1 AU in km

    # Prepare Plotly figure
    fig = go.Figure()

    # Add the Sun at the center
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(size=10, color='yellow'),
        name='Sun'
    ))

    # Add planets based on planet_data
    for _, row in planet_data.iterrows():
        a = row['a (AU)']
        diameter = row['diameter (km)']
        color = 'orange'  # Default color

        # Set color based on planet name
        if row['full_name'] == 'Mercury':
            color = 'gray'
        elif row['full_name'] == 'Venus':
            color = 'orange'
        elif row['full_name'] == 'Earth':
            color = 'blue'
        elif row['full_name'] == 'Mars':
            color = 'red'

        # Generate circular orbit path
        theta = np.linspace(0, 2 * np.pi, 100)
        r = a * AU_to_km  # Convert to km

        # Calculate x, y, z using orbital inclination
        i = row['i']  # Inclination in degrees
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = np.zeros_like(x)  # Start with z=0

        # Rotate the orbit for proper inclination (around x-axis)
        z_rotated = z * np.cos(np.radians(i)) - y * np.sin(np.radians(i))
        y_rotated = y * np.cos(np.radians(i)) + z * np.sin(np.radians(i))

        # Plot the planet orbit
        fig.add_trace(go.Scatter3d(
            x=x, y=y_rotated, z=z_rotated,
            mode='lines',
            line=dict(color=color, width=2),
            name=row['full_name']
        ))

        # Plot the planet itself as a dot on its orbit
        fig.add_trace(go.Scatter3d(
            x=[x[0]], y=[y_rotated[0]], z=[z_rotated[0]],
            mode='markers',
            marker=dict(size=3, color=color, opacity=0.8),
            name=row['full_name'] + ' (Diameter: ' + str(diameter) + ' km)'
        ))

    # Add NEOs
    for index, row in neo_data.iterrows():
        if row['pha'] == 'Y':  # Only plot hazardous NEOs
            a = row['a'] * AU_to_km
            e = row['e']
            i = row['i']
            ma = row['ma']

            # Calculate radius and true anomaly
            num_points = 100
            true_anomalies = np.linspace(0, 360, num_points)

            M = np.radians(ma)  # Mean anomaly in radians
            E = M  # Start with E = M
            for _ in range(10):  # Iterate to solve Kepler's equation
                E = M + e * np.sin(E)

            true_anomaly = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
            r = a * (1 - e * np.cos(E))  # Radius at true anomaly

            # Convert to Cartesian coordinates
            x = r * np.cos(true_anomaly)
            y = r * np.sin(true_anomaly)

            # Apply orbital inclination
            z = r * np.sin(np.radians(i))  # Inclination for NEOs

            # Rotate the orbit for proper inclination
            z_rotated = z * np.cos(np.radians(i)) - y * np.sin(np.radians(i))
            y_rotated = y * np.cos(np.radians(i)) + z * np.sin(np.radians(i))

            # Plot NEO as a point
            fig.add_trace(go.Scatter3d(
                x=[x], y=[y_rotated], z=[z_rotated],
                mode='markers',
                marker=dict(size=1.5, color='blue', opacity=0.7),
                name=row['full_name']
            ))

    # Add NECs (comets)
    for index, row in nec_data.iterrows():
        a = row['a'] * AU_to_km
        e = row['e']
        i = row['i']
        ma = row['ma']

        # Calculate radius and true anomaly
        num_points = 100
        true_anomalies = np.linspace(0, 360, num_points)

        M = np.radians(ma)  # Mean anomaly in radians
        E = M  # Start with E = M
        for _ in range(10):  # Iterate to solve Kepler's equation
            E = M + e * np.sin(E)

        true_anomaly = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
        r = a * (1 - e * np.cos(E))  # Radius at true anomaly

        # Convert to Cartesian coordinates
        x = r * np.cos(true_anomaly)
        y = r * np.sin(true_anomaly)

        # Apply orbital inclination
        z = r * np.sin(np.radians(i))  # Inclination for NECs

        # Rotate the orbit for proper inclination
        z_rotated = z * np.cos(np.radians(i)) - y * np.sin(np.radians(i))
        y_rotated = y * np.cos(np.radians(i)) + z * np.sin(np.radians(i))

        # Plot NEC as a point
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y_rotated], z=[z_rotated],
            mode='markers',
            marker=dict(size=1.5, color='green', opacity=0.7),
            name=row['full_name']
        ))

    # Update layout for better visibility and a space-like effect
    fig.update_layout(
        height=800,
        width=1400,
        title='3D Visualization of NEOs, NECs, and Planets',
        scene=dict(
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=False,
                backgroundcolor='black',
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=False,
                backgroundcolor='black',
            ),
            zaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=False,
                backgroundcolor='black',
            ),
            aspectmode='data',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5),
            )
        ),
        paper_bgcolor='black',
        plot_bgcolor='black',
        font=dict(color='white'),
        showlegend=True
    )

    # Generate HTML div for the plot
    plot_div = pyo.plot(fig, include_plotlyjs=False, output_type='div')

    return render_template('index.html', plot_div=plot_div)

if __name__ == '__main__':
    app.run(debug=True)
