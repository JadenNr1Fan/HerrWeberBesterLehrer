<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scenery Map</title>

    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css">

    <style>
        * { box-sizing: border-box; }

        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background: #f4f4f4;
            color: #17211f;
        }

        header {
            background: #2f5d50;
            color: white;
            text-align: center;
            padding: 22px 16px;
        }

        header h1 { margin: 0 0 6px; }
        header p { margin: 0; opacity: 0.9; }

        #map {
            height: 620px;
            width: 100%;
        }

        .map-toolbar {
            position: absolute;
            top: 145px;
            left: 18px;
            z-index: 900;
            width: min(380px, calc(100% - 36px));
            background: rgba(255, 255, 255, 0.96);
            padding: 14px;
            border-radius: 14px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.22);
        }

        .map-toolbar label {
            display: block;
            font-weight: bold;
            margin-bottom: 7px;
        }

        .search-row {
            display: flex;
            gap: 8px;
        }

        .search-row input, .upload-modal input {
            width: 100%;
            padding: 10px;
            border: 1px solid #c9d1cd;
            border-radius: 8px;
        }

        button {
            background: #2f5d50;
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }

        button:hover { background: #24483f; }

        .hint {
            font-size: 13px;
            margin-top: 8px;
            color: #4d5c57;
            line-height: 1.35;
        }

        .content {
            padding: 24px;
        }

        .gallery {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
        }

        .card {
            background: white;
            padding: 10px;
            border-radius: 12px;
            width: 220px;
            box-shadow: 0 3px 14px rgba(0, 0, 0, 0.1);
        }

        .card img, .card .pdf-card {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 8px;
            background: #e8ecea;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 42px;
            text-decoration: none;
            color: #2f5d50;
        }

        .card h4 { margin: 10px 0 4px; }
        .card p { margin: 0; color: #5f6e69; }

        .hover-preview {
            position: fixed;
            z-index: 2000;
            pointer-events: none;
            display: none;
            background: white;
            padding: 10px;
            border-radius: 14px;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.35);
            max-width: 330px;
        }

        .hover-preview img {
            width: 300px;
            max-height: 230px;
            object-fit: contain;
            border-radius: 10px;
        }

        .hover-preview .pdf-preview {
            width: 300px;
            height: 180px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #eef1ef;
            color: #2f5d50;
            font-size: 54px;
        }

        .hover-preview strong {
            display: block;
            margin-top: 8px;
        }

        .modal-backdrop-custom {
            position: fixed;
            inset: 0;
            z-index: 3000;
            display: none;
            align-items: center;
            justify-content: center;
            background: rgba(0, 0, 0, 0.7);
            padding: 20px;
        }

        .upload-modal, .image-modal, .top-modal {
            background: white;
            border-radius: 16px;
            max-width: 760px;
            width: 100%;
            padding: 22px;
            position: relative;
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.35);
        }

        .upload-modal h2, .image-modal h2, .top-modal h2 { margin-top: 0; }

        .upload-modal form p { margin: 12px 0; }
        .upload-modal input[type="file"] { border: none; padding-left: 0; }

        .close-btn {
            position: absolute;
            top: 12px;
            right: 14px;
            background: #d94f4f;
            padding: 7px 11px;
            border-radius: 999px;
        }

        .selected-location {
            background: #eef6f3;
            border-left: 4px solid #2f5d50;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 12px;
        }

        .image-modal img {
            width: 100%;
            max-height: 75vh;
            object-fit: contain;
            border-radius: 12px;
            background: #f3f3f3;
        }

        .image-modal iframe {
            width: 100%;
            height: 75vh;
            border: none;
            border-radius: 12px;
        }

        .vote-box {
            position: fixed;
            right: 20px;
            bottom: 20px;
            z-index: 2500;
            display: none;
            gap: 8px;
            align-items: center;
            background: rgba(255, 255, 255, 0.96);
            border-radius: 999px;
            padding: 10px 12px;
            box-shadow: 0 7px 25px rgba(0, 0, 0, 0.25);
        }

        .vote-box button {
            font-size: 24px;
            background: #eef1ef;
            color: #17211f;
            padding: 8px 12px;
        }

        .vote-box span { font-weight: bold; min-width: 26px; text-align: center; }

        .top-overlay {
            position: fixed;
            inset: 0;
            z-index: 4000;
            display: none;
            align-items: center;
            justify-content: center;
            background: rgba(0, 0, 0, 0.72);
            padding: 20px;
        }

        .top-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 14px;
        }

        .top-item {
            background: #f7f9f8;
            border-radius: 12px;
            padding: 10px;
            cursor: pointer;
        }

        .top-item img, .top-item .pdf-card {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 9px;
            background: #e8ecea;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 42px;
            color: #2f5d50;
        }

        .error-list {
            background: #ffe8e8;
            border-left: 4px solid #d94f4f;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 12px;
        }
    </style>
