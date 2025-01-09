document.addEventListener('DOMContentLoaded', function () {
    // element referanslarını al
    const elements = {
        brand: document.getElementById('brand-select'),
        series: document.getElementById('series-select'),
        model: document.getElementById('model-select'),
        body: document.getElementById('body-select'),
        transmission: document.getElementById('transmission-select'),
        fuel: document.getElementById('fuel-select'),
        additionalInputs: document.getElementById('additional-inputs'),
        year: document.getElementById('year-select'),
        kmInput: document.getElementById('km-input'),
        predictBtn: document.getElementById('predict-btn'),
        resultDiv: document.getElementById('result'),
        errorDiv: document.getElementById('error')
    };

    // seçim elementini doldur
    function populateSelect(selectElement, data, placeholder) {
        resetSelect(selectElement, placeholder);
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item;
            option.textContent = item;
            selectElement.appendChild(option);
        });
        selectElement.disabled = false;
    }

    // seçim elementini sıfırla
    function resetSelect(selectElement, placeholder) {
        selectElement.innerHTML = `<option value="">${placeholder}</option>`;
        selectElement.disabled = true;
    }

    // API'dan veri çek ve seçim elementini doldur
    function fetchData(endpoint, selectElement, placeholder) {
        console.log(`Fetching data from: ${endpoint}`);
        fetch(endpoint)
            .then(response => response.json())
            .then(data => {
                console.log(`Data fetched for ${placeholder}:`, data);
                populateSelect(selectElement, data[Object.keys(data)[0]], placeholder);
            })
            .catch(error => console.error(`Error fetching ${placeholder}:`, error));
    }

    // markaları çek ve seçim elementini doldur
    fetch('/get-brands')
        .then(response => response.json())
        .then(data => {
            if (data.brands && data.brands.length) {
                populateSelect(elements.brand, data.brands, 'Marka Seç');
                elements.brand.disabled = false;
            }
        })
        .catch(error => console.error('Error fetching brands:', error));

    // yılları çek ve seçim elementini doldur
    fetchData('/get-years', elements.year, 'Yıl Seç');

    // marka seçildiğinde serileri çek
    elements.brand.addEventListener('change', function () {
        const brand = elements.brand.value;
        resetSelect(elements.series, 'Seri Seç');
        resetSelect(elements.model, 'Model Seç');
        resetSelect(elements.body, 'Kasa Tipini Seç');
        resetSelect(elements.transmission, 'Vites Tipini Seç');
        resetSelect(elements.fuel, 'Yakıt Tipini Seç');
        elements.additionalInputs.style.display = 'none';

        if (brand) {
            fetchData(`/get-series?brand=${encodeURIComponent(brand)}`, elements.series, 'Seri Seç');
        }
    });

    // seri seçildiğinde modelleri çek
    elements.series.addEventListener('change', function () {
        const series = elements.series.value;
        resetSelect(elements.model, 'Model Seç');
        resetSelect(elements.body, 'Kasa Tipini Seç');
        resetSelect(elements.transmission, 'Vites Tipini Seç');
        resetSelect(elements.fuel, 'Yakıt Tipini Seç');
        elements.additionalInputs.style.display = 'none';

        if (series) {
            fetchData(`/get-models?series=${encodeURIComponent(series)}`, elements.model, 'Model Seç');
        }
    });

    // model seçildiğinde kasa tiplerini çek
    elements.model.addEventListener('change', function () {
        const model = elements.model.value;
        resetSelect(elements.body, 'Kasa Tipini Seç');
        resetSelect(elements.transmission, 'Vites Tipini Seç');
        resetSelect(elements.fuel, 'Yakıt Tipini Seç');
        elements.additionalInputs.style.display = 'none';

        if (model) {
            fetchData(`/get-bodies?model=${encodeURIComponent(model)}`, elements.body, 'Kasa Tipini Seç');
        }
    });

    // kasa tipi seçildiğinde vites tiplerini çek
    elements.body.addEventListener('change', function () {
        const body = elements.body.value;
        resetSelect(elements.transmission, 'Vites Tipini Seç');
        resetSelect(elements.fuel, 'Yakıt Tipini Seç');
        elements.additionalInputs.style.display = 'none';

        if (body) {
            fetchData(`/get-transmissions?body=${encodeURIComponent(body)}`, elements.transmission, 'Vites Tipini Seç');
        }
    });

    // vites tipi seçildiğinde yakıt tiplerini çek
    elements.transmission.addEventListener('change', function () {
        const transmission = elements.transmission.value;
        resetSelect(elements.fuel, 'Yakıt Tipini Seç');
        elements.additionalInputs.style.display = 'none';

        if (transmission) {
            fetchData(`/get-fuels?transmission=${encodeURIComponent(transmission)}`, elements.fuel, 'Yakıt Tipini Seç');
        }
    });

    // yakıt tipi seçildiğinde ek girişleri göster (yıl ve kilometre)
    elements.fuel.addEventListener('change', function () {
        elements.additionalInputs.style.display = elements.fuel.value ? 'block' : 'none';
    });

    // tahmin butonuna tıklandığında verileri topla
    elements.predictBtn.addEventListener('click', function (event) {
        event.preventDefault();
        console.log('Predict button clicked');

        const data = {
            brand: elements.brand.value,
            series: elements.series.value,
            model: elements.model.value,
            body: elements.body.value,
            transmission: elements.transmission.value,
            fuel: elements.fuel.value,
            year: elements.year.value,
            km: elements.kmInput.value
        };

        console.log('Data to be sent:', data);

        // boş alanların kontrolü
        if (Object.values(data).some(value => !value)) {
            alert('Lütfen tüm alanları doldurun!');
            return;
        }

        // tahmin isteği gönder
        fetch('/predict-price', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(result => {
            console.log('Predict result:', result);
            if (result.price) {
                elements.resultDiv.innerHTML = `<p>Tahmini Fiyat: <strong>${result.price} TL</strong></p>
                                                <button id="suggest-btn">Öneride Bulun</button>`;
                elements.resultDiv.style.display = 'block';
                // öneriler kısmı
                document.getElementById('suggest-btn').addEventListener('click', () => {
                    fetch('/suggest-cars', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ price: result.price })
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Suggestions data:', data);
                        if (data.suggestions) {
                            let suggestionHTML = '<table><thead><tr><th>Marka</th><th>Seri</th><th>Model</th><th>Yıl</th><th>Kilometre</th><th>Vites Tipi</th><th>Yakıt Tipi</th><th>Fiyat</th></tr></thead><tbody>';
                            data.suggestions.forEach(car => {
                                suggestionHTML += `<tr>
                                    <td>${car.Marka}</td>
                                    <td>${car.Seri}</td>
                                    <td>${car.Model}</td>
                                    <td>${car.Yıl}</td>
                                    <td>${car.Kilometre}</td>
                                    <td>${car.VitesTipi}</td>
                                    <td>${car.YakıtTipi}</td>
                                    <td class="price">${car.Fiyat} TL</td>
                                </tr>`;
                            });
                            suggestionHTML += '</tbody></table>';
                            document.getElementById('suggestions').innerHTML = suggestionHTML;
                            document.getElementById('suggestions').style.display = 'block';
                        } else {
                            console.error('No suggestions found');
                        }
                    })
                    .catch(error => console.error('Error fetching suggestions:', error));
                });
                elements.errorDiv.style.display = 'none';
            } else if (result.error) {
                elements.errorDiv.innerHTML = `<p>Hata: ${result.error}</p>`;
                elements.errorDiv.style.display = 'block';
                elements.resultDiv.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error predicting price:', error);
            elements.errorDiv.innerHTML = `<p>Hata: Bir hata oluştu. Lütfen tekrar deneyin.</p>`;
            elements.errorDiv.style.display = 'block';
            elements.resultDiv.style.display = 'none';
        });
    });
    
    // istatistik sayfası için modal fonksiyonları
    var modal = document.getElementById('modal');
    var modalImg = document.getElementById('modal-img');
    var closeBtn = document.getElementById('close');

    if (modal && modalImg && closeBtn) {
        var statImages = document.querySelectorAll('.stat-image');

        statImages.forEach(function (image) {
            image.addEventListener('click', function () {
                modal.style.display = 'block';
                modalImg.src = this.src;
            });
        });

        closeBtn.addEventListener('click', function () {
            modal.style.display = 'none';
        });

        modal.addEventListener('click', function () {
            modal.style.display = 'none';
        });
    }
});