import sys
import csv
import numpy as np
from scipy import signal as sp_signal

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QDoubleSpinBox, QGroupBox,
    QFrame, QSplitter, QScrollArea, QPushButton, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# -------------------------------------------------------------------------
# UI Styling (Dark Hydrographic Theme)
# -------------------------------------------------------------------------
DARK_STYLE = """
QMainWindow {
    background-color: #090D11;
}
QWidget {
    color: #C9D1D9;
    font-family: "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 11px;
}
QGroupBox {
    border: 1px solid #1F2937;
    border-radius: 6px;
    margin-top: 10px;
    font-weight: bold;
    color: #38BDF8;
    background-color: #111827;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 8px;
    background-color: #111827;
    border-radius: 3px;
}
QLabel {
    color: #9CA3AF;
}
QDoubleSpinBox {
    background-color: #090D11;
    border: 1px solid #374151;
    border-radius: 4px;
    padding: 4px 6px;
    color: #38BDF8;
    font-weight: bold;
}
QDoubleSpinBox:focus {
    border: 1px solid #38BDF8;
}
QPushButton {
    background-color: #1F2937;
    color: #38BDF8;
    border: 1px solid #374151;
    border-radius: 4px;
    padding: 6px 12px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #374151;
    border-color: #38BDF8;
}
QPushButton:pressed {
    background-color: #0284C7;
    color: #FFFFFF;
}
QFrame#metricCard {
    background-color: #090D11;
    border: 1px solid #1F2937;
    border-radius: 6px;
}
"""


class SonarEchoSounderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sonar Echo Sounder Simulator (Bathymetric Profiler)")
        self.resize(1450, 920)
        self.setMinimumSize(1024, 720)

        # Stored data for export
        self.bathymetry_positions = []
        self.bathymetry_measured_depths = []

        self.init_ui()
        self.recalculate()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # -----------------------------------------------------------------
        # LEFT PANEL: Parameters & Controls
        # -----------------------------------------------------------------
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        scroll_content = QWidget()
        ctrl_layout = QVBoxLayout(scroll_content)

        # 1. Hydrographic & Vessel Configuration
        group_vessel = QGroupBox("1. VESSEL & ENVIRONMENT CONFIG")
        grid_v = QGridLayout(group_vessel)
        grid_v.setSpacing(6)

        grid_v.addWidget(QLabel("Base Water Depth (m):"), 0, 0)
        self.spin_base_depth = self.create_spinbox(5.0, 200.0, 40.0, grid_v, 0, 1, step=5.0)

        grid_v.addWidget(QLabel("Sound Velocity (m/s):"), 1, 0)
        self.spin_velocity = self.create_spinbox(1400.0, 1600.0, 1500.0, grid_v, 1, 1, step=5.0)

        grid_v.addWidget(QLabel("Boat Speed (knots):"), 2, 0)
        self.spin_boat_speed = self.create_spinbox(1.0, 25.0, 6.0, grid_v, 2, 1, step=0.5)

        grid_v.addWidget(QLabel("Pulse Rate (Hz/Ping):"), 3, 0)
        self.spin_pulse_rate = self.create_spinbox(0.5, 10.0, 2.0, grid_v, 3, 1, step=0.5)

        ctrl_layout.addWidget(group_vessel)

        # 2. Transducer & Seabed Characteristics
        group_sonar = QGroupBox("2. ACOUSTIC & SEABED CHARACTERISTICS")
        grid_s = QGridLayout(group_sonar)
        grid_s.setSpacing(6)

        grid_s.addWidget(QLabel("Transducer Freq (kHz):"), 0, 0)
        self.spin_freq = self.create_spinbox(10.0, 200.0, 50.0, grid_s, 0, 1, step=5.0)

        grid_s.addWidget(QLabel("Seabed Roughness (m):"), 1, 0)
        self.spin_roughness = self.create_spinbox(0.0, 5.0, 0.4, grid_s, 1, 1, step=0.1)

        grid_s.addWidget(QLabel("Acoustic Noise (V):"), 2, 0)
        self.spin_noise = self.create_spinbox(0.0, 0.5, 0.04, grid_s, 2, 1, step=0.01)

        ctrl_layout.addWidget(group_sonar)

        # 3. Data Export Action
        group_export = QGroupBox("3. DATA EXPORT")
        vbox_exp = QVBoxLayout(group_export)

        btn_export = QPushButton("Export Bathymetry to CSV")
        btn_export.clicked.connect(self.export_csv)
        vbox_exp.addWidget(btn_export)

        ctrl_layout.addWidget(group_export)
        ctrl_layout.addStretch()

        scroll.setWidget(scroll_content)
        left_layout.addWidget(scroll)

        # Connect input signals
        for spin in [self.spin_base_depth, self.spin_velocity, self.spin_boat_speed,
                     self.spin_pulse_rate, self.spin_freq, self.spin_roughness, self.spin_noise]:
            spin.valueChanged.connect(self.recalculate)

        # -----------------------------------------------------------------
        # RIGHT PANEL: Hydrographic Metrics & Visualizations
        # -----------------------------------------------------------------
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Metric Readout Cards
        metrics_group = QGroupBox("SONAR HYDROGRAPHIC READOUTS")
        grid_metrics = QGridLayout(metrics_group)
        grid_metrics.setSpacing(6)

        self.lbl_total_pings = self.create_metric_card("Total Pings Sampled", "0", grid_metrics, 0, 0)
        self.lbl_ping_tof = self.create_metric_card("Latest Seabed ToF", "0.00 ms", grid_metrics, 0, 1)
        self.lbl_current_depth = self.create_metric_card("Measured Current Depth", "0.00 m", grid_metrics, 0, 2)
        self.lbl_min_depth = self.create_metric_card("Min Track Depth", "0.00 m", grid_metrics, 1, 0)
        self.lbl_max_depth = self.create_metric_card("Max Track Depth", "0.00 m", grid_metrics, 1, 1)
        self.lbl_mean_err = self.create_metric_card("RMS Depth Error", "0.00 m", grid_metrics, 1, 2)

        right_layout.addWidget(metrics_group)

        # Matplotlib Display Group (Echo Signal, ToF History, Bathymetry Profile)
        plots_group = QGroupBox("ECHO SOUNDER SCOPE & RECONSTRUCTED BATHYMETRIC PROFILE")
        layout_plots = QVBoxLayout(plots_group)

        self.fig = Figure(figsize=(9, 7), facecolor='#05080A')
        self.canvas = FigureCanvas(self.fig)
        layout_plots.addWidget(self.canvas)

        right_layout.addWidget(plots_group, stretch=1)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([360, 1090])

    def create_spinbox(self, min_val, max_val, val, layout, row, col, step=0.1):
        spin = QDoubleSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(val)
        spin.setSingleStep(step)
        layout.addWidget(spin, row, col)
        return spin

    def create_metric_card(self, title, default_val, layout, row, col):
        card = QFrame()
        card.setObjectName("metricCard")
        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(6, 4, 6, 4)

        lbl_title = QLabel(title.upper())
        lbl_title.setStyleSheet("color: #9CA3AF; font-size: 10px; font-weight: bold;")
        lbl_val = QLabel(default_val)
        lbl_val.setStyleSheet("color: #38BDF8; font-size: 12px; font-weight: bold;")

        vbox.addWidget(lbl_title)
        vbox.addWidget(lbl_val)
        layout.addWidget(card, row, col)
        return lbl_val

    def generate_seabed_topography(self, positions):
        base_d = self.spin_base_depth.value()
        roughness = self.spin_roughness.value()

        # Synthetic seabed feature components:
        # 1. Flat Region (0 - 150 m)
        # 2. Sloping Seabed (150 - 450 m)
        # 3. Sandbank (450 - 650 m)
        # 4. Depression / Trench (650 - 850 m)
        # 5. Artificial Object / Shipwreck (850 - 1000 m)

        true_depths = []
        np.random.seed(101)

        for x in positions:
            d = base_d

            # Sloping seabed section
            if 150.0 <= x <= 450.0:
                d += (x - 150.0) * 0.08  # 8% slope down

            # Sandbank (Gaussian elevation hill)
            elif 450.0 < x <= 650.0:
                d += 24.0 - 12.0 * np.exp(-0.5 * ((x - 550.0) / 35.0) ** 2)

            # Trench / Depression (Gaussian dip)
            elif 650.0 < x <= 850.0:
                d += 24.0 + 15.0 * np.exp(-0.5 * ((x - 750.0) / 30.0) ** 2)

            # Artificial object (Sharp box structure)
            elif 850.0 < x <= 1000.0:
                d += 24.0
                if 910.0 <= x <= 935.0:
                    d -= 7.5  # 7.5m high artificial object on seabed

            else:
                d += 0.0

            # Add random seabed roughness texture
            if roughness > 0:
                d += np.random.normal(0, roughness * 0.3)

            true_depths.append(d)

        return np.array(true_depths)

    def recalculate(self):
        v_sound = self.spin_velocity.value()  # m/s
        speed_knots = self.spin_boat_speed.value()
        pulse_rate = self.spin_pulse_rate.value()  # Hz
        fc_khz = self.spin_freq.value()  # kHz
        noise_amp = self.spin_noise.value()

        # Convert boat speed (1 knot = 0.514444 m/s)
        v_boat_m_s = speed_knots * 0.514444

        # Track total vessel travel distance (fixed at 1000 meters for survey run)
        total_distance_m = 1000.0
        time_total_s = total_distance_m / max(0.1, v_boat_m_s)

        # Generate Ping sampling positions along survey track
        num_pings = int(np.clip(time_total_s * pulse_rate, 50, 400))
        ping_positions = np.linspace(0.0, total_distance_m, num_pings)
        ping_times = ping_positions / v_boat_m_s

        # Generate True Seabed Bathymetry
        true_depths = self.generate_seabed_topography(ping_positions)

        # Two-way Acoustic Travel Time calculation: ToF = 2 * depth / velocity
        true_tofs = (2.0 * true_depths) / v_sound  # seconds

        # Simulate Sonar Ping Measurement with Acoustic Noise
        np.random.seed(42)
        tof_noise = np.random.normal(0, (noise_amp * 0.002), len(true_tofs))
        measured_tofs = true_tofs + tof_noise

        # Calculated Seabed Depth formula: depth = velocity * ToF / 2
        measured_depths = (v_sound * measured_tofs) / 2.0

        # Store results for CSV export
        self.bathymetry_positions = ping_positions
        self.bathymetry_measured_depths = measured_depths

        # Compute Hydrographic Metrics
        latest_tof_ms = measured_tofs[-1] * 1000.0
        current_depth = measured_depths[-1]
        min_d = np.min(measured_depths)
        max_d = np.max(measured_depths)
        rms_err = np.sqrt(np.mean((measured_depths - true_depths) ** 2))

        # Update UI Metric Cards
        self.lbl_total_pings.setText(f"{num_pings}")
        self.lbl_ping_tof.setText(f"{latest_tof_ms:.2f} ms")
        self.lbl_current_depth.setText(f"{current_depth:.2f} m")
        self.lbl_min_depth.setText(f"{min_d:.2f} m")
        self.lbl_max_depth.setText(f"{max_d:.2f} m")
        self.lbl_mean_err.setText(f"{rms_err:.3f} m")

        # Synthesize Single Echo RF Oscilloscope Waveform for the central ping
        mid_idx = num_pings // 2
        mid_tof = measured_tofs[mid_idx]

        max_t_scope = max(0.1, mid_tof * 1.3)
        t_scope = np.linspace(0, max_t_scope, 1000)

        # Pulse Envelope
        fc = fc_khz * 1000.0
        dur = 0.002
        dt = t_scope - mid_tof
        pulse_env = np.exp(-0.5 * (dt / (dur / 3.0)) ** 2)
        echo_rf = pulse_env * np.cos(2 * np.pi * fc * dt)

        if noise_amp > 0:
            echo_rf += np.random.normal(0, noise_amp, len(t_scope))

        echo_env = np.abs(sp_signal.hilbert(echo_rf - np.mean(echo_rf)))

        self.plot_visuals(t_scope, echo_rf, echo_env, mid_tof, ping_positions, ping_times, measured_tofs, true_depths, measured_depths)

    def export_csv(self):
        if len(self.bathymetry_positions) == 0:
            QMessageBox.warning(self, "Export Error", "No bathymetric data available to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Export Bathymetry CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["position_m", "depth_m"])
                    for pos, depth in zip(self.bathymetry_positions, self.bathymetry_measured_depths):
                        writer.writerow([f"{pos:.3f}", f"{depth:.3f}"])

                QMessageBox.information(self, "Export Success", f"Bathymetric data successfully saved to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"An error occurred while writing the file:\n{str(e)}")

    def plot_visuals(self, t_scope, echo_rf, echo_env, mid_tof, positions, ping_times, measured_tofs, true_depths, measured_depths):
        self.fig.clear()

        # Hydrographic Theme Colors
        bg_color = '#05080A'
        grid_color = '#13231B'
        trace_green = '#00FF66'
        water_cyan = '#38BDF8'
        seabed_brown = '#D97706'
        noise_red = '#EF4444'

        # Create 3 Subplots Grid
        ax1 = self.fig.add_subplot(311)  # Single Acoustic Echo Oscilloscope Signal
        ax2 = self.fig.add_subplot(312)  # Depth vs Survey Time (ToF Tracking)
        ax3 = self.fig.add_subplot(313)  # Reconstructed 2D Bathymetric Seabed Profile

        for ax in [ax1, ax2, ax3]:
            ax.set_facecolor(bg_color)
            ax.tick_params(colors='#9CA3AF', labelsize=7)
            for spine in ax.spines.values():
                spine.set_color('#1F2937')

        # -----------------------------------------------------------------
        # 1. TOP SUBPLOT: Acoustic Return Echo Signal (Single Ping)
        # -----------------------------------------------------------------
        t_scope_ms = t_scope * 1000.0
        mid_tof_ms = mid_tof * 1000.0

        ax1.plot(t_scope_ms, echo_rf, color=water_cyan, linewidth=0.8, alpha=0.7, label="Acoustic Return RF Signal")
        ax1.plot(t_scope_ms, echo_env, color=trace_green, linewidth=1.1, label="Hilbert Envelope")
        ax1.scatter([mid_tof_ms], [np.max(echo_env)], color=noise_red, s=50, zorder=5, label=f"Detected Seabed Echo ({mid_tof_ms:.2f} ms)")

        ax1.set_title("TRANSDUCER ACOUSTIC RETURN ECHO WAVEFORM", color=water_cyan, fontsize=8, fontweight='bold', loc='left')
        ax1.set_xlabel("Time of Flight (ms)", color='#9CA3AF', fontsize=7)
        ax1.set_ylabel("Amplitude (V)", color='#9CA3AF', fontsize=7)
        ax1.grid(True, linestyle=':', linewidth=0.5, color=grid_color)
        ax1.legend(facecolor='#0B1217', edgecolor=grid_color, labelcolor='#C9D1D9', fontsize=6, loc='upper right')

        # -----------------------------------------------------------------
        # 2. MIDDLE SUBPLOT: Depth vs Time of Flight
        # -----------------------------------------------------------------
        ax2.plot(ping_times, measured_tofs * 1000.0, color='#A855F7', linewidth=1.2, marker='o', markersize=2, label="Two-Way Travel Time (ToF)")
        ax2.set_title("ACOUSTIC TRAVEL TIME (ToF) VS SURVEY RUN TIME", color='#A855F7', fontsize=8, fontweight='bold', loc='left')
        ax2.set_xlabel("Survey Duration (seconds)", color='#9CA3AF', fontsize=7)
        ax2.set_ylabel("ToF (ms)", color='#9CA3AF', fontsize=7)
        ax2.grid(True, linestyle=':', linewidth=0.5, color=grid_color)
        ax2.legend(facecolor='#0B1217', edgecolor=grid_color, labelcolor='#C9D1D9', fontsize=6, loc='upper right')

        # -----------------------------------------------------------------
        # 3. BOTTOM SUBPLOT: Reconstructed Seabed Bathymetry Profile
        # -----------------------------------------------------------------
        ax3.plot(positions, true_depths, color='#94A3B8', linestyle='--', linewidth=1.2, label="Actual Seabed Profile")
        ax3.plot(positions, measured_depths, color=water_cyan, linewidth=1.5, label="Sonar Measured Bathymetry")

        # Fill Water Column and Seabed Sediment
        ax3.fill_between(positions, 0, measured_depths, color='#0284C7', alpha=0.18, label="Water Column")
        ax3.fill_between(positions, measured_depths, np.max(measured_depths) + 10, color='#78350F', alpha=0.35, label="Seabed / Sub-bottom")

        # Invert Y-axis so depth goes downwards
        ax3.set_ylim(np.max(measured_depths) + 8, 0)
        ax3.set_xlim(0, positions[-1])

        ax3.set_title("RECONSTRUCTED 2D BATHYMETRIC CROSS-SECTION", color=trace_green, fontsize=8, fontweight='bold', loc='left')
        ax3.set_xlabel("Vessel Track Position (meters)", color='#9CA3AF', fontsize=7)
        ax3.set_ylabel("Depth (meters)", color='#9CA3AF', fontsize=7)
        ax3.grid(True, linestyle=':', linewidth=0.5, color=grid_color)
        ax3.legend(facecolor='#0B1217', edgecolor=grid_color, labelcolor='#C9D1D9', fontsize=6, loc='lower right')

        self.fig.tight_layout()
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(DARK_STYLE)

    window = SonarEchoSounderApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()