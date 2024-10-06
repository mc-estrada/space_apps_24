#Planets Database.csv
#full_name,T (years),e,a (AU),i,L (mean long.),varpi (long.peri),Om (Long. Ascend node),om (arg peri),diameter (km),Orbital Vel. (km/s)

#NEO PHA Database.csv
#neo,pha,full_name,diameter,orbit_id,epoch,e,a,q,i,w,per_y,om,ma,ad,n,moid,H,class,Notes,

#Near Earth Comet Database.csv
#full_name,neo,pha,H,G,M1,M2,epoch,e,a,q,i,om,w,ma,ad,n,per_y,moid


'''
// Orbital Parameters common across datasets
typedef struct
{
    double e;       // Eccentricity
    double a;       // Semi-major axis in AU
    double q;       // Perihelion distance in AU
    double i;       // Inclination in degrees
    double L;       // Mean longitude in degrees (planets only)
    double varpi;   // Longitude of periapsis (planets)
    double Om;      // Longitude of the ascending node
    double w;       // Argument of periapsis
    double ma;      // Mean anomaly
    double ad;      // Aphelion distance in AU
    double n;       // Mean motion (degrees/day)
    double per_y;   // Orbital period in years
    double moid;    // Minimum Orbit Intersection Distance (NEOs, comets)
    double epoch;   // Epoch (reference time for orbital elements)
} OrbitalParams;

// Physical Parameters (like diameter, velocity)
typedef struct
{
    double diameter;     // Diameter in km (for planets/NEOs)
    double orbital_vel;  // Orbital velocity in km/s (for planets)
} PhysicalParams;

// Extra Parameters for comets (e.g., brightness)
typedef struct
{
    double H;    // Absolute magnitude (comets, NEOs)
    double G;    // Slope parameter (comets, NEOs)
    double M1;   // Magnitude parameter 1 (comets)
    double M2;   // Magnitude parameter 2 (comets)
} CometParams;

// Main structure for Planets, NEOs, PHAs, and Comets
typedef struct
{
    char full_name[100];  // Object name
    int neo;              // 1 if Near Earth Object, 0 otherwise
    int pha;              // 1 if Potentially Hazardous Asteroid, 0 otherwise
    char orbit_id[50];    // Orbit ID (for NEOs)
    char classification[50]; // Classification (NEOs, comets)
    char notes[200];      // Notes on the object

    // Orbital parameters for the object
    OrbitalParams orbit;

    // Physical properties (diameter, velocity)
    PhysicalParams physical;

    // Specific parameters for comets (H, G, M1, M2)
    CometParams comet_params;

} SpaceObject;

'''

import csv
from typing import List

from dataclasses import dataclass
from typing import Optional

#common parameter
@dataclass
class OrbitalParams:
    e: Optional[float] = None  # Eccentricity
    a: Optional[float] = None  # Semi-major axis in AU
    q: Optional[float] = None  # Perihelion distance in AU
    i: Optional[float] = None  # Inclination in degrees
    L: Optional[float] = None  # Mean longitude in degrees (planets only)
    varpi: Optional[float] = None  # Longitude of periapsis (planets)
    Om: Optional[float] = None  # Longitude of the ascending node
    w: Optional[float] = None  # Argument of periapsis
    ma: Optional[float] = None  # Mean anomaly
    ad: Optional[float] = None  # Aphelion distance in AU
    n: Optional[float] = None  # Mean motion (degrees/day)
    per_y: Optional[float] = None  # Orbital period in years
    moid: Optional[float] = None  # Minimum Orbit Intersection Distance (NEOs, comets)
    epoch: Optional[float] = None  # Epoch (reference time for orbital elements)

@dataclass
class PhysicalParams:
    diameter: Optional[float] = None  # Diameter in km (for planets/NEOs)
    orbital_vel: Optional[float] = None  # Orbital velocity in km/s (for planets)

@dataclass
class CometParams:
    H: Optional[float] = None  # Absolute magnitude (comets, NEOs)
    G: Optional[float] = None  # Slope parameter (comets, NEOs)
    M1: Optional[float] = None  # Magnitude parameter 1 (comets)
    M2: Optional[float] = None  # Magnitude parameter 2 (comets)

