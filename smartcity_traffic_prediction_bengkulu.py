import osmnx as ox
import networkx as nx
from geopy.distance import geodesic
import folium
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import pickle
import os
from sklearn.tree import DecisionTreeClassifier
import numpy as np

# Konfigurasi optimasi
ox.settings.log_console = False
ox.settings.use_cache = True

# File cache untuk graf
GRAPH_CACHE_FILE = "bengkulu_graph.pkl"

# Fungsi untuk load/save graf dengan cache
def load_or_create_graph():
    if os.path.exists(GRAPH_CACHE_FILE):
        print("Loading cached graph...")
        with open(GRAPH_CACHE_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        print("Creating new graph... (This may take a while)")
        # Gunakan place name yang lebih stabil
        G = ox.graph_from_place(
            "Bengkulu, Bengkulu, Indonesia", 
            network_type='drive',
            simplify=True
        )
        
        # Simpan ke cache
        with open(GRAPH_CACHE_FILE, 'wb') as f:
            pickle.dump(G, f)
        print("Graph cached for future use.")
        return G

# Load graf dengan optimasi
G = load_or_create_graph()

# Daftar lokasi yang bisa dipilih sebagai start/end
locations = {
    "UNIB": {"lat": -3.759151679706669, "lon": 102.27244696570337},
    "SMA Negeri 1": {"lat": -3.7956820399891193, "lon": 102.26669585378794},
    "Mega Mall Bengkulu": {"lat": -3.7936951693487595, "lon": 102.26681161414268},
    "Kantor Gubernur": {"lat": -3.8209031712069805, "lon": 102.28394468112342},
    "Bencoolen Mall": {"lat": -3.81088901481175, "lon": 102.26820413774178},
    "Pantai Panjang": {"lat": -3.808250867494018, "lon": 102.26280196936469},
    "Rumah Sakit Umum Kota Bengkulu": {"lat": -3.796049609889266, "lon": 102.26842810624596},
    "Balai Buntar": {"lat": -3.821776176237121102, "lon": 102.29586},
    "Benteng Marlborough": {"lat": -3.787312290773892, "lon": 102.25166496763057},
    "Museum Bengkulu": {"lat": 3.8156828963327922, "lon": 102.28756307631366},
    "Wisata Pulau Tikus 3 putra Bengkulu": {"lat": 3.790154921884453, "lon": 102.2508977763127},
    "Pantai Tapak Paderi": {"lat": -3.7942787908531788, "lon": 102.24865179646642},
    "Kawasan Kota Tuo Pasar Bengkulu": {"lat": -3.772726707364913, "lon": 102.26336856763051},
    "Pantai Lentera Merah": {"lat": -3.898413728389778, "lon": 102.27885614451513},
    "Rumah Bekas Kediaman Bung Karno": {"lat": -3.7991187382445433, "lon": 102.26125360995908},
    "View Tower": {"lat": -3.7903047970540507, "lon": 102.25088704747691},
    "Tugu Pers Bengkulu": {"lat": -3.786646996179853, "lon": 102.25110620995892},
    "Monumen Tugu Thomas Parr": {"lat": -3.7887247015657706, "lon": 102.25068796763055},
}

# Titik keramaian dengan jam aktif yang realistis
poi_list = [
    {
        "nama": "Simpang Lima", 
        "lat": -3.7973364729275967, 
        "lon": 102.26598527496665, 
        "radius": 200, 
        "severity": "high",
        "jam_aktif": [
            {"start": 6, "end": 9, "level": "high"},     # Rush hour pagi
            {"start": 11, "end": 13, "level": "medium"}, # Siang hari
            {"start": 15, "end": 18, "level": "high"},   # Rush hour sore
            {"start": 19, "end": 21, "level": "medium"}  # Malam hari
        ],
        "tipe": "persimpangan"
    },
    {
        "nama": "SMA Negeri 1", 
        "lat": -3.7956820399891193, 
        "lon": 102.26669585378794, 
        "radius": 120, 
        "severity": "medium",
        "jam_aktif": [
            {"start": 6, "end":9, "level":"high"},
            {"start":15,"end":18,"level":"high"}
        ],
        "tipe": "sekolah"
    },
    {
        "nama": "SMA Negeri 6", 
        "lat": -3.7840403674703866, 
        "lon": 102.26305307580493, 
        "radius": 120, 
        "severity": "medium",
        "jam_aktif": [
            {"start": 6, "end":9, "level":"high"},
            {"start":15,"end":18,"level":"high"}
        ],
        "tipe": "sekolah"
    },
    {
        "nama": "SMA Muhammadiyah 1 Kota Bengkulu", 
        "lat": -3.7853123815287484, 
        "lon": 102.2638354022807,  
        "radius": 100, 
        "severity": "medium",
        "jam_aktif": [
            {"start": 6, "end":9, "level":"high"},
            {"start":15,"end":18,"level":"high"}
        ],
        "tipe": "sekolah"
    },
    {
        "nama": "Mega Mall Bengkulu", 
        "lat": -3.7936951693487595, 
        "lon": 102.26681161414268, 
        "radius": 180, 
        "severity": "high",
        "jam_aktif": [
            {"start": 10, "end": 12, "level": "medium"},
            {"start": 14, "end": 16, "level": "medium"},
            {"start": 18, "end": 22, "level": "high"}
        ],
        "tipe": "mall"
    },
    {
        "nama": "Kantor Gubernur", 
        "lat": -3.8209031712069805, 
        "lon": 102.28394468112342, 
        "radius": 150, 
        "severity": "medium",
        "jam_aktif": [
            {"start": 7, "end": 9, "level": "high"},
            {"start": 11, "end": 13, "level": "medium"},
            {"start": 15, "end": 17, "level": "high"}
        ],
        "tipe": "kantor"
    },{
        "nama": "Bencoolen Mall", 
        "lat": -3.81088901481175, 
        "lon": 102.26820413774178, 
        "radius": 140, 
        "severity": "medium",
        "jam_aktif": [
            {"start": 10, "end": 12, "level": "low"},
            {"start": 14, "end": 16, "level": "medium"},
            {"start": 18, "end": 22, "level": "high"}
        ],
        "tipe": "mall"
    },
    {"nama": "Pasar Panorama",
     "lat": -3.8158397939508877,
     "lon": 102.29992148065534,
     "radius": 200,
     "severity": "high",
     "jam_aktif": [
            {"start": 7, "end": 9, "level": "high"},
            {"start": 9, "end": 15, "level": "low"},
            {"start": 15, "end": 18, "level": "medium"}
    ],
    "tipe": "Pasar"
    },
    {"nama": "Universitas Bengkulu (UNIB)",
     "lat": -3.7594880278420986, 
     "lon": 102.27238753694245,
     "radius": 400,
     "severity": "high",
     "jam_aktif": [
            {"start": 7, "end": 9, "level": "high"},
            {"start": 9, "end": 15, "level": "low"},
            {"start": 15, "end": 18, "level": "medium"}
    ],
    "tipe": "Universitas"
    },
    {"nama": "Universitas Dehasen",
     "lat": -3.7939654793946107, 
     "lon": 102.27774866350157,
     "radius": 200,
     "severity": "high",
     "jam_aktif": [
            {"start": 7, "end": 9, "level": "high"},
            {"start": 9, "end": 15, "level": "low"},
            {"start": 15, "end": 18, "level": "medium"}
    ],
    "tipe": "Universitas"
    },
    {
        "nama": "SMAN 5 Bengkulu", 
        "lat": -3.794361990854101, 
        "lon": 102.27177613204843,  
        "radius": 100, 
        "severity": "medium",
        "jam_aktif": [
            {"start": 6, "end":9, "level":"high"},
            {"start":15,"end":18,"level":"high"}
        ],
        "tipe": "sekolah"
    },
    {
        "nama": "SMkN 1 Bengkulu", 
        "lat": -3.7960750470913123, 
        "lon": 102.27272593127405,  
        "radius": 100, 
        "severity": "medium",
        "jam_aktif": [
            {"start": 6, "end":9, "level":"high"},
            {"start":15,"end":18,"level":"high"}
        ],
        "tipe": "sekolah"
    },
]

# Cache untuk menyimpan node terdekat POI (optimasi)
poi_affected_edges = {}

def get_poi_activity_level(poi, jam):
    """Mendapatkan tingkat aktivitas POI berdasarkan jam"""
    for jadwal in poi.get("jam_aktif", []):
        if jadwal["start"] <= jam <= jadwal["end"]:
            return jadwal["level"]
    return "inactive"  # Tidak aktif jika di luar jam operasi

def get_severity_multiplier(base_severity, activity_level):
    """Menghitung multiplier berdasarkan severity dasar dan tingkat aktivitas"""
    base_multipliers = {"low": 1.2, "medium": 1.5, "high": 2.0}
    activity_multipliers = {
        "inactive": 0.8,  # Sangat rendah saat tidak aktif
        "low": 1.0,       # Normal
        "medium": 1.3,    # Sedang
        "high": 1.8       # Tinggi saat jam sibuk
    }
    
    base = base_multipliers.get(base_severity, 1.5)
    activity = activity_multipliers.get(activity_level, 1.0)
    
    return base * activity

def precompute_poi_edges():
    """Precompute edges yang terkena dampak POI untuk optimasi"""
    global poi_affected_edges
    if poi_affected_edges:  # Sudah di-cache
        return
    
    print("Precomputing POI affected edges...")
    for poi_idx, poi in enumerate(poi_list):
        affected_edges = []
        poi_coord = (poi['lat'], poi['lon'])
        
        for u, v, k, data in G.edges(keys=True, data=True):
            if 'length' not in data:
                continue
            
            midpoint_lat = (G.nodes[u]['y'] + G.nodes[v]['y']) / 2
            midpoint_lon = (G.nodes[u]['x'] + G.nodes[v]['x']) / 2
            
            dist = geodesic((midpoint_lat, midpoint_lon), poi_coord).meters
            if dist <= poi['radius']:
                affected_edges.append((u, v, k, data['length']))
        
        poi_affected_edges[poi_idx] = affected_edges
    print(f"Precomputed {len(poi_affected_edges)} POI zones.")

# Fungsi AI: mengubah bobot jalan berdasarkan kondisi
def apply_traffic_conditions(G_base, jam, cuaca, scenario="normal"):
    """
    Scenarios:
    - normal: kondisi standar
    - avoid_traffic: hindari kemacetan maksimal  
    - through_traffic: lewati area macet (simulasi rute terburuk)
    """
    G_copy = G_base.copy()
    
    # Faktor berdasarkan cuaca
    weather_multiplier = {"Cerah": 1.0, "Mendung": 1.1, "Hujan": 1.6}
    weather_factor = weather_multiplier.get(cuaca, 1.0)
    
    # Faktor berdasarkan jam
    if jam in range(6, 9) or jam in range(15, 18):  # Rush hour
        time_factor = 2.5
        traffic_status = "Rush Hour"
    elif jam in range(11, 13) or jam in range(18, 20):  # Busy
        time_factor = 1.8
        traffic_status = "Busy"
    elif jam in range(9, 11) or jam in range(13, 15):  # Medium
        time_factor = 1.3
        traffic_status = "Medium"
    else:  # Normal
        time_factor = 1.0
        traffic_status = "Normal"
    
    # Terapkan kondisi berdasarkan skenario
    scenario_multipliers = {
        "normal": 1.0,
        "avoid_traffic": 1.5,  # Hindari area macet lebih kuat
        "through_traffic": 0.7  # Paksa lewat area macet (simulasi rute buruk)
    }
    
    scenario_factor = scenario_multipliers.get(scenario, 1.0)
    affected_count = 0
    active_pois = []
    
    for poi_idx, affected_edges in poi_affected_edges.items():
        poi = poi_list[poi_idx]
        
        # Dapatkan tingkat aktivitas POI berdasarkan jam
        activity_level = get_poi_activity_level(poi, jam)
        
        # Hitung multiplier berdasarkan aktivitas
        poi_factor = get_severity_multiplier(poi.get("severity", "medium"), activity_level)
        
        # Simpan info POI aktif untuk analisis
        if activity_level != "inactive":
            active_pois.append({
                "nama": poi["nama"],
                "activity": activity_level,
                "tipe": poi.get("tipe", "unknown")
            })
        
        for u, v, k, original_length in affected_edges:
            if G_copy.has_edge(u, v):
                total_factor = time_factor * weather_factor * poi_factor * scenario_factor
                
                if scenario == "through_traffic":
                    # Untuk rute "terburuk", kurangi penalti (simulasi memaksa lewat)
                    total_factor = max(1.1, total_factor * 0.5)
                
                G_copy[u][v][k]['length'] = original_length * total_factor
                affected_count += 1
    
    return G_copy, traffic_status, affected_count, active_pois

# Fungsi untuk multiple rute dengan algoritma berbeda
def get_multiple_routes(G, start_node, end_node, jam, cuaca):
    routes = {}
    
    try:
        # 1. Rute Tercepat (tanpa pertimbangan kemacetan)
        routes['fastest'] = {
            'path': nx.shortest_path(G, start_node, end_node, weight='length'),
            'name': 'Rute Tercepat',
            'color': 'blue',
            'description': 'Rute terpendek tanpa pertimbangan kemacetan'
        }
        
        # 2. Rute Rekomendasi AI (hindari kemacetan)
        G_avoid, status1, count1, active_pois = apply_traffic_conditions(G, jam, cuaca, "avoid_traffic")
        routes['recommended'] = {
            'path': nx.shortest_path(G_avoid, start_node, end_node, weight='length'),
            'name': 'Rute Rekomendasi',
            'color': 'green',
            'description': f'Rute yang menghindari kemacetan ({status1})',
            'active_pois': active_pois
        }
        
        # 3. Rute Alternatif (simulasi lewat kemacetan)
        G_through, status2, count2, _ = apply_traffic_conditions(G, jam, cuaca, "through_traffic")
        alt_route = nx.shortest_path(G_through, start_node, end_node, weight='length')
        
        # Pastikan rute alternatif berbeda dari yang lain
        if alt_route != routes['fastest']['path'] and alt_route != routes['recommended']['path']:
            routes['alternative'] = {
                'path': alt_route,
                'name': 'Rute Alternatif',
                'color': 'red',
                'description': 'Rute yang melewati area kemacetan'
            }
        else:
            # Coba cari rute alternatif dengan menghapus beberapa edge utama
            try:
                G_alt = G.copy()
                main_edges = routes['fastest']['path']
                # Hapus beberapa edge dari rute utama untuk memaksa rute berbeda
                for i in range(min(3, len(main_edges)-1)):
                    u, v = main_edges[i], main_edges[i+1]
                    if G_alt.has_edge(u, v):
                        G_alt.remove_edge(u, v)
                
                alt_path = nx.shortest_path(G_alt, start_node, end_node, weight='length')
                routes['alternative'] = {
                    'path': alt_path,
                    'name': 'Rute Alternatif',
                    'color': 'red',
                    'description': 'Rute alternatif yang menghindari jalan utama'
                }
            except:
                pass
    
    except nx.NetworkXNoPath:
        messagebox.showerror("Error", "Tidak ada rute yang ditemukan antara lokasi tersebut!")
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"Error dalam pencarian rute: {str(e)}")
        return {}
    
    return routes

