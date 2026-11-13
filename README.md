# ⚡ DisputeForge — AI Chargeback & Dispute Defense Pack Generator

**DisputeForge** — готовый к коммерческому запуску B2B Micro-SaaS для защиты интернет-магазинов (Shopify, WooCommerce, Stripe, PayPal) от необоснованных чарджбэков («friendly fraud»).

---

## 🚀 Как запустить локально за 10 секунд:

1. Откройте терминал в папке проекта:
   ```powershell
   cd disputeforge
   python app.py
   ```
2. Откройте браузер по адресу:
   👉 **http://localhost:8088**

3. Нажмите кнопку **«✨ Load Sample Case»**, затем **«⚡ Generate Defense Pack»**, чтобы мгновенно протестировать генерацию официального пакета доказательств для банка.

---

## 🌐 Как развернуть онлайн бесплатно (1-Click Cloud Deploy):

### Вариант A: Render.com (Бесплатно за 3 минуты)
1. Создайте бесплатный аккаунт на [render.com](https://render.com).
2. Нажмите **New +** -> **Web Service**.
3. Подключите ваш репозиторий GitHub с папкой `disputeforge`.
4. В поле **Start Command** укажите:
   ```bash
   python app.py
   ```
5. Получите публичный URL вида `https://disputeforge.onrender.com`.

### Вариант B: Railway.app
1. Зайдите на [railway.app](https://railway.app).
2. Выберите **Deploy from GitHub repo**.
3. Railway автоматически определит Python и запустит сервис.

---

## 🛠 Архитектура стека:
- **Backend:** Python 3 (Native HTTP Server + REST API, нулевые внешние зависимости).
- **База данных:** SQLite (`disputeforge.db`) с сохранением истории споров и метрик возвращенных денег.
- **Frontend UI:** Responsive B2B Dark Theme на Tailwind CSS, Lucide Icons, Print Dossier Engine (экспорт в PDF).
- **Dispute Engine:** Реализация стандарта **Visa Compelling Evidence 3.0 (CE 3.0)** и классификаторов кодов Mastercard (4837, 4855, 4853).
