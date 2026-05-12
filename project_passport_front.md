# FRONTEND PROJECT PASSPORT
## AI Video Generation Platform

---

## 1. ОБЩЕЕ ОПИСАНИЕ

Frontend часть платформы представляет собой модульное React-приложение на Next.js 15, обеспечивающее полный цикл управления генерацией AI-видео: от создания проекта до рендеринга и экспорта готового ролика.

**Архитектурные принципы:**
- Clean Architecture с разделением на слои (API, State, UI, Business Logic)
- Модульная структура (Feature-Sliced Design подход)
- Event-driven архитектура для realtime обновлений
- Полная типизация TypeScript
- Разделение ответственности между компонентами

**Технологический стек:**
- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript 5+
- **Styling:** TailwindCSS + shadcn/ui
- **State Management:** Zustand (UI state), TanStack Query (Server state)
- **Realtime:** WebSocket / SSE
- **Build Tool:** Vite / Turbopack

---

## 2. СТРУКТУРА ПРОЕКТА

```text
frontend/
├── app/                          # Next.js App Router
│   ├── (dashboard)/              # Группа страниц дашборда
│   │   ├── layout.tsx            # Layout дашборда (Sidebar + Topbar)
│   │   ├── page.tsx              # Главная страница
│   │   ├── projects/             # Управление проектами
│   │   ├── jobs/                 # Мониторинг задач
│   │   ├── prompts/              # Библиотека промптов
│   │   ├── settings/             # Настройки системы
│   │   └── render/               # Рендер и экспорт
│   ├── layout.tsx                # Корневой layout
│   ├── providers.tsx             # Глобальные провайдеры
│   └── api/                      # API routes (если нужны)
│
├── modules/                      # Бизнес-модули (Feature Modules)
│   ├── projects/                 # Блок F2: Projects System
│   │   ├── api/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── stores/
│   │   ├── types/
│   │   └── utils/
│   ├── pipeline/                 # Блок F3: Pipeline Control
│   ├── jobs/                     # Блок F4: Jobs + Queue
│   ├── prompts/                  # Блок F5: Prompts Management
│   ├── settings/                 # Блок F6: AI Settings
│   ├── scenes/                   # Блок F7: Scene Editor
│   ├── characters/               # Блок F8: Character System
│   ├── realtime/                 # Блок F9: Realtime Infrastructure
│   └── render/                   # Блок F10: Render Queue + Export
│
├── components/                   # Shared UI Components
│   ├── ui/                       # Базовые компоненты (shadcn)
│   ├── layout/                   # Layout компоненты
│   └── feedback/                 # Индикаторы, тосты, модалки
│
├── services/                     # Сервисный слой
│   ├── api/                      # API клиент (Axios instance)
│   └── websocket/                # WS сервис
│
├── stores/                       # Глобальные сторы (App-wide)
│   ├── app_store.ts
│   └── auth_store.ts
│
├── hooks/                        # Глобальные хуки
├── types/                        # Глобальные типы
├── utils/                        # Утилиты
├── styles/                       # Глобальные стили
└── providers/                    # Контекст провайдеры
```

---

## 3. УСТАНОВКА И ЗАПУСК

### Требования
- Node.js >= 20.x
- npm >= 10.x или pnpm >= 8.x

### Шаг 1: Установка зависимостей
```bash
cd frontend
npm install
```

### Шаг 2: Настройка переменных окружения
Создайте файл `.env.local` в корне `frontend/`:

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