</head>
<body>

<header>
    <h1>Scenery Map</h1>
    <p>Suche zuerst einen Ort, klicke dann doppelt auf die genaue Stelle und lade dort dein PNG/PDF hoch.</p>
</header>

<div class="map-toolbar">
    <label for="place-search">Allgemeinen Ort suchen</label>
    <div class="search-row">
        <input id="place-search" type="text" placeholder="z. B. Zürich, Spanien, Paris">
        <button id="search-btn" type="button">Suchen</button>
    </div>
    <div class="hint" id="map-hint">Danach doppelt auf die genaue Stelle auf der Karte klicken.</div>
</div>

<div id="map"></div>

<div class="content">
    <h2>Hochgeladene Dateien</h2>

    <div class="gallery">
        {% for img in images %}
            <div class="card">
                {% if img.is_pdf %}
                    <a class="pdf-card" href="{{ img.image.url }}" target="_blank">PDF</a>
                {% else %}
                    <img src="{{ img.image.url }}" alt="{{ img.title }}">
                {% endif %}
                <h4>{{ img.title }}</h4>
                <p>{{ img.origin }}</p>
                <p>👍 {{ img.likes }} · 👎 {{ img.dislikes }}</p>
            </div>
        {% empty %}
            <p>Noch keine Dateien hochgeladen.</p>
        {% endfor %}
    </div>
</div>

<div class="hover-preview" id="hover-preview"></div>

<div class="modal-backdrop-custom" id="upload-backdrop">
    <div class="upload-modal">
        <button class="close-btn" type="button" data-close="upload-backdrop">×</button>
        <h2>Neue Datei an dieser Stelle hinzufügen</h2>
        {% if form.errors %}
            <div class="error-list">{{ form.errors }}</div>
        {% endif %}
        <div class="selected-location" id="selected-location-text">Noch kein Punkt gewählt.</div>
        <form method="POST" enctype="multipart/form-data" id="upload-form">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Hochladen</button>
        </form>
    </div>
</div>

<div class="modal-backdrop-custom" id="image-backdrop">
    <div class="image-modal">
        <button class="close-btn" type="button" data-close="image-backdrop">×</button>
        <h2 id="image-modal-title"></h2>
        <div id="image-modal-content"></div>
    </div>
</div>

<div class="vote-box" id="vote-box">
    <button type="button" id="like-btn" title="Like">👍</button>
    <span id="like-count">0</span>
    <button type="button" id="dislike-btn" title="Dislike">👎</button>
    <span id="dislike-count">0</span>
</div>

<div class="top-overlay" id="top-overlay">
    <div class="top-modal">
        <button class="close-btn" type="button" data-close="top-overlay">×</button>
        <h2>Top 3 meist gelikte Bilder</h2>
        <div class="top-grid" id="top-grid"></div>
    </div>
</div>

