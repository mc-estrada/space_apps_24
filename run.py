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

    # Load planet data from the CSV file
    planet_data = pd.read_csv('planets.csv')

    # Constants
    AU_to_km = 149597870.7  # 1 AU in km

    # Prepare Plotly figure
    fig = go.Figure()

    # Add the Sun at the center with a smaller size
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(size=3, color='yellow'),  # Smaller size for the Sun
        name='Sun'
    ))

    # Add planets based on planet_data
    for _, row in planet_data.iterrows():
        a = row['a (AU)']
        diameter = row['diameter (km)']
        color = 'orange'  # Default color, can vary by planet

        # Set color based on planet name
        if row['full_name'] == 'Mercury':
            color = 'gray'
        elif row['full_name'] == 'Venus':
            color = 'orange'
        elif row['full_name'] == 'Earth':
            color = 'green'
        elif row['full_name'] == 'Mars':
            color = 'red'

        # Generate circular orbit path
        theta = np.linspace(0, 2 * np.pi, 100)
        r = a * AU_to_km  # Convert to km

        # Calculate x, y, z using orbital inclination
        i = row['i']  # Inclination in degrees
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = r * np.sin(np.radians(i)) * np.ones_like(x)  # Inclination effect

        # Plot the planet orbit
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color=color, width=2),  # Thinner lines for orbits
            name=row['full_name']
        ))

        # Plot the planet as a smaller dot on its orbit
        fig.add_trace(go.Scatter3d(
            x=[r], y=[0], z=[r * np.sin(np.radians(i))],  # Adjust for inclination
            mode='markers',
            marker=dict(size=5, color=color),  # Smaller size for planets
            name=row['full_name'] + ' (Diameter: ' + str(diameter) + ' km)'
        ))

    # Add NEOs
    for index, row in neo_data.iterrows():
        if row['pha'] == 'Y':  # Only plot hazardous NEOs
            a = row['a'] * AU_to_km
            e = row['e']
            i = row['i']
            ma = row['ma']
            num_points = 100
            true_anomalies = np.linspace(0, 360, num_points)

            # True anomaly calculation
            M = np.radians(ma)  # Mean anomaly in radians
            E = M  # Start with E = M
            for _ in range(10):  # Iterate to solve Kepler's equation
                E = M + e * np.sin(E)

            true_anomaly = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
            r = a * (1 - e * np.cos(E))  # Radius at true anomaly

            # Convert to Cartesian coordinates
            x = r * np.cos(true_anomaly)
            y = r * np.sin(true_anomaly)
            z = x * np.sin(np.radians(i))  # Inclination for NEOs

            # Plot NEO as a smaller point
            fig.add_trace(go.Scatter3d(
                x=[x], y=[y], z=[z],
                mode='markers',
                marker=dict(size=3, color='blue'),  # Smaller size for NEOs
                name=row['full_name']
            ))

    # Update layout for better visibility
    fig.update_layout(
        title='Near Earth Objects and Planets',
        scene=dict(
            xaxis=dict(showbackground=False),
            yaxis=dict(showbackground=False),
            zaxis=dict(showbackground=False),
            aspectmode='data'
        ),
        showlegend=True
    )

    # Generate HTML div for the plot
    plot_div = pyo.plot(fig, include_plotlyjs=False, output_type='div')

    return render_template('index.html', plot_div=plot_div)

if __name__ == '__main__':
    app.run(debug=True)