# Fungsi menghitung panjang rute (optimasi)
def calculate_route_stats(G, route_path, kendaraan='Motor'):
    if not route_path or len(route_path) < 2:
        return 0, 0
    
    # Kecepatan rata-rata berdasarkan kendaraan
    kecepatan_km_jam = 35 if kendaraan == 'Motor' else 25  # Motor lebih cepat menyusup
    
    total_length = 0
    total_time = 0  # Estimasi waktu dalam detik
    
    for i in range(len(route_path) - 1):
        u, v = route_path[i], route_path[i + 1]
        
        if G.has_edge(u, v):
            # Gunakan networkx untuk mendapatkan edge dengan weight terpendek
            try:
                # Method 1: Langsung dari edge data
                edge_data = G[u][v]
                edge_length = 0
                
                # Jika multi-edge (dictionary dengan key 0, 1, 2, etc)
                if isinstance(edge_data, dict) and len(edge_data) > 0:
                    # Ambil edge pertama atau yang memiliki length terpendek
                    if 0 in edge_data and 'length' in edge_data[0]:
                        edge_length = edge_data[0]['length']
                    else:
                        # Cari semua length yang tersedia
                        lengths = []
                        for key, data in edge_data.items():
                            if isinstance(data, dict) and 'length' in data:
                                lengths.append(data['length'])
                        if lengths:
                            edge_length = min(lengths)
                
                # Method 2: Fallback menggunakan networkx edge attributes
                if edge_length == 0:
                    try:
                        edge_length = nx.shortest_path_length(G, u, v, weight='length')
                    except:
                        pass
                
                # Method 3: Manual calculation using coordinates (fallback terakhir)
                if edge_length == 0:
                    try:
                        u_coord = (G.nodes[u]['y'], G.nodes[u]['x'])
                        v_coord = (G.nodes[v]['y'], G.nodes[v]['x'])
                        edge_length = geodesic(u_coord, v_coord).meters
                    except:
                        edge_length = 100  # Default 100 meter jika semua gagal
                
                # Hitung waktu berdasarkan panjang edge
                if edge_length > 0:
                    edge_time_hours = edge_length / 1000 / kecepatan_km_jam
                    edge_time_seconds = edge_time_hours * 3600
                    
                    total_length += edge_length
                    total_time += edge_time_seconds
                    
            except Exception as e:
                print(f"Error processing edge {u}-{v}: {e}")
                # Fallback: gunakan koordinat untuk estimasi
                try:
                    u_coord = (G.nodes[u]['y'], G.nodes[u]['x'])
                    v_coord = (G.nodes[v]['y'], G.nodes[v]['x'])
                    edge_length = geodesic(u_coord, v_coord).meters
                    
                    edge_time_hours = edge_length / 1000 / kecepatan_km_jam
                    edge_time_seconds = edge_time_hours * 3600
                    
                    total_length += edge_length
                    total_time += edge_time_seconds
                except:
                    print(f"Failed to calculate distance for edge {u}-{v}")
                    continue
    
    return total_length, total_time

