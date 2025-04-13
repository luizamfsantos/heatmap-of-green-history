# heatmap-of-green-history

# TL;DR
- Main goal of this project is to use MapBiomas alerts to detect deforestation hotspots, analyze their evolution over time, and layer them with socioeconomic and environmental data

# Data
- Geolocated deforestation alerts over [MapBiomas](https://plataforma.alerta.mapbiomas.org/api/docs/index.html)

# Processing
- Cluster alerts spatially and temporally. 
    - Ideas: 
        - Using classical graph-based community detection (e.g. Louvain)
        - Using graph machine learning (e.g. GNNs)
        - Using spatio-temporal clustering (e.g. DBSCAN)
- Detect birth/death/split/merge events of hotspot clusters

# Visualizations
- Evolving hotspots over time
- Overlay hotspots with:
    - Major cities
    - Economic growth indicators
    - Pollution scores
    - Native land

# Historical context
- Indigenous land demarcation
- Policy shits
- Infrastructure projects (e.g. roads, dams)
- Land use changes
- Climate events (e.g. droughts, floods)