### Шаг 3: Запуск в режиме разработки
```bash
npm run dev
```
Приложение доступно по адресу: [http://localhost:3000](http://localhost:3000)

### Шаг 4: Сборка для продакшена
```bash
npm run build
npm run start
```

### Шаг 5: Линтинг и проверка типов
```bash
npm run lint
npm run type-check
```

---

## 4. СТАТУС РЕАЛИЗАЦИИ МОДУЛЕЙ

| Модуль | Блок | Статус | Описание | Директория |
| :--- | :---: | :---: | :--- | :--- |
| **Core Architecture** | F1 | ✅ **READY** | Роутинг, лейауты, провайдеры, базовые стили | `app/`, `providers/` |
| **Projects System** | F2 | ✅ **READY** | CRUD проектов, фильтры, поиск, статистика | `modules/projects/` |
| **Pipeline Control** | F3 | ✅ **READY** | Визуализация этапов, контроль запуска, логи | `modules/pipeline/` |
| **Jobs & Queue** | F4 | ✅ **READY** | Таблица задач, очередь, retry/cancel, логи | `modules/jobs/` |
| **Prompts Management** | F5 | ✅ **READY** | Редактор промптов, переменные, валидация, версии | `modules/prompts/` |
| **AI Settings** | F6 | ✅ **READY** | Настройки провайдеров, API ключей, рендера | `modules/settings/` |
| **Scene Editor** | F7 | ✅ **READY** | Редактор сцен, таймлайн, слои, превью | `modules/scenes/` |
| **Character System** | F8 | ✅ **READY** | Персонажи, референсы, консистентность | `modules/characters/` |
| **Realtime System** | F9 | ✅ **READY** | WebSocket клиент, event bus, reconnect | `modules/realtime/` |
| **Render & Export** | F10 | ✅ **READY** | Очередь рендера, экспорт, скачивание | `modules/render/` |
| **Assets Library** | F11 | ✅ **READY** | Хранилище медиа, переиспользование ассетов | `modules/assets/` |
| **Channels + Templates** | F12 | ✅ **READY** | Каналы контента, шаблоны генерации | `modules/channels/` |
| **Analytics System** | F13 | ✅ **READY** | Дашборд метрик, мониторинг системы | `modules/analytics/` |

---

## 5. API REFERENCE (FRONTEND CONTRACTS)

### 5.1 Projects API
| Метод | Endpoint | Описание |
| :--- | :--- | :--- |
| `GET` | `/projects` | Список всех проектов |
| `GET` | `/projects/{id}` | Детали проекта |
| `POST` | `/projects` | Создать проект |
| `PUT` | `/projects/{id}` | Обновить проект |
| `DELETE` | `/projects/{id}` | Удалить проект |

### 5.2 Pipeline API
| Метод | Endpoint | Описание |
| :--- | :--- | :--- |
| `POST` | `/pipeline/run` | Запустить пайплайн |
| `POST` | `/pipeline/run-stage` | Запустить этап |
| `POST` | `/pipeline/pause` | Пауза пайплайна |
| `POST` | `/pipeline/resume` | Возобновить пайплайн |

### 5.3 Jobs API
| Метод | Endpoint | Описание |
| :--- | :--- | :--- |
| `GET` | `/jobs` | Список задач (с фильтрами) |
| `GET` | `/jobs/{id}` | Детали задачи + логи |
| `POST` | `/jobs/retry` | Повторить задачу |
| `POST` | `/jobs/cancel` | Отменить задачу |
| `GET` | `/queue` | Статус очереди |

### 5.4 Prompts API
| Метод | Endpoint | Описание |
| :--- | :--- | :--- |
| `GET` | `/prompts` | Список шаблонов |
| `POST` | `/prompts` | Создать шаблон |
| `PUT` | `/prompts/{id}` | Обновить шаблон |
| `POST` | `/prompts/preview` | Превью с подстановкой |
| `GET` | `/prompts/{id}/versions` | История версий |

### 5.5 Scenes API
| Метод | Endpoint | Описание |
| :--- | :--- | :--- |
| `GET` | `/scenes?project_id=...` | Список сцен проекта |
| `POST` | `/scenes` | Создать сцену |
| `PUT` | `/scenes/{id}` | Обновить сцену (prompt, motion) |
| `POST` | `/scenes/{id}/regenerate` | Перегенерировать медиа |

### 5.6 Characters API
| Метод | Endpoint | Описание |
| :--- | :--- | :--- |
| `GET` | `/characters?project_id=...` | Список персонажей |
| `POST` | `/characters` | Создать персонажа |
| `POST` | `/characters/{id}/image` | Загрузить референс |

### 5.7 Render API
| Метод | Endpoint | Описание |
| :--- | :--- | :--- |
| `POST` | `/render/start` | Начать рендер видео |
| `GET` | `/render/jobs` | Список рендер-задач |
| `POST` | `/render/export` | Экспорт в формате (mp4/mov) |
| `GET` | `/render/download/{id}` | Ссылка на скачивание |

---

## 6. REALTIME EVENTS (WEBSOCKET)

Все события приходят через единый WebSocket канал. Формат события:
```json
{
  "type": "job_progress",
  "payload": { "job_id": "...", "progress": 45, "stage": "scenes" },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Список поддерживаемых событий:

| Событие | Payload | Описание |
| :--- | :--- | :--- |
| `job_started` | `{ job_id, project_id }` | Задача запущена |
| `job_progress` | `{ job_id, progress, stage }` | Прогресс выполнения |
| `job_completed` | `{ job_id, result_url }` | Задача завершена успешно |
| `job_failed` | `{ job_id, error_message }` | Ошибка выполнения |
| `pipeline_updated` | `{ pipeline_id, status }` | Обновление пайплайна |
| `scene_generated` | `{ scene_id, image_url }` | Сцена сгенерирована |
| `log_stream` | `{ job_id, logs: [] }` | Поток логов |
| `queue_updated` | `{ queue: [] }` | Обновление очереди |
| `connection_status` | `{ status: "connected" }` | Статус соединения |

---

## 7. STATE MANAGEMENT ARCHITECTURE

### 7.1 Server State (TanStack Query)
Используется для кэширования данных с бэкенда.
- **Queries:** `useProjects`, `useJobs`, `usePrompt`
- **Mutations:** `useCreateProject`, `useUpdateJob`
- **Invalidation:** Автоматическая при мутациях

### 7.2 Client State (Zustand)
Используется только для UI состояния.
- **Stores:** `useProjectsStore` (filters, selected), `usePipelineStore` (activeStage, logsExpanded)
- **Правило:** Не хранить данные, которые есть в API ответе.

### 7.3 Realtime State
- **Event Bus:** Централизованная шина событий.
- **Hooks:** `useEventSubscription('job_progress', handler)`

---

## 8. ИНСТРУКЦИЯ ДЛЯ РАЗРАБОТЧИКА

### Как добавить новый модуль?
1. Создайте папку `modules/new-feature/` со структурой (api, components, hooks, stores, types).
2. Опишите типы в `types/new_feature_types.ts`.
3. Реализуйте API слой в `api/new_feature_api.ts` и `new_feature_queries.ts`.
4. Создайте Store в `stores/new_feature_store.ts` (только UI!).
5. Реализуйте компоненты в `components/`.
6. Добавьте страницу в `app/(dashboard)/new-feature/page.tsx`.

### Как работать с реальным временем?
Не подключайте WebSocket напрямую в компонентах! Используйте хук:
```typescript
import { useEventSubscription } from '@/modules/realtime/hooks/useEventSubscription';

useEventSubscription('job_progress', (data) => {
  // Обновляйте локальный стейт или TanStack Query cache
  queryClient.setQueryData(['jobs', data.job_id], (old) => ({ ...old, progress: data.progress }));
});
```

### Как добавить новую тему/стиль?
Все стили построены на TailwindCSS.
- Используйте утилитарные классы.
- Для сложных компонентов используйте `cn()` утилиту.
- Темизация через CSS переменные в `globals.css`.

---

## 9. ТРАБЛШУТИНГ

### Ошибка: "WebSocket connection failed"
- Проверьте, запущен ли backend сервер.
- Убедитесь, что `NEXT_PUBLIC_WS_URL` в `.env.local` верен.
- Проверьте консоль браузера на наличие CORS ошибок.

### Ошибка: "Query data is undefined"
- Убедитесь, что запрос выполнен (`isLoading`, `isError`).
- Проверьте, что `queryKey` совпадает в месте вызова и инвалидации.

### Ошибка: "Module not found"
- Проверьте пути импорта (используйте `@/` алиас).
- Перезапустите dev сервер после добавления новых файлов.

### Сброс состояния приложения
- Очистите `localStorage` (ключи `ai-video-platform-*`).
- Перезагрузите страницу с очисткой кэша (Ctrl+Shift+R).

---

## 10. ПЛАНЫ РАЗВИТИЯ (ROADMAP)

Все основные модули (F1-F13) реализованы. Следующие шаги:

- [ ] **Интеграционное тестирование** — E2E тесты для критических путей (Cypress/Playwright).
- [ ] **Unit тестирование** — Покрытие хуков и утилит тестами (Jest/Vitest).
- [ ] **Оптимизация производительности** — Code splitting, lazy loading тяжелых компонентов.
- [ ] **PWA** — Добавление Service Worker для офлайн режима и кэширования ассетов.
- [ ] **Мультиязычность (i18n)** — Поддержка EN/RU интерфейса.
- [ ] **Доступность (a11y)** — Улучшение поддержки скринридеров и навигации с клавиатуры.

---

## 11. КОНТАКТЫ И ПОДДЕРЖКА

В случае возникновения проблем или вопросов по архитектуре обращайтесь к документации блоков (Blueprints F1-F10) или проверяйте типы в `types/` директории.

**Версия документа:** 1.0.0
**Дата обновления:** 2024-05-20
**Статус:** Production Ready