# Peta folium dengan multiple rute
def create_route_map(routes_data, start_coords, end_coords, jam):
    if not routes_data:
        return
    
    m = folium.Map(location=start_coords, zoom_start=13)
    
    # Marker start dan end
    folium.Marker(start_coords, tooltip='🚩 Start', 
                 icon=folium.Icon(color='green', icon='play')).add_to(m)
    folium.Marker(end_coords, tooltip='🏁 End', 
                 icon=folium.Icon(color='red', icon='stop')).add_to(m)
    
    # Tambahkan POI markers dengan status aktivitas
    for poi in poi_list:
        activity_level = get_poi_activity_level(poi, jam)
        
        # Tentukan warna berdasarkan tingkat aktivitas
        if activity_level == "inactive":
            color = "gray"
            status_text = "Tidak Aktif"
        elif activity_level == "low":
            color = "yellow"
            status_text = "Aktivitas Rendah"
        elif activity_level == "medium":
            color = "orange"
            status_text = "Aktivitas Sedang"
        else:  # high
            color = "red"
            status_text = "Aktivitas Tinggi"
        
        # Buat jadwal string untuk popup
        jadwal_str = ""
        for jadwal in poi.get("jam_aktif", []):
            jadwal_str += f"{jadwal['start']:02d}:00-{jadwal['end']:02d}:00 ({jadwal['level'].title()})<br>"
        
        folium.CircleMarker(
            location=[poi['lat'], poi['lon']],
            radius=12 if activity_level != "inactive" else 6,
            popup=f"<b>{poi['nama']}</b><br>"
                  f"Tipe: {poi.get('tipe', 'unknown').title()}<br>"
                  f"Status Jam {jam}:00: <b>{status_text}</b><br>"
                  f"Jadwal Aktif:<br>{jadwal_str}"
                  f"Radius: {poi['radius']}m",
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.7 if activity_level != "inactive" else 0.3
        ).add_to(m)
        
        # Area dampak POI - hanya tampilkan jika aktif
        if activity_level != "inactive":
            folium.Circle(
                location=[poi['lat'], poi['lon']],
                radius=poi['radius'],
                color=color,
                fill=False,
                opacity=0.4,
                weight=2
            ).add_to(m)
    
    # Tambahkan setiap rute
    route_colors = ['blue', 'green', 'red', 'purple', 'orange']
    legend_items = []
    
    for idx, (route_key, route_info) in enumerate(routes_data.items()):
        route_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route_info['path']]
        color = route_info.get('color', route_colors[idx % len(route_colors)])
        
        folium.PolyLine(
            route_coords, 
            color=color, 
            weight=4, 
            opacity=0.8,
            tooltip=f"{route_info['name']}: {route_info['description']}"
        ).add_to(m)
        
        legend_items.append(f"<span style='color:{color};'>&#9632;</span> {route_info['name']}")
    
    # Legend yang diperbaiki
    legend_html = f"""
    <div style='position: fixed; bottom: 50px; left: 50px; width: 320px; 
                background-color: white; z-index:9999; font-size:12px;
                border:2px solid grey; padding: 10px; border-radius: 5px;'>
      <b>🗺️ Legenda Rute:</b><br>
      {'<br>'.join(legend_items)}<br><br>

      <b>🚦 Status Kemacetan POI (Jam {jam}:00):</b><br>
      🔴 Tinggi &nbsp; 🟠 Sedang<br>
      🟡 Rendah &nbsp; ⚫ Tidak Aktif<br>

      <br>
      <b>📍 Tipe Lokasi:</b><br>
      🏫 Sekolah: Sibuk pagi & sore<br>
      🛒 Mall: Sibuk sore & malam<br>
      🏢 Kantor: Sibuk jam kerja
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    file_name = "bengkulu_multiple_routes.html"
    m.save(file_name)
    webbrowser.open(file_name)

# Thread untuk processing (menghindari freeze UI)
def process_routes_thread():
    try:
        # Update status
        status_label.config(text="Memproses rute...", fg="blue")
        root.update()
        
        # Validasi input
        try:
            jam = int(jam_entry.get())
            if not 0 <= jam <= 23:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Salah", "Masukkan jam antara 0–23.")
            status_label.config(text="Input tidak valid", fg="red")
            return

        cuaca = cuaca_combo.get()
        start_location = start_combo.get()
        end_location = end_combo.get()
        kendaraan = kendaraan_combo.get()
        
        if not cuaca or not start_location or not end_location:
            messagebox.showwarning("Input Salah", "Lengkapi semua pilihan.")
            status_label.config(text="Input tidak lengkap", fg="red")
            return
        
        if start_location == end_location:
            messagebox.showwarning("Input Salah", "Lokasi start dan end harus berbeda.")
            status_label.config(text="Lokasi sama", fg="red")
            return

        # Precompute POI edges jika belum
        if not poi_affected_edges:
            status_label.config(text="Menganalisis titik kemacetan...", fg="blue")
            root.update()
            precompute_poi_edges()

        # Ambil koordinat
        start_coords = [locations[start_location]["lat"], locations[start_location]["lon"]]
        end_coords = [locations[end_location]["lat"], locations[end_location]["lon"]]
        
        # Cari node terdekat
        status_label.config(text="Mencari node terdekat...", fg="blue")
        root.update()
        
        start_node = ox.distance.nearest_nodes(G, X=start_coords[1], Y=start_coords[0])
        end_node = ox.distance.nearest_nodes(G, X=end_coords[1], Y=end_coords[0])

        # Dapatkan multiple rute
        status_label.config(text="Menghitung rute alternatif...", fg="blue")
        root.update()
        
        routes_data = get_multiple_routes(G, start_node, end_node, jam, cuaca)
        
        if not routes_data:
            status_label.config(text="Tidak ada rute ditemukan", fg="red")
            return

        # Analisis hasil dengan informasi POI aktif
        analysis = f"Rute: {start_location} → {end_location}\n"
        analysis += f"Jam: {jam}:00 | Cuaca: {cuaca}\n"
        analysis += "=" * 60 + "\n\n"

        # Tampilkan status POI saat ini
        analysis += "- STATUS TITIK KERAMAIAN:\n"
        for poi in poi_list:
            activity = get_poi_activity_level(poi, jam)
            status_emoji = {
                "inactive": "⚫", "low": "🟡", "medium": "🟠", "high": "🔴"
            }   
            status_text = {
                "inactive": "Tidak Aktif", "low": "Rendah", 
                "medium": "Sedang", "high": "Tinggi"
            }
            analysis += f"  {status_emoji.get(activity, '⚫')} {poi['nama']} ({poi.get('tipe', '').title()}): {status_text.get(activity, 'Unknown')}\n"
        analysis += "\n"

        for route_key, route_info in routes_data.items():
            length, time_est = calculate_route_stats(G, route_info['path'], kendaraan)
            time_minutes = int(time_est / 60)
            
            analysis += f"- {route_info['name']}:\n"
            analysis += f"  -Jarak: {length:.0f} meter\n"
            analysis += f"  -Estimasi: {time_minutes} menit\n"
            analysis += f"  -{route_info['description']}\n\n"

        # Rekomendasi yang lebih cerdas
        if len(routes_data) >= 2:
            fastest_length = calculate_route_stats(G, routes_data['fastest']['path'], kendaraan)[0]
            recommended_length = calculate_route_stats(G, routes_data['recommended']['path'], kendaraan)[0]
            
            # Hitung POI aktif yang berpengaruh
            active_pois = routes_data.get('recommended', {}).get('active_pois', [])
            high_activity_count = sum(1 for poi in active_pois if poi['activity'] == 'high')

            # Prediksi kemacetan Decision Tree
            pred_dt = predict_kemacetan_dt(jam, cuaca, len(active_pois))
            analysis += f"[AI Decision Tree] Prediksi kemacetan saat ini: {pred_dt}"

            analysis += "\nREKOMENDASI SISTEM:"
            if high_activity_count > 0:
                analysis += f" Terdapat {high_activity_count} titik kemacetan tinggi pada jam ini."
                analysis += " Gunakan Rute Rekomendasi untuk menghindari kemacetan.\n"
            elif recommended_length > fastest_length + 200:
                analysis += " Perbedaan rute tidak signifikan, pilih Rute Tercepat.\n"
            else:
                analysis += " Kondisi lalu lintas relatif lancar, semua rute dapat digunakan.\n"

            analysis += "\n" + "=" * 60 + "\n"
            analysis += "KESIMPULAN ANALISIS SISTEM AI:\n"
            analysis += "Dapat dilihat bahwa area rawan kemacetan seperti sekolah, pasar, dan kantor memiliki jam sibuk masing-masing. "
            analysis += f"Sistem mendeteksi {high_activity_count} titik dengan aktivitas tinggi. "
            analysis += f"Cuaca saat ini: {cuaca}, yang berpotensi memengaruhi visibilitas dan kecepatan kendaraan di jalan. "
            analysis += "Kondisi ini menunjukkan kemungkinan perlambatan atau antrean kendaraan di jalur utama yang menghubungkan titik-titik tersebut. "

            if cuaca == "Hujan":
                analysis += "Karena kondisi hujan, kemungkinan besar terjadi perlambatan arus kendaraan akibat jalanan licin dan genangan air. Disarankan untuk berhati-hati atau memilih rute alternatif. "

            analysis += "\n\nTerima kasih telah menggunakan sistem prediksi rute dan kemacetan ini. "
            analysis += "Semoga informasi ini membantu Anda merencanakan perjalanan dengan lebih baik.\n"

        
        # Update UI
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, analysis)
        
        # Buat peta
        status_label.config(text="Membuat peta...", fg="blue")
        root.update()
        
        create_route_map(routes_data, start_coords, end_coords, jam)
        
        status_label.config(text="Selesai! Peta telah dibuka.", fg="green")
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        status_label.config(text=error_msg, fg="red")
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# Fungsi utama (non-blocking)
def run_app():
    # Jalankan di thread terpisah untuk menghindari freeze
    thread = threading.Thread(target=process_routes_thread, daemon=True)
    thread.start()

# GUI Layout
root = tk.Tk()
root.title("Sistem Prediksi Rute & Kemacetan - Bengkulu")
root.geometry("700x700")
root.configure(bg='#f0f0f0')

# Header
header_frame = tk.Frame(root, bg='#2c3e50', height=60)
header_frame.pack(fill='x')
header_frame.pack_propagate(False)

tk.Label(header_frame, text="Traffic Route Prediction System", 
         font=("Arial", 16, "bold"), fg="white", bg='#2c3e50').pack(pady=15)

# Main content frame
main_frame = tk.Frame(root, bg='#f0f0f0')
main_frame.pack(fill='both', expand=True, padx=20, pady=10)

# Input section
input_frame = tk.LabelFrame(main_frame, text="📝 Pengaturan Rute", font=("Arial", 12, "bold"), 
                           bg='#f0f0f0', padx=10, pady=10)
input_frame.pack(fill='x', pady=(0, 10))

# Grid layout untuk input
for i in range(4):  
    input_frame.grid_columnconfigure(1, weight=1)

tk.Label(input_frame, text="Lokasi Awal:", bg='#f0f0f0', font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
start_combo = ttk.Combobox(input_frame, values=list(locations.keys()), width=25, font=("Arial", 10))
start_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

tk.Label(input_frame, text="Lokasi Tujuan:", bg='#f0f0f0', font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
end_combo = ttk.Combobox(input_frame, values=list(locations.keys()), width=25, font=("Arial", 10))
end_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

tk.Label(input_frame, text="Kendaraan:", bg='#f0f0f0', font=("Arial", 10)).grid(row=4, column=0, sticky="w", padx=5, pady=5)
kendaraan_combo = ttk.Combobox(input_frame, values=["Motor", "Mobil"], width=25, font=("Arial", 10))
kendaraan_combo.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

tk.Label(input_frame, text="Jam (0-23):", bg='#f0f0f0', font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
jam_entry = tk.Entry(input_frame, width=27, font=("Arial", 10))
jam_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

tk.Label(input_frame, text="Cuaca:", bg='#f0f0f0', font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=5, pady=5)
cuaca_combo = ttk.Combobox(input_frame, values=["Cerah", "Mendung", "Hujan"], width=25, font=("Arial", 10))
cuaca_combo.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

# Button
button_frame = tk.Frame(main_frame, bg='#f0f0f0')
button_frame.pack(pady=10)

run_button = tk.Button(button_frame, text="Analisis Rute & Buka Peta", command=run_app,
                      bg="#27ae60", fg="white", font=("Arial", 10, "bold"), 
                      padx=15, pady=8, cursor="hand2")
run_button.pack()

# Status label
status_label = tk.Label(main_frame, text="⏳ Siap untuk analisis rute...", 
                       font=("Arial", 10), bg='#f0f0f0', fg="gray")
status_label.pack(pady=5)

# Results section
result_frame = tk.LabelFrame(main_frame, text="📊 Hasil Analisis", font=("Arial", 12, "bold"), 
                            bg='#f0f0f0', padx=10, pady=10)
result_frame.pack(fill='both', expand=True)

result_text = tk.Text(result_frame, height=15, font=("Consolas", 9), wrap=tk.WORD,
                     bg="white", relief="sunken", borderwidth=2)
result_text.pack(fill='both', expand=True, padx=5, pady=5)

# Info footer dengan informasi jam aktif
info_frame = tk.Frame(root, bg='#34495e', height=50)
info_frame.pack(fill='x')
info_frame.pack_propagate(False)

info_text = "Prediksi rute dan kemacetan berdasarkan data titik keramaian di Bengkulu " \
            "yang dilengkapi dengan AI Decision Tree untuk memprediksi tingkat kemacetan secara otomatis untuk memberikan rekomendasi rute terbaik."
tk.Label(info_frame, text=info_text, 
         fg="white", bg='#34495e', font=("Arial", 8), wraplength=650).pack(pady=8)

# Precompute saat startup
def startup_precompute():
    try:
        status_label.config(text="Inisialisasi sistem...", fg="blue")
        root.update()
        precompute_poi_edges()
        status_label.config(text="Sistem siap digunakan!", fg="green")
    except Exception as e:
        status_label.config(text=f"Warning: {str(e)}", fg="orange")

# Jalankan precompute di background
startup_thread = threading.Thread(target=startup_precompute, daemon=True)
startup_thread.start()

# Simulasi data training (jam, cuaca, jumlah_poi_aktif) -> kelas kemacetan
# 0: Cerah, 1: Mendung, 2: Hujan
X_train = []
y_train = []
for jam in range(24):
    for cuaca in [0, 1, 2]:
        for poi in range(4):
            # Aturan simulasi: makin banyak poi aktif, makin tinggi kemacetan
            if cuaca == 2 or jam in range(6,10) or jam in range(15,19):
                label = 2 if poi >= 2 else 1
            else:
                label = 1 if poi >= 2 else 0
            X_train.append([jam, cuaca, poi])
            y_train.append(label)
# 0: rendah, 1: sedang, 2: tinggi
dt_model = DecisionTreeClassifier()
dt_model.fit(X_train, y_train)
# joblib.dump(dt_model, 'dt_model.pkl') # Tidak perlu simpan file, langsung pakai

def predict_kemacetan_dt(jam, cuaca_str, poi_aktif):
    cuaca_map = {"Cerah": 0, "Mendung": 1, "Hujan": 2}
    cuaca = cuaca_map.get(cuaca_str, 0)
    pred = dt_model.predict([[jam, cuaca, poi_aktif]])
    label_map = {0: "Rendah", 1: "Sedang", 2: "Tinggi"}
    return label_map[pred[0]]

root.mainloop()