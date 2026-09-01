# 🌊 Sonar Echo Sounder Simulator

> An interactive marine sonar simulation laboratory for modeling acoustic pulse transmission, seabed echoes, two-way travel time, and water-depth estimation using the echo-sounding principle.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green?logo=qt)
[![NumPy](https://img.shields.io/badge/Numerical-NumPy-orange?logo=numpy)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-orange?logo=matplotlib)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<img width="948" height="503" alt="image" src="https://github.com/user-attachments/assets/710b9f84-359a-4e13-8753-cd1c4b17a4d8" />


---

## 📌 Overview

**Sonar Echo Sounder Simulator** is an interactive desktop application for understanding the fundamental principles of **acoustic echo sounding and underwater depth measurement**.

The simulator models an acoustic pulse transmitted from a sonar transducer toward the seabed. The pulse travels through the water column, reflects from the seafloor, and returns to the receiver.

The measured **two-way travel time (TWTT)** is then used to estimate water depth.

This project provides a virtual laboratory for exploring:

* Echo sounding
* Sonar pulse transmission
* Seabed echoes
* Two-way travel time
* Water sound velocity
* Depth calculation
* Acoustic propagation
* Echo amplitude
* Noise
* Signal processing
* Hydrographic survey principles

---

# ✨ Key Features

## 📡 Acoustic Pulse Transmission

The simulator models an acoustic pulse transmitted from a sonar transducer toward the seabed.

```text id="s9w4kc"
                 SONAR
              TRANSDUCER
                  │
                  │
                  ▼
                  │
                  │ Acoustic Pulse
                  │
                  ▼
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
             WATER
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                  │
                  │
                  ▼
              SEABED
────────────────────────────────────
                  ▲
                  │
                  │ Echo
                  │
                  ▲
              TRANSDUCER
```

The returned echo provides the information required to estimate water depth.

---

# 🌊 Echo Sounding Principle

Echo sounding is based on measuring the time required for an acoustic pulse to travel from the transducer to the seabed and back.

```text id="m4c8zq"
Transducer
    │
    │ ↓ Transmitted Pulse
    │
    ▼
  Seabed
    │
    │ ↑ Reflected Echo
    │
    ▲
Transducer
```

The measured time is called **Two-Way Travel Time (TWTT)**.

---

# ⏱️ Two-Way Travel Time

For a simplified constant-velocity water column:

```text id="x7n3pa"
TWTT = 2d / v
```

where:

* `TWTT` = two-way travel time
* `d` = water depth
* `v` = speed of sound in water

Therefore:

```text id="q6r8yc"
d = v × TWTT / 2
```

The simulator demonstrates this fundamental relationship used in echo sounding.

---

# 📏 Water Depth Measurement

The basic measurement sequence is:

```text id="k5m2vx"
Transmit Acoustic Pulse
          │
          ▼
   Propagate Through Water
          │
          ▼
       Seabed
          │
          ▼
     Echo Reflection
          │
          ▼
      Echo Return
          │
          ▼
   Measure TWTT
          │
          ▼
   Calculate Depth
```

A longer travel time corresponds to a greater water depth when sound velocity is held constant.

---

# 🔊 Acoustic Wave Propagation

Sound travels through water at a finite velocity.

A simplified relationship is:

```text id="v8j4mq"
Distance = Velocity × Time
```

For echo sounding:

```text id="c5p9xz"
Depth = Velocity × TWTT / 2
```

The actual speed of sound in water varies with environmental conditions such as:

* Temperature
* Salinity
* Pressure
* Depth

The simulator provides a simplified environment for exploring the effect of acoustic velocity on depth calculations.

---

# 🌡️ Sound Velocity

Accurate depth estimation depends on an appropriate sound-speed value.

Conceptually:

```text id="u3k7bn"
Sound Speed
     ↓
Travel Time
     ↓
Calculated Depth
```

An incorrect sound-speed assumption can introduce depth errors.

This makes sound-velocity information an important component of hydrographic surveying.

---

# 📈 Echo Signal Visualization

The received acoustic signal can be represented as an echo waveform.

```text id="r6n2yc"
Amplitude
   │
   │   █
   │   █
   │   █
───┼───█────────────────────────█────► Time
                                 █
                                 █
                              Seabed
                               Echo
```

The position of the seabed echo corresponds to the acoustic travel time.

---

# 🎯 Seabed Echo

The seabed produces a reflected acoustic response.

```text id="p7c4mz"
              Transducer
                  │
                  │
                  ▼
                  │
                  │
                  ▼
                  │
────────────────────────────────
              SEABED
                  ▲
                  │
                  │
                  │
              Echo Return
```

The strength of the return can depend on factors such as:

* Seabed characteristics
* Acoustic incidence angle
* Acoustic frequency
* Signal level
* Water conditions
* Sediment properties

The simulator provides a simplified representation of these effects.

---

# 🪨 Seabed Representation

Different seabed surfaces can produce different acoustic responses.

Conceptually:

```text id="h4v8qs"
Hard Seabed
────────────────────────────
████████████████████████████


Soft Sediment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
████████████████████████████
```

Harder surfaces may produce stronger acoustic reflections, while softer sediments can produce different echo characteristics.

---

# 📉 Acoustic Attenuation

Acoustic energy decreases as it propagates through water.

A simplified propagation model can demonstrate:

```text id="n6k2wp"
Transmitted Pulse
██████████

        ↓

████████

        ↓

██████

        ↓

████
```

Signal loss can result from mechanisms such as:

* Absorption
* Scattering
* Geometric spreading
* Environmental conditions

---

# 📊 Signal-to-Noise Ratio

Real sonar systems operate in the presence of environmental and electronic noise.

A simplified SNR relationship is:

```text id="j8q5rx"
SNR = Signal Power / Noise Power
```

In decibels:

```text id="m2v7kc"
SNR(dB) = 10 log₁₀(Psignal / Pnoise)
```

Higher SNR generally improves the ability to distinguish a seabed echo from background noise.

---

# 🚤 Echo Sounding from a Survey Vessel

The simulator can be viewed conceptually as a sonar system mounted on a vessel:

```text id="f5c9xz"
              SURVEY VESSEL
        ______________________
       /                      \
______/________________________\____
                │
                │ Transducer
                ▼
                │
                │ Acoustic Pulse
                ▼
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                 WATER
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                  │
                  │
                  ▼
────────────────────────────────────
                 SEABED
```

As a vessel moves, repeated depth measurements can be collected to construct a bathymetric profile.

---

# 🗺️ From Echo Sounding to Bathymetry

A single measurement provides a depth estimate.

Repeated measurements provide a profile:

```text id="r3m7qp"
Depth
  │
  │       ●
  │     ●   ●
  │   ●       ●
  │ ●           ●
  │
  └──────────────────────────► Distance
             Survey Track
```

This forms the conceptual basis for hydrographic bathymetric surveying.

---

# 🔬 Echo Sounding Pipeline

```text id="q8v3mz"
┌───────────────────────────────┐
│       Survey Parameters       │
│                               │
│ Sound Speed                   │
│ Water Depth                   │
│ Pulse Parameters              │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Pulse Generation        │
│                               │
│       Acoustic Signal         │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Water Propagation        │
│                               │
│       Acoustic Path           │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        Seabed Reflection      │
│                               │
│        Echo Generation        │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        Echo Reception         │
│                               │
│          TWTT                 │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Depth Calculation       │
│                               │
│       d = vt / 2              │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        Bathymetric Data       │
│                               │
│       Depth / Position        │
└───────────────────────────────┘
```

---

# 🎛️ Configurable Parameters

The simulator provides a controlled environment for experimenting with acoustic survey parameters.

| Parameter           | Purpose                                  |
| ------------------- | ---------------------------------------- |
| **Water Depth**     | Defines the simulated seabed depth       |
| **Sound Velocity**  | Controls acoustic propagation speed      |
| **Frequency**       | Defines the acoustic operating frequency |
| **Pulse Amplitude** | Controls transmitted signal level        |
| **Pulse Width**     | Controls temporal characteristics        |
| **Attenuation**     | Simulates propagation loss               |
| **Noise**           | Introduces background signal variations  |
| **Sampling Rate**   | Controls digital signal representation   |

---

# 🧮 Mathematical Model

The simplified echo model can be represented as a delayed and attenuated acoustic pulse:

```text id="w5k8nc"
y(t) = A · x(t - τ)
```

where:

* `x(t)` = transmitted acoustic pulse
* `y(t)` = received seabed echo
* `A` = reflection and propagation scaling
* `τ` = two-way travel-time delay

The delay is related to depth:

```text id="e9r2vp"
τ = 2d / v
```

Therefore:

```text id="a3k6mz"
d = vτ / 2
```

---

# 🧪 Example Experiments

## Experiment 1 — Water Depth

Simulate different water depths:

```text id="x5n8cq"
5 m
10 m
25 m
50 m
100 m
```

Observe how the seabed echo shifts with increasing depth.

Expected relationship:

```text id="k7m4zr"
Depth ↑
  ↓
Travel Distance ↑
  ↓
TWTT ↑
```

---

## Experiment 2 — Sound Velocity

Keep depth constant and change the assumed sound velocity.

Observe how the calculated depth changes.

This demonstrates why sound-speed information is important for accurate echo sounding.

---

## Experiment 3 — Echo Amplitude

Change the simulated seabed reflection strength.

Compare:

```text id="v2c7xm"
Weak Seabed Return
       vs
Strong Seabed Return
```

Observe the effect on the received waveform.

---

## Experiment 4 — Acoustic Attenuation

Increase attenuation with depth.

Observe how the received seabed echo becomes weaker.

```text id="n4q8yc"
Depth ↑
   ↓
Propagation Loss ↑
   ↓
Echo Amplitude ↓
```

---

## Experiment 5 — Environmental Noise

Increase the noise level.

Observe the effect on seabed echo detection.

```text id="p6m3vz"
Low Noise
   ↓
Clear Seabed Echo


High Noise
   ↓
Reduced Echo Visibility
```

---

## Experiment 6 — Sampling Rate

Change the sampling rate and observe the effect on the digital representation of the echo.

This provides an introduction to the relationship between acoustic signals and digital signal acquisition.

---

# 🛥️ Hydrographic Survey Concept

Repeated echo-sounding measurements along a survey line can produce a bathymetric profile.

```text id="r7c4kx"
Vessel
  🚤
  ───────────────────────────►

       ↓    ↓    ↓    ↓
       │    │    │    │
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          WATER
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     \       /\       /
      \_____/  \_____/
           SEABED
```

Each measurement provides a depth estimate at a particular survey position.

---

# 🌊 Applications in Marine Technology

Echo sounding is relevant to:

### ⚓ Hydrographic Surveying

* Bathymetric mapping
* Depth measurement
* Navigation surveys
* Port surveys
* Channel surveys

### 🚢 Marine Engineering

* Vessel draft clearance
* Seabed assessment
* Marine infrastructure surveys

### 🏗️ Offshore Engineering

* Pipeline route surveys
* Cable route surveys
* Foundation site investigation
* Offshore construction support

### 🌊 Inland Waterways

* River depth surveys
* Reservoir mapping
* Lake bathymetry
* Sedimentation studies

---

# 🛰️ Integration with Survey Systems

A practical echo-sounding workflow can combine acoustic depth measurements with positioning data.

```text id="c8n5rz"
Sonar
  │
  ├── Echo Time
  │
  └── Depth
        │
        ▼
   Positioning System
        │
        ├── Latitude
        ├── Longitude
        └── Vessel Position
        │
        ▼
   Bathymetric Dataset
```

This forms the foundation of modern hydrographic data acquisition.

---

# 🎓 Educational Applications

This project can be used to demonstrate:

* Sonar Fundamentals
* Echo Sounding
* Acoustic Wave Propagation
* Two-Way Travel Time
* Water Depth Calculation
* Sound Velocity
* Seabed Reflection
* Acoustic Attenuation
* Signal-to-Noise Ratio
* Hydrographic Surveying
* Bathymetry
* Marine Acoustic Systems
* Digital Signal Processing
* Sonar Signal Analysis

---

# 🛠️ Technology Stack

| Technology     | Purpose                                     |
| -------------- | ------------------------------------------- |
| **Python**     | Core simulation                             |
| **NumPy**      | Numerical computation and signal generation |
| **PyQt5**      | Desktop graphical interface                 |
| **Matplotlib** | Acoustic waveform visualization             |

---

# 🚀 Installation

### 1. Clone the repository

```bash id="q5v8mx"
git clone https://github.com/vishwakiran712/Sonar-Echo-Sounder-Simulator.git
cd Sonar-Echo-Sounder-Simulator
```

### 2. Install dependencies

```bash id="w8m3cz"
pip install numpy matplotlib PyQt5
```

### 3. Run the application

```bash id="y4k7qn"
python app.py
```

---

# 📂 Project Structure

```text id="h3v9xm"
Sonar-Echo-Sounder-Simulator/
│
├── app.py
├── README.md
└── LICENSE
```

---

# 🔭 Possible Future Enhancements

Potential extensions include:

* Multi-beam echo sounding
* Single-beam echo sounder simulation
* Variable seabed profiles
* Moving survey vessel
* Survey-line simulation
* Bathymetric profile generation
* Sound-speed profiles
* Temperature effects
* Salinity effects
* Depth-dependent sound velocity
* Seabed classification
* Multiple seabed layers
* Sub-bottom reflector simulation
* Beam-angle modeling
* Beam-width simulation
* Bottom-tracking algorithms
* Automatic echo detection
* Peak detection
* Signal filtering
* Matched filtering
* Gain control
* TVG simulation
* Real-time sonar display
* GPS/INS integration
* NMEA data simulation
* CSV survey-data export
* Bathymetric grid generation
* 2D bathymetry visualization
* 3D seabed visualization
* Real sonar hardware integration

---

# ⚠️ Simulation Notice

This application is intended for **education, experimentation, and marine acoustic/hydrographic research**.

It is a simplified simulation and does not replace calibrated echo sounders, hydrographic survey equipment, sound-velocity measurements, positioning systems, approved survey procedures, or qualified hydrographic personnel.

Real-world sonar measurements are affected by sound-speed profiles, temperature, salinity, pressure, transducer characteristics, beam geometry, vessel motion, draft, tide, heave, pitch, roll, seabed characteristics, multipath, and environmental noise.

---

# 📜 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

# 👨‍💻 Author

**Vishwakiran B.V.S.**

Engineering • Sports Technology • Product Research • Marine Robotics • NDT • Hydrography • Acoustics • Signal Processing

GitHub: [@vishwakiran712](https://github.com/vishwakiran712)

---

# ⭐ Project

If you find this project useful for learning, marine acoustics, hydrographic surveying, bathymetry, or sonar signal processing, consider giving the repository a ⭐.

**Repository:**
https://github.com/vishwakiran712/Sonar-Echo-Sounder-Simulator