@dataclass
class SpaceObject:
    full_name: str  # Object name
    neo: int = 0  # 1 if Near Earth Object, 0 otherwise
    pha: int = 0  # 1 if Potentially Hazardous Asteroid, 0 otherwise
    orbit_id: Optional[str] = None  # Orbit ID (for NEOs)
    classification: Optional[str] = None  # Classification (NEOs, comets)
    notes: Optional[str] = None  # Notes on the object

    orbit: OrbitalParams = OrbitalParams()
    physical: PhysicalParams = PhysicalParams()
    comet_params: CometParams = CometParams()




def read_planets_database(filename: str) -> List[SpaceObject]:
    space_objects = []
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            planet = SpaceObject(
                full_name=row.get('full_name', '').strip(),
                orbit=OrbitalParams(
                    e=float(row.get('e', 0)),
                    a=float(row.get('a (AU)', 0)),
                    i=float(row.get('i', 0)),
                    L=float(row.get('L (mean long.)', 0)),
                    varpi=float(row.get('varpi (long.peri)', 0)),
                    Om=float(row.get('Om (Long. Ascend node)', 0)),
                    w=float(row.get('om (arg peri)', 0)),
                    per_y=float(row.get('T (years)', 0))
                ),
                physical=PhysicalParams(
                    diameter=float(row.get('diameter (km)', 0)),
                    orbital_vel=float(row.get('Orbital Vel. (km/s)', 0))
                )
            )
            space_objects.append(planet)
    return space_objects

def read_neo_pha_database(filename: str) -> List[SpaceObject]:
    space_objects = []
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            neo = SpaceObject(
                full_name=row.get('full_name', '').strip(),
                neo=int(row.get('neo', 0)),
                pha=int(row.get('pha', 0)),
                orbit_id=row.get('orbit_id', '').strip(),
                classification=row.get('class', '').strip(),
                notes=row.get('Notes', '').strip(),
                orbit=OrbitalParams(
                    e=float(row.get('e', 0)),
                    a=float(row.get('a', 0)),
                    q=float(row.get('q', 0)),
                    i=float(row.get('i', 0)),
                    w=float(row.get('w', 0)),
                    Om=float(row.get('om', 0)),
                    ma=float(row.get('ma', 0)),
                    ad=float(row.get('ad', 0)),
                    n=float(row.get('n', 0)),
                    moid=float(row.get('moid', 0)),
                    per_y=float(row.get('per_y', 0)),
                    epoch=float(row.get('epoch', 0))
                ),
                physical=PhysicalParams(
                    diameter=float(row.get('diameter', 0))
                ),
                comet_params=CometParams(
                    H=float(row.get('H', 0))
                )
            )
            space_objects.append(neo)
    return space_objects

def read_near_earth_comet_database(filename: str) -> List[SpaceObject]:
    space_objects = []
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            comet = SpaceObject(
                full_name=row.get('full_name', '').strip(),
                neo=int(row.get('neo', 0)),
                pha=int(row.get('pha', 0)),
                classification=row.get('class', '').strip(),
                orbit=OrbitalParams(
                    e=float(row.get('e', 0)),
                    a=float(row.get('a', 0)),
                    q=float(row.get('q', 0)),
                    i=float(row.get('i', 0)),
                    Om=float(row.get('om', 0)),
                    w=float(row.get('w', 0)),
                    ma=float(row.get('ma', 0)),
                    ad=float(row.get('ad', 0)),
                    n=float(row.get('n', 0)),
                    moid=float(row.get('moid', 0)),
                    per_y=float(row.get('per_y', 0)),
                    epoch=float(row.get('epoch', 0))
                ),
                comet_params=CometParams(
                    H=float(row.get('H', 0)),
                    G=float(row.get('G', 0)),
                    M1=float(row.get('M1', 0)),
                    M2=float(row.get('M2', 0))
                )
            )
            space_objects.append(comet)
    return space_objects


def load_fieles():
    planets = read_planets_database('Planets Database.csv')
    neos = read_neo_pha_database('NEO PHA Database.csv')
    comets = read_near_earth_comet_database('Near Earth Comet Database.csv')
    return