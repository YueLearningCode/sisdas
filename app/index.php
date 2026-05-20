<!doctype html>
<html lang="id">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Prediksi Harga Mobil Bekas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap" rel="stylesheet">
    <style>
        :root {
            --ink: #172033;
            --muted: #667085;
            --line: #d9e2ec;
            --brand: #0f766e;
            --brand-dark: #115e59;
            --soft: #eef8f6;
            --accent: #f59e0b;
        }

        body {
            min-height: 100vh;
            background: #f7fafc;
            color: var(--ink);
            font-family: "Ubuntu", sans-serif;
        }

        .hero {
            background:
                linear-gradient(90deg, rgba(9, 47, 51, 0.92), rgba(15, 118, 110, 0.82)),
                url("https://cms.suzukihyperlocal.com/read-file?path=images/news/1722311483.webp") no-repeat;
            background-position: center;
            background-size: cover;
            color: white;
        }

        .hero-inner {
            min-height: 340px;
            display: flex;
            align-items: center;
            padding: 68px 0 52px;
        }

        .section {
            padding: 38px 0;
        }

        .panel {
            background: white;
            border: 1px solid var(--line);
            border-radius: 8px;
            box-shadow: 0 14px 30px rgba(15, 23, 42, 0.06);
        }

        .form-control,
        .form-select {
            border-radius: 6px;
            min-height: 44px;
        }

        .btn-primary {
            --bs-btn-bg: var(--brand);
            --bs-btn-border-color: var(--brand);
            --bs-btn-hover-bg: var(--brand-dark);
            --bs-btn-hover-border-color: var(--brand-dark);
            border-radius: 6px;
            min-height: 46px;
        }

        .price {
            font-size: clamp(28px, 5vw, 42px);
            font-weight: 700;
            color: var(--brand-dark);
            line-height: 1.1;
            overflow-wrap: anywhere;
        }

        .metric {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 14px;
            background: var(--soft);
        }

        .metric-label {
            color: var(--muted);
            font-size: 13px;
            margin-bottom: 4px;
        }

        .metric-value {
            font-weight: 700;
            color: var(--ink);
        }

        .bar-row {
            display: grid;
            grid-template-columns: minmax(92px, 120px) 1fr 48px;
            gap: 10px;
            align-items: center;
            margin-bottom: 12px;
            font-size: 14px;
        }

        .bar-track {
            height: 12px;
            background: #e5edf3;
            border-radius: 999px;
            overflow: hidden;
        }

        .bar-fill {
            height: 100%;
            background: var(--accent);
            border-radius: 999px;
        }

        .history-table {
            font-size: 14px;
        }

        .team-card {
            position: relative;
            aspect-ratio: 3 / 4;
            overflow: hidden;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #e5edf3;
            box-shadow: 0 10px 22px rgba(15, 23, 42, 0.08);
        }

        .team-photo {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
            transition: transform 0.28s ease;
        }

        .team-info {
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            padding: 16px 14px;
            color: white;
            background: linear-gradient(180deg, rgba(15, 23, 42, 0), rgba(15, 23, 42, 0.88));
            transform: translateY(100%);
            opacity: 0;
            transition: transform 0.28s ease, opacity 0.28s ease;
        }

        .team-card:hover .team-photo,
        .team-card:focus-within .team-photo {
            transform: scale(1.04);
        }

        .team-card:hover .team-info,
        .team-card:focus-within .team-info {
            transform: translateY(0);
            opacity: 1;
        }

        .team-name {
            font-weight: 700;
            margin-bottom: 3px;
            text-shadow: 0 1px 8px rgba(0, 0, 0, 0.28);
        }

        .team-nim {
            font-size: 14px;
            margin-bottom: 0;
            color: rgba(255, 255, 255, 0.86);
        }

        .text-muted-custom {
            color: var(--muted);
        }

        @media (max-width: 576px) {
            .hero-inner {
                min-height: 300px;
                padding: 48px 0 36px;
            }

            .bar-row {
                grid-template-columns: 1fr;
                gap: 6px;
            }
        }
    </style>
