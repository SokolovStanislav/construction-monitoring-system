# Система мониторинга строительного процесса

Система автоматизированного анализа строительной готовности объекта и контроля расхода материалов на основе обработки аэрофотоснимков с использованием ансамбля нейросетевых моделей компьютерного зрения.

> **Статус проекта:** в разработке (магистерская диссертация)

## Назначение

Система предназначена для:
- Автоматизированного определения готовности строительных объектов по аэрофотоснимкам
- Контроля расхода строительных материалов
- Выявления отклонений от проектного графика
- Формирования аналитических отчётов на естественном языке

## Архитектура

В основе системы лежит **ансамбль из четырёх специализированных нейросетевых моделей**, каждая из которых решает свою подзадачу:

| Модель | Назначение | Архитектура |
|--------|-----------|-------------|
| Детектор объектов | Поиск техники, материалов, персонала | YOLOv8 |
| Сегментатор | Определение границ конструкций | SegFormer |
| Классификатор | Определение стадии строительства | EfficientNet-B4 |
| Детектор изменений | Анализ прогресса во времени | Siamese U-Net |

Результаты работы моделей объединяются модулем агрегации (Ensemble Router) по стратегии позднего слияния (late fusion).

## Технологический стек

**Backend:**
- Python 3.11, FastAPI
- PostgreSQL + PostGIS, Redis, MinIO
- Celery (очередь задач)

**Machine Learning:**
- PyTorch 2.0+
- Ultralytics (YOLOv8), HuggingFace Transformers (SegFormer)
- OpenCV, GDAL, Albumentations

**Frontend:**
- React + TypeScript
- Mapbox GL JS (карты), Recharts (графики)

**Интеграция:**
- LLM (GPT-4o / YandexGPT) через механизм Function Calling

## Структура проекта

```
construction-monitoring-system/
├── backend/            # Серверная часть (FastAPI)
│   ├── api/            # HTTP-эндпоинты
│   ├── services/       # Бизнес-логика, агрегация, LLM
│   └── database/       # SQLAlchemy-модели, миграции
├── ml/                 # Модуль машинного обучения
│   ├── models/         # Определения 4 моделей ансамбля
│   ├── training/       # Скрипты обучения
│   ├── inference/      # Скрипты инференса
│   ├── preprocessing/  # Аугментация, геообработка
│   └── configs/        # YAML-конфиги обучения
├── frontend/           # Клиентский интерфейс (React)
├── data/               # Данные (управляются через DVC)
├── docs/               # Документация, UML-диаграммы
├── tests/              # Модульные и интеграционные тесты
├── docker-compose.yml  # Развёртывание всех сервисов
└── README.md
```

## Быстрый старт

### Предварительные требования
- Docker и Docker Compose
- (Опционально) NVIDIA GPU с драйверами для ML-сервиса

### Запуск

```bash
# Клонирование репозитория
git clone https://github.com/SokolovStanislav/construction-monitoring-system.git
cd construction-monitoring-system

# Запуск всех сервисов
docker-compose up --build
```

После запуска сервисы будут доступны по адресам:
- **API:** http://localhost:8000
- **Документация API (Swagger):** http://localhost:8000/docs
- **Frontend:** http://localhost:3000

### Проверка работоспособности

```bash
curl http://localhost:8000/health
# Ожидаемый ответ: {"status": "ok"}
```

## Примеры API-запросов

### Создание проекта
```bash
curl -X POST "http://localhost:8000/api/v1/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ЖК Солнечный",
    "start_date": "2025-03-01"
  }'
```

### Загрузка аэрофотоснимков
```bash
curl -X POST "http://localhost:8000/api/v1/images/upload?project_id=..." \
  -F "files=@drone_image_001.tif" \
  -F "files=@drone_image_002.tif"
```

### Получение отчёта о прогрессе
```bash
curl "http://localhost:8000/api/v1/reports/{project_id}/progress"
```

### Чат с LLM
```bash
curl -X POST "http://localhost:8000/api/v1/reports/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "...",
    "message": "Какой процент готовности и есть ли отставание?"
  }'
```

## Жизненный цикл разработки

Проект использует **гибридную модель ЖЦ**:
- **Каскадная модель** — для разработки программных компонентов (backend, frontend, инфраструктура)
- **CRISP-DM** — для разработки и обучения ML-моделей (итеративный подход с экспериментами)

Ветвление в Git:
- `main` — стабильная версия
- `develop` — основная ветка разработки
- `feature/*` — новые функции
- `experiment/*` — ML-эксперименты

## Локальная разработка

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn api.main:app --reload

# Frontend
cd frontend
npm install
npm start
```

## Лицензия

Учебный проект. Все материалы предназначены для использования в рамках магистерской диссертации.

## Автор

**Соколов С.А.**  
Магистрант 1 курса  
Направление: 09.04.01 "Информатика и вычислительная техника"  
Программа: "Искусственный интеллект"  
ВГТУ, 2026
