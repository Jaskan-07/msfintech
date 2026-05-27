Project Structure
ui/
│
├── public/
├── src/
│   ├── app/
│   ├── features/
│   ├── shared/
│   ├── config/
│   ├── assets/
│   ├── styles/
│   ├── tests/
│   └── main.tsx
│
├── .env
├── package.json
├── Dockerfile
└── README.md
Folder Details
1. public/

Contains static public assets.

public/
├── favicon.ico
├── index.html
└── assets/
Purpose
Static files
Public images
Browser metadata
2. src/

Main application source code.

3. src/app/

Contains application bootstrap and core setup.

app/
├── store/
├── router/
├── providers/
├── layouts/
└── App.tsx
app/store/

Global state configuration.

store/
├── index.ts
├── rootReducer.ts
└── middleware.ts
Responsibilities
Redux store setup
Global reducers
Middleware registration
Application-wide state
app/router/

Centralized routing configuration.

router/
├── AppRouter.tsx
├── PrivateRoute.tsx
└── routes.ts
Responsibilities
Route definitions
Lazy loading
Protected routes
Navigation guards
app/providers/

Application providers and wrappers.

providers/
├── ThemeProvider.tsx
├── AuthProvider.tsx
└── QueryProvider.tsx
Responsibilities
Authentication context
Theme configuration
React Query provider
Global wrappers
app/layouts/

Reusable page layouts.

layouts/
├── MainLayout.tsx
├── DashboardLayout.tsx
└── AuthLayout.tsx
Responsibilities
Header/Footer structure
Navigation
Page templates
4. src/features/

Feature-based modules.

features/
├── auth/
├── users/
├── dashboard/
├── reports/
└── settings/

Each feature owns its:

API layer
Components
Hooks
Store
Types
Utilities
Pages
Example Feature Structure
features/auth/
├── api/
├── components/
├── hooks/
├── pages/
├── store/
├── types/
├── utils/
└── index.ts
Why Feature-Based Architecture?
Benefits
Better scalability
Independent ownership
Easier refactoring
Reduced coupling
Easier onboarding
5. src/shared/

Reusable common modules shared across features.

shared/
├── components/
├── hooks/
├── services/
├── utils/
├── constants/
├── validators/
└── types/
shared/components/

Reusable UI components.

components/
├── Button/
├── Modal/
├── Table/
└── Loader/
Rules
Generic only
No business logic
Highly reusable
shared/services/

Shared services and API utilities.

services/
├── apiClient.ts
├── interceptors.ts
└── auth.service.ts
Responsibilities
Axios instance
Token management
Error handling
Request interceptors
shared/hooks/

Reusable hooks.

Example:

hooks/
├── useDebounce.ts
├── usePagination.ts
└── useLocalStorage.ts
6. src/config/

Application configuration.

config/
├── env.ts
├── constants.ts
└── featureFlags.ts
Responsibilities
Environment variables
App constants
Feature toggles
7. src/assets/

Application assets.

assets/
├── images/
├── icons/
└── fonts/
8. src/styles/

Global styles and themes.

styles/
├── globals.scss
├── variables.scss
└── themes/
9. src/tests/

Testing utilities and test setup.

tests/
├── mocks/
├── integration/
└── setupTests.ts
Environment Configuration

Use environment-specific files:

.env.development
.env.qa
.env.production
Example
VITE_API_BASE_URL=https://api.company.com
Recommended Technology Stack
Area	Recommended
Framework	React + TypeScript
Build Tool	Vite
State Management	Redux Toolkit / Zustand
API Layer	Axios + React Query
Styling	Tailwind / SCSS
Forms	React Hook Form
Validation	Zod / Yup
Testing	Vitest / RTL
E2E Testing	Cypress / Playwright