</head>

<body>
    <header class="hero">
        <div class="container hero-inner">
            <div class="col-lg-8">
                <span class="badge text-bg-light text-success mb-3">Random Forest Regressor</span>
                <h1 class="display-5 fw-bold mb-3">Prediksi Harga Mobil Bekas Berbasis Machine Learning</h1>
                <p class="lead mb-4">
                    Project pengembangan mahasiswa yang mengimplementasikan algoritma Random Forest Regression untuk memperkirakan harga mobil bekas berdasarkan spesifikasi kendaraan dan data historis.
                </p>
                <a href="#prediksi" class="btn btn-light btn-lg">Mulai Prediksi</a>
            </div>
        </div>
    </header>

    <main>
        <section id="prediksi" class="section">
            <div class="container">
                <div class="row g-4 align-items-start">
                    <div class="col-lg-7">
                        <div class="panel p-4 mb-4">
                            <div class="d-flex justify-content-between align-items-start gap-3 mb-3">
                                <div>
                                    <h2 class="h4 mb-1">Form Input Mobil</h2>
                                    <p class="text-muted-custom mb-0">Isi data utama kendaraan untuk prediksi harga.</p>
                                </div>
                                <span class="badge rounded-pill text-bg-success">POST /predict</span>
                            </div>

                            <form id="predictForm" class="row g-3">
                                <div class="col-md-6">
                                    <label for="brand" class="form-label">Brand</label>
                                    <select id="brand" name="brand" class="form-select" required>
                                        <option value="Toyota">Toyota</option>
                                        <option value="Honda">Honda</option>
                                        <option value="Daihatsu">Daihatsu</option>
                                        <option value="Suzuki">Suzuki</option>
                                        <option value="Nissan">Nissan</option>
                                        <option value="Mazda">Mazda</option>
                                        <option value="Mitsubishi">Mitsubishi</option>
                                        <option value="Hyundai">Hyundai</option>
                                    </select>
                                </div>

                                <div class="col-md-6">
                                    <label for="car_name" class="form-label">Nama Mobil</label>
                                    <select id="car_name" name="car_name" class="form-select" required>
                                        <option value="Daihatsu Ayla">Daihatsu Ayla</option>
                                        <option value="Daihatsu Sigra">Daihatsu Sigra</option>
                                        <option value="Daihatsu Terios">Daihatsu Terios</option>
                                        <option value="Daihatsu Xenia">Daihatsu Xenia</option>
                                        <option value="Honda Brio">Honda Brio</option>
                                        <option value="Honda City">Honda City</option>
                                        <option value="Honda CR-V">Honda CR-V</option>
                                        <option value="Honda HR-V">Honda HR-V</option>
                                        <option value="Honda Jazz">Honda Jazz</option>
                                        <option value="Honda Mobilio">Honda Mobilio</option>
                                        <option value="Hyundai Creta">Hyundai Creta</option>
                                        <option value="Hyundai Ioniq">Hyundai Ioniq</option>
                                        <option value="Hyundai Stargazer">Hyundai Stargazer</option>
                                        <option value="Mazda CX-5">Mazda CX-5</option>
                                        <option value="Mazda Mazda2">Mazda Mazda2</option>
                                        <option value="Mazda Mazda3">Mazda Mazda3</option>
                                        <option value="Mitsubishi Outlander">Mitsubishi Outlander</option>
                                        <option value="Mitsubishi Pajero">Mitsubishi Pajero</option>
                                        <option value="Mitsubishi Xpander">Mitsubishi Xpander</option>
                                        <option value="Nissan Livina">Nissan Livina</option>
                                        <option value="Nissan March">Nissan March</option>
                                        <option value="Nissan X-Trail">Nissan X-Trail</option>
                                        <option value="Suzuki Baleno">Suzuki Baleno</option>
                                        <option value="Suzuki Ertiga">Suzuki Ertiga</option>
                                        <option value="Suzuki Karimun">Suzuki Karimun</option>
                                        <option value="Suzuki XL7">Suzuki XL7</option>
                                        <option value="Toyota Agya">Toyota Agya</option>
                                        <option value="Toyota Avanza" selected>Toyota Avanza</option>
                                        <option value="Toyota Calya">Toyota Calya</option>
                                        <option value="Toyota Fortuner">Toyota Fortuner</option>
                                        <option value="Toyota Innova">Toyota Innova</option>
                                        <option value="Toyota Rush">Toyota Rush</option>
                                        <option value="Toyota Yaris">Toyota Yaris</option>
                                    </select>
                                </div>

                                <div class="col-md-4">
                                    <label for="year" class="form-label">Tahun</label>
                                    <input id="year" name="year" type="number" class="form-control" min="2000" max="2026" value="2020" required>
                                </div>

                                <div class="col-md-4">
                                    <label for="mileage_km" class="form-label">Kilometer</label>
                                    <input id="mileage_km" name="mileage_km" type="number" class="form-control" min="0" step="1000" value="50000" required>
                                </div>
                                
                                <div class="col-md-4">
                                    <label for="owner_count" class="form-label">Jumlah Pemilik</label>
                                    <input id="owner_count" name="owner_count" type="number" class="form-control" min="1" max="5" value="1">
                                </div>

                                <div class="col-md-6">
                                    <label for="engine_size_cc" class="form-label">Mesin</label>
                                    <select id="engine_size_cc" name="engine_size_cc" class="form-select">
                                        <option value="">Otomatis dari data</option>
                                        <option value="1000">1000 cc</option>
                                        <option value="1200">1200 cc</option>
                                        <option value="1300">1300 cc</option>
                                        <option value="1500">1500 cc</option>
                                        <option value="1800">1800 cc</option>
                                        <option value="2000">2000 cc</option>
                                        <option value="2400">2400 cc</option>
                                    </select>
                                </div>

                                <div class="col-md-6">
                                    <label for="transmission" class="form-label">Transmisi</label>
                                    <select id="transmission" name="transmission" class="form-select">
                                        <option value="">Otomatis dari data</option>
                                        <option value="Automatic">Automatic</option>
                                        <option value="Manual">Manual</option>
                                    </select>
                                </div>

                                <div class="col-md-6">
                                    <label for="fuel_type" class="form-label">Bahan Bakar</label>
                                    <select id="fuel_type" name="fuel_type" class="form-select">
                                        <option value="">Otomatis dari data</option>
                                        <option value="Petrol">Petrol</option>
                                        <option value="Diesel">Diesel</option>
                                        <option value="Hybrid">Hybrid</option>
                                        <option value="Electric">Electric</option>
                                    </select>
                                </div>

                                <div class="col-md-6">
                                    <label for="condition" class="form-label">Kondisi</label>
                                    <select id="condition" name="condition" class="form-select">
                                        <option value="">Otomatis dari data</option>
                                        <option value="Excellent">Excellent</option>
                                        <option value="Good">Good</option>
                                        <option value="Fair">Fair</option>
                                    </select>
                                </div>

                                <div class="col-md-6">
                                    <label for="location" class="form-label">Lokasi</label>
                                    <select id="location" name="location" class="form-select">
                                        <option value="">Otomatis dari data</option>
                                        <option value="Jakarta Utara">Jakarta Utara</option>
                                        <option value="Jakarta Barat">Jakarta Barat</option>
                                        <option value="Jakarta Selatan">Jakarta Selatan</option>
                                        <option value="Tangerang">Tangerang</option>
                                        <option value="Bekasi">Bekasi</option>
                                        <option value="Bogor">Bogor</option>
                                        <option value="Depok">Depok</option>
                                        <option value="Bandung">Bandung</option>
                                        <option value="Semarang">Semarang</option>
                                        <option value="Surabaya">Surabaya</option>
                                        <option value="Medan">Medan</option>
                                        <option value="Makassar">Makassar</option>
                                        <option value="Pekanbaru">Pekanbaru</option>
                                        <option value="Padang">Padang</option>
                                    </select>
                                </div>

                                <div class="col-md-6">
                                    <label for="color" class="form-label">Warna</label>
                                    <select id="color" name="color" class="form-select">
                                        <option value="">Otomatis dari data</option>
                                        <option value="Black">Black</option>
                                        <option value="White">White</option>
                                        <option value="Silver">Silver</option>
                                        <option value="Gray">Gray</option>
                                        <option value="Red">Red</option>
                                        <option value="Blue">Blue</option>
                                    </select>
                                </div>

                                <div class="col-12">
                                    <button id="submitButton" type="submit" class="btn btn-primary w-100">Prediksi Harga</button>
                                </div>
                            </form>
                        </div>

                        <div class="panel p-4">
                            <h2 class="h4 mb-3">Faktor Paling Berpengaruh</h2>
                            <p class="text-muted-custom small mb-3">Kriteria dengan kontribusi terbesar pada model Random Forest.</p>
                            <div id="featureImportanceChart"></div>
                        </div>
                    </div>

                    <div class="col-lg-5">
                        <div class="panel p-4 mb-4">
                            <h2 class="h4 mb-3">Hasil Prediksi</h2>
                            <p class="text-muted-custom mb-2">Estimasi harga</p>
                            <div id="predictedPrice" class="price mb-3">Rp 0</div>

                            <div class="row g-3">
                                <div class="col-md-6">
                                    <div class="metric">
                                        <div class="metric-label">Confidence</div>
                                        <div id="confidenceLabel" class="metric-value">-</div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="metric">
                                        <div class="metric-label">R2 Score</div>
                                        <div id="r2Score" class="metric-value">-</div>
                                    </div>
                                </div>
                                <div class="col-12">
                                    <div class="metric">
                                        <div class="metric-label">Rentang estimasi berdasarkan RMSE</div>
                                        <div id="priceRange" class="metric-value">-</div>
                                    </div>
                                </div>
                                <div class="col-12">
                                    <div class="metric">
                                        <div class="metric-label">Perbandingan harga pasar</div>
                                        <div id="marketComparison" class="metric-value">-</div>
                                        <div id="marketDetail" class="small text-muted-custom mt-1"></div>
                                    </div>
                                </div>
                            </div>

                            <div id="messageBox" class="alert mt-3 mb-0 d-none" role="alert"></div>
                        </div>

                        <div class="panel p-4">
                            <h2 class="h4 mb-3">Distribusi Harga Dataset</h2>
                            <p id="datasetInfo" class="text-muted-custom small mb-3">Memuat statistik dataset.</p>
                            <div id="distributionChart"></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="section pt-0">
            <div class="container">
                <div class="panel p-4">
                    <div class="d-flex justify-content-between align-items-center gap-3 mb-3">
                        <div>
                            <h2 class="h4 mb-1">Riwayat Prediksi</h2>
                            <p class="text-muted-custom mb-0">Disimpan sementara di browser untuk demo localhost.</p>
                        </div>
                        <button id="clearHistoryButton" type="button" class="btn btn-outline-secondary btn-sm">Hapus Riwayat</button>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-sm align-middle history-table mb-0">
                            <thead>
                                <tr>
                                    <th>Mobil</th>
                                    <th>Tahun</th>
                                    <th>Kilometer</th>
                                    <th>Prediksi</th>
                                    <th>Confidence</th>
                                    <th>Pasar</th>
                                </tr>
                            </thead>
                            <tbody id="historyBody">
                                <tr>
                                    <td colspan="6" class="text-muted-custom">Belum ada riwayat.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>

        <section class="section pt-0">
            <div class="container">
                <div class="panel p-4">
                    <div class="mb-4">
                        <h2 class="h4 mb-1">Profil Team</h2>
                        <p class="text-muted-custom mb-0">Kelompok 1 Sisdas</p>
                    </div>

                    <div class="row g-3">
                        <div class="col-md-6 col-lg-2">
                            <div class="team-card" tabindex="0">
                                <img class="team-photo" src="asset/arma.jpeg" alt="Foto profil Grahadi Arma W">
                                <div class="team-info">
                                    <div class="team-name">Grahadi Arma W</div>
                                    <p class="team-nim">NIM 2403111017</p>
                                </div>
                            </div>
                        </div>

                        <div class="col-md-6 col-lg-2">
                            <div class="team-card" tabindex="0">
                                <img class="team-photo" src="asset/irsal.jpeg" alt="Foto profil Mhd Irsal">
                                <div class="team-info">
                                    <div class="team-name">Mhd Irsal</div>
                                    <p class="team-nim">NIM 2403114255</p>
                                </div>
                            </div>
                        </div>

                        <div class="col-md-6 col-lg-2">
                            <div class="team-card" tabindex="0">
                                <img class="team-photo" src="asset/michel.jpeg" alt="Foto profil Michael Elfredo P">
                                <div class="team-info">
                                    <div class="team-name">Michael Elfredo P</div>
                                    <p class="team-nim">NIM 2403112307</p>
                                </div>
                            </div>
                        </div>

                        <div class="col-md-6 col-lg-2">
                            <div class="team-card" tabindex="0">
                                <img class="team-photo" src="asset/nurul.jpeg" alt="Foto profil Nurul Triatika">
                                <div class="team-info">
                                    <div class="team-name">Nurul Triatika</div>
                                    <p class="team-nim">NIM 2403111759</p>
                                </div>
                            </div>
                        </div>

                        <div class="col-md-6 col-lg-2">
                            <div class="team-card" tabindex="0">
                                <img class="team-photo" src="asset/puan.jpeg" alt="Foto profil Puan Nabila Risty">
                                <div class="team-info">
                                    <div class="team-name">Puan Nabila Risty</div>
                                    <p class="team-nim">NIM 2403111378</p>
                                </div>
                            </div>
                        </div>

                        <div class="col-md-6 col-lg-2">
                            <div class="team-card" tabindex="0">
                                <img class="team-photo" src="asset/rasyid.jpeg" alt="Foto profil Rasyid Saputra">
                                <div class="team-info">
                                    <div class="team-name">Rasyid Saputra</div>
                                    <p class="team-nim">NIM 2403127126</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <script>
        const API_BASE_URL = "http://127.0.0.1:5001";
        const HISTORY_KEY = "carPricePredictionHistory";
        const CAR_BRAND_MAP = {
            "Daihatsu Ayla": "Daihatsu",
            "Daihatsu Sigra": "Daihatsu",
            "Daihatsu Terios": "Daihatsu",
            "Daihatsu Xenia": "Daihatsu",
            "Honda Brio": "Honda",
            "Honda City": "Honda",
            "Honda CR-V": "Honda",
            "Honda HR-V": "Honda",
            "Honda Jazz": "Honda",
            "Honda Mobilio": "Honda",
            "Hyundai Creta": "Hyundai",
            "Hyundai Ioniq": "Hyundai",
            "Hyundai Stargazer": "Hyundai",
            "Mazda CX-5": "Mazda",
            "Mazda Mazda2": "Mazda",
            "Mazda Mazda3": "Mazda",
            "Mitsubishi Outlander": "Mitsubishi",
            "Mitsubishi Pajero": "Mitsubishi",
            "Mitsubishi Xpander": "Mitsubishi",
            "Nissan Livina": "Nissan",
            "Nissan March": "Nissan",
            "Nissan X-Trail": "Nissan",
            "Suzuki Baleno": "Suzuki",
            "Suzuki Ertiga": "Suzuki",
            "Suzuki Karimun": "Suzuki",
            "Suzuki XL7": "Suzuki",
            "Toyota Agya": "Toyota",
            "Toyota Avanza": "Toyota",
            "Toyota Calya": "Toyota",
            "Toyota Fortuner": "Toyota",
            "Toyota Innova": "Toyota",
            "Toyota Rush": "Toyota",
            "Toyota Yaris": "Toyota"
        };
        const form = document.getElementById("predictForm");
        const button = document.getElementById("submitButton");
        const brandInput = document.getElementById("brand");
        const carNameInput = document.getElementById("car_name");
        const predictedPrice = document.getElementById("predictedPrice");
        const confidenceLabel = document.getElementById("confidenceLabel");
        const r2Score = document.getElementById("r2Score");
        const priceRange = document.getElementById("priceRange");
        const marketComparison = document.getElementById("marketComparison");
        const marketDetail = document.getElementById("marketDetail");
        const messageBox = document.getElementById("messageBox");
        const distributionChart = document.getElementById("distributionChart");
        const featureImportanceChart = document.getElementById("featureImportanceChart");
        const datasetInfo = document.getElementById("datasetInfo");
        const historyBody = document.getElementById("historyBody");
        const clearHistoryButton = document.getElementById("clearHistoryButton");

        function formatRupiah(value) {
            return new Intl.NumberFormat("id-ID", {
                style: "currency",
                currency: "IDR",
                maximumFractionDigits: 0
            }).format(value);
        }

        function getOptionalValue(formData, key) {
            const value = formData.get(key);
            return value === "" ? null : value;
        }

        function setMessage(type, text) {
            messageBox.className = `alert alert-${type} mt-3 mb-0`;
            messageBox.textContent = text;
        }

        function getHistory() {
            return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
        }

        function saveHistory(item) {
            const history = [item, ...getHistory()].slice(0, 8);
            localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
            renderHistory();
        }

        function renderHistory() {
            const history = getHistory();
            if (history.length === 0) {
                historyBody.innerHTML = '<tr><td colspan="6" class="text-muted-custom">Belum ada riwayat.</td></tr>';
                return;
            }

            historyBody.innerHTML = history.map((item) => `
                <tr>
                    <td>${item.car_name || item.brand}</td>
                    <td>${item.year}</td>
                    <td>${Number(item.mileage_km).toLocaleString("id-ID")} km</td>
                    <td>${formatRupiah(item.predicted_price)}</td>
                    <td>${item.confidence}</td>
                    <td>${item.market_category}</td>
                </tr>
            `).join("");
        }

        function renderDistribution(distribution) {
            if (!distribution || distribution.length === 0) {
                distributionChart.innerHTML = '<p class="text-muted-custom mb-0">Distribusi belum tersedia.</p>';
                return;
            }

            const maxCount = Math.max(...distribution.map((item) => item.count), 1);
            distributionChart.innerHTML = distribution.map((item) => {
                const width = Math.max((item.count / maxCount) * 100, 4);
                return `
                    <div class="bar-row">
                        <div>${item.label}</div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: ${width}%"></div>
                        </div>
                        <div>${item.count}</div>
                    </div>
                `;
            }).join("");
        }

        function updateCarNameOptions(selectedCarName = null) {
            const selectedBrand = brandInput.value;
            const matchingCarNames = Object.keys(CAR_BRAND_MAP).filter(
                (carName) => CAR_BRAND_MAP[carName] === selectedBrand
            );

            carNameInput.innerHTML = matchingCarNames.map((carName) => (
                `<option value="${carName}">${carName}</option>`
            )).join("");

            if (selectedCarName && matchingCarNames.includes(selectedCarName)) {
                carNameInput.value = selectedCarName;
                return;
            }

            if (matchingCarNames.length > 0) {
                carNameInput.value = matchingCarNames[0];
            }
        }

        function renderFeatureImportance(features) {
            if (!features || features.length === 0) {
                featureImportanceChart.innerHTML = '<p class="text-muted-custom mb-0">Feature importance belum tersedia.</p>';
                return;
            }

            const maxImportance = Math.max(...features.map((item) => item.importance), 1);
            featureImportanceChart.innerHTML = features.map((item) => {
                const width = Math.max((item.importance / maxImportance) * 100, 4);
                return `
                    <div class="bar-row">
                        <div>${item.feature}</div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: ${width}%"></div>
                        </div>
                        <div>${item.percentage}%</div>
                    </div>
                `;
            }).join("");
        }

        async function loadStats() {
            try {
                const response = await fetch(`${API_BASE_URL}/stats`);
                const data = await response.json();
                datasetInfo.textContent = `${data.dataset_rows} data mobil, R2 model ${data.metrics.r2_score}.`;
                renderFeatureImportance(data.feature_importance);
                renderDistribution(data.price_distribution);
            } catch (error) {
                datasetInfo.textContent = "Statistik belum bisa dimuat. Pastikan Flask API aktif.";
                featureImportanceChart.innerHTML = '<p class="text-muted-custom mb-0">Feature importance belum bisa dimuat.</p>';
            }
        }

        form.addEventListener("submit", async function(event) {
            event.preventDefault();
            const formData = new FormData(form);

            const payload = {
                car_name: formData.get("car_name"),
                brand: formData.get("brand"),
                year: Number(formData.get("year")),
                mileage_km: Number(formData.get("mileage_km")),
                engine_size_cc: getOptionalValue(formData, "engine_size_cc") ? Number(formData.get("engine_size_cc")) : null,
                transmission: getOptionalValue(formData, "transmission"),
                fuel_type: getOptionalValue(formData, "fuel_type"),
                condition: getOptionalValue(formData, "condition"),
                location: getOptionalValue(formData, "location"),
                color: getOptionalValue(formData, "color"),
                owner_count: formData.get("owner_count") ? Number(formData.get("owner_count")) : null
            };

            button.disabled = true;
            button.textContent = "Memproses...";
            setMessage("info", "Mengirim data ke Flask API.");

            try {
                const response = await fetch(`${API_BASE_URL}/predict`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.error || "Prediksi gagal.");
                }

                predictedPrice.textContent = formatRupiah(data.predicted_price);
                confidenceLabel.textContent = data.confidence.label;
                r2Score.textContent = data.confidence.r2_score;
                priceRange.textContent = `${formatRupiah(data.confidence.price_range.min)} - ${formatRupiah(data.confidence.price_range.max)}`;
                marketComparison.textContent = data.market_comparison.category;
                marketDetail.textContent = `Rata-rata pasar ${formatRupiah(data.market_comparison.average_price)} dari ${data.market_comparison.sample_count} data pembanding.`;

                saveHistory({
                    car_name: payload.car_name,
                    brand: payload.brand,
                    year: payload.year,
                    mileage_km: payload.mileage_km,
                    predicted_price: data.predicted_price,
                    confidence: data.confidence.label,
                    market_category: data.market_comparison.category
                });

                setMessage("success", "Prediksi berhasil diproses.");
            } catch (error) {
                setMessage("danger", error.message);
            } finally {
                button.disabled = false;
                button.textContent = "Prediksi Harga";
            }
        });

        clearHistoryButton.addEventListener("click", function() {
            localStorage.removeItem(HISTORY_KEY);
            renderHistory();
        });

        carNameInput.addEventListener("change", function() {
            const selectedBrand = CAR_BRAND_MAP[carNameInput.value];
            if (selectedBrand) {
                brandInput.value = selectedBrand;
                updateCarNameOptions(carNameInput.value);
            }
        });

        brandInput.addEventListener("change", function() {
            updateCarNameOptions();
        });

        updateCarNameOptions("Toyota Avanza");
        loadStats();
        renderHistory();
    </script>
</body>

</html>
