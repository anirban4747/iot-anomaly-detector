from scapy.all import rdpcap, IP
import pandas as pd
import numpy as np


def extract_live_features(pcap_path, window_size=100):
    """
    Parses a local PCAP file and aggregates packet sizes and
    inter-arrival times into structural rows for model inference.

    Uses non-overlapping windows: every `window_size` packets produces
    exactly one feature row, and the buffer is cleared after each window
    to keep memory usage bounded on large captures.
    """
    print(f"Ingesting raw network capture: {pcap_path}")
    try:
        packets = rdpcap(pcap_path)
    except FileNotFoundError:
        print("PCAP file target not found. Skipping execution.")
        return None

    features = []
    packet_buffer = []

    for pkt in packets:
        if pkt.haslayer(IP):
            packet_buffer.append({'size': len(pkt), 'time': float(pkt.time)})

            if len(packet_buffer) >= window_size:
                window = packet_buffer[:window_size]
                sizes = [p['size'] for p in window]
                times = [p['time'] for p in window]

                intervals = np.diff(times)
                mean_interval = np.mean(intervals) if len(intervals) > 0 else 0
                duration = times[-1] - times[0]

                features.append({
                    'mean_packet_size': np.mean(sizes),
                    'std_packet_size': np.std(sizes),
                    'packet_rate': window_size / duration if duration > 0 else 0,
                    'mean_inter_arrival': mean_interval
                })

                # Consume the processed window instead of letting the buffer grow unbounded
                packet_buffer = packet_buffer[window_size:]

    if not features:
        print(f"Not enough packets to fill a single window of size {window_size}.")

    return pd.DataFrame(features)


if __name__ == "__main__":
    print("Feature extraction pipeline initialized successfully.")