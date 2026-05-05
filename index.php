<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Car Price Predictor</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="min-h-screen bg-gradient-to-br from-teal-400 via-blue-500 to-purple-500 flex items-center justify-center relative overflow-hidden">

    <!-- LEFT DECOR -->
    <div class="hidden md:block absolute left-0 bottom-0 opacity-50">
        <img src="https://mycolor.space/img/color-scheme-left.svg" class="img-fluid w-[34rem]">
    </div>

    <!-- RIGHT DECOR -->
    <div class="hidden md:block absolute right-0 bottom-0 opacity-50">
        <img src="https://mycolor.space/img/color-scheme-right.svg" class="img-fluid w-[34rem]">
    </div>
    <div class="bg-white/90 backdrop-blur-lg p-8 rounded-2xl shadow-xl w-full max-w-2xl">

        <!-- Title -->
        <h1 class="text-2xl font-bold text-gray-800 text-center">
            Prediksi Harga Mobil Bekas
        </h1>

        <p class="text-gray-600 text-center mt-2 mb-6">
            Masukkan spesifikasi kendaraan untuk memprediksi harga jual kembali.
        </p>

        <!-- FORM -->
        <form id="predictForm" class="grid grid-cols-1 md:grid-cols-2 gap-4">

            <!-- Brand -->
            <select class="p-3 rounded-lg border">
                <option>Merek</option>
                <option>Toyota</option>
                <option>Honda</option>
                <option>Daihatsu</option>
            </select>

            <!-- Model -->
            <input type="text" placeholder="Model (Avanza, Jazz, dll)"
                class="p-3 rounded-lg border">

            <!-- Tahun -->
            <input type="number" placeholder="Tahun Produksi"
                class="p-3 rounded-lg border">

            <!-- Kilometer -->
            <input type="number" placeholder="Kilometer (km)"
                class="p-3 rounded-lg border">

            <!-- Fuel -->
            <select class="p-3 rounded-lg border">
                <option>Bahan Bakar</option>
                <option>Bensin</option>
                <option>Diesel</option>
            </select>

            <!-- Transmisi -->
            <select class="p-3 rounded-lg border">
                <option>Transmisi</option>
                <option>Manual</option>
                <option>Automatic</option>
            </select>

            <!-- Kondisi -->
            <select class="p-3 rounded-lg border">
                <option>Kondisi</option>
                <option>1 - Buruk</option>
                <option>2</option>
                <option>3</option>
                <option>4</option>
                <option>5 - Sangat Baik</option>
            </select>

            <!-- Tahun Prediksi -->
            <input type="number" placeholder="Prediksi X Tahun ke Depan"
                class="p-3 rounded-lg border">

            <!-- Button -->
            <button type="submit"
                class="col-span-1 md:col-span-2 mt-4 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg font-semibold hover:opacity-90">
                Prediksi Harga
            </button>

        </form>

        <!-- RESULT -->
        <div id="result" class="mt-6 text-center hidden">
            <p class="text-gray-700">Estimasi Harga:</p>
            <h2 class="text-2xl font-bold text-blue-600 mt-2">
                Rp 0
            </h2>
        </div>

    </div>

    <script>
        const form = document.getElementById("predictForm");
        const result = document.getElementById("result");

        form.addEventListener("submit", function(e) {
            e.preventDefault();

            // Dummy result (nanti diganti ML backend)
            result.classList.remove("hidden");
            result.querySelector("h2").innerText = "Rp 120.000.000";
        });
    </script>

</body>

</html>