<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<script>
    const images = JSON.parse('{{ image_data_json|escapejs }}');
    const topImages = JSON.parse('{{ top_images_json|escapejs }}');
    const voteUrlTemplate = "{% url 'vote-image' 999999 %}";

    const map = L.map('map').setView([20, 0], 2);
    map.doubleClickZoom.disable();

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);

    let selectedMarker = null;
    let activeImage = null;

    const hoverPreview = document.getElementById('hover-preview');
    const voteBox = document.getElementById('vote-box');
    const likeCount = document.getElementById('like-count');
    const dislikeCount = document.getElementById('dislike-count');

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    function filePreviewHtml(img, large = false) {
        if (img.is_pdf) {
            if (large) {
                return `<iframe src="${img.url}"></iframe><p><a href="${img.url}" target="_blank">PDF in neuem Tab öffnen</a></p>`;
            }
            return `<div class="pdf-preview">PDF</div>`;
        }
        return `<img src="${img.url}" alt="${img.title}">`;
    }

    function openImageModal(img) {
        activeImage = img;
        document.getElementById('image-modal-title').textContent = `${img.title} · ${img.origin}`;
        document.getElementById('image-modal-content').innerHTML = filePreviewHtml(img, true);
        document.getElementById('image-backdrop').style.display = 'flex';
        updateVoteBox(img);
    }

    function updateVoteBox(img) {
        voteBox.style.display = 'flex';
        likeCount.textContent = img.likes;
        dislikeCount.textContent = img.dislikes;
    }

    function addImageMarker(img) {
        const marker = L.marker([img.latitude, img.longitude]).addTo(map);
        marker.bindTooltip(img.title, {direction: 'top'});

        marker.on('mouseover', function(e) {
            hoverPreview.innerHTML = `${filePreviewHtml(img)}<strong>${img.title}</strong><small>${img.origin}</small>`;
            hoverPreview.style.display = 'block';
        });

        marker.on('mousemove', function(e) {
            hoverPreview.style.left = (e.originalEvent.clientX + 18) + 'px';
            hoverPreview.style.top = (e.originalEvent.clientY + 18) + 'px';
        });

        marker.on('mouseout', function() {
            hoverPreview.style.display = 'none';
        });

        marker.on('click', function() {
            openImageModal(img);
        });
    }

    images.forEach(addImageMarker);

    document.getElementById('search-btn').addEventListener('click', function() {
        const query = document.getElementById('place-search').value.trim();
        if (!query) return;

        document.getElementById('map-hint').textContent = 'Ort wird gesucht...';

        fetch('https://nominatim.openstreetmap.org/search?format=json&limit=1&q=' + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {
                if (!data.length) {
                    document.getElementById('map-hint').textContent = 'Ort nicht gefunden. Versuche es genauer.';
                    return;
                }

                const lat = parseFloat(data[0].lat);
                const lon = parseFloat(data[0].lon);
                map.setView([lat, lon], 13);
                document.getElementById('id_origin').value = query;
                document.getElementById('map-hint').textContent = 'Jetzt auf die genaue Stelle doppelklicken.';
            })
            .catch(() => {
                document.getElementById('map-hint').textContent = 'Suche fehlgeschlagen. Prüfe deine Internetverbindung.';
            });
    });

    document.getElementById('place-search').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            document.getElementById('search-btn').click();
        }
    });

    map.on('dblclick', function(e) {
        const lat = e.latlng.lat.toFixed(6);
        const lon = e.latlng.lng.toFixed(6);

        document.getElementById('id_latitude').value = lat;
        document.getElementById('id_longitude').value = lon;
        document.getElementById('selected-location-text').textContent = `Ausgewählte Koordinaten: ${lat}, ${lon}`;

        if (selectedMarker) {
            selectedMarker.setLatLng(e.latlng);
        } else {
            selectedMarker = L.marker(e.latlng).addTo(map);
        }

        document.getElementById('upload-backdrop').style.display = 'flex';
    });

    document.querySelectorAll('[data-close]').forEach(button => {
        button.addEventListener('click', function() {
            document.getElementById(this.dataset.close).style.display = 'none';
            if (this.dataset.close === 'image-backdrop') {
                activeImage = null;
                voteBox.style.display = 'none';
            }
        });
    });

    function sendVote(voteType) {
        if (!activeImage) return;

        fetch(voteUrlTemplate.replace('999999', activeImage.id), {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'vote=' + encodeURIComponent(voteType)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) return;
            activeImage.likes = data.likes;
            activeImage.dislikes = data.dislikes;
            updateVoteBox(activeImage);
        });
    }

    document.getElementById('like-btn').addEventListener('click', () => sendVote('like'));
    document.getElementById('dislike-btn').addEventListener('click', () => sendVote('dislike'));

    function showTopOverlay() {
        if (!topImages.length) return;

        const grid = document.getElementById('top-grid');
        grid.innerHTML = '';

        topImages.forEach((img, index) => {
            const item = document.createElement('div');
            item.className = 'top-item';
            item.innerHTML = `
                ${img.is_pdf ? '<div class="pdf-card">PDF</div>' : `<img src="${img.url}" alt="${img.title}">`}
                <h3>#${index + 1} ${img.title}</h3>
                <p>${img.origin}</p>
                <p>👍 ${img.likes} · 👎 ${img.dislikes}</p>
            `;
            item.addEventListener('click', () => {
                document.getElementById('top-overlay').style.display = 'none';
                openImageModal(img);
            });
            grid.appendChild(item);
        });

        document.getElementById('top-overlay').style.display = 'flex';
    }

    window.addEventListener('load', showTopOverlay);

    {% if form.errors %}
        document.getElementById('upload-backdrop').style.display = 'flex';
    {% endif %}
</script>

</body>
</html>
