# PhD Progress Tracker - Web Frontend

A modern web interface for tracking PhD progress, built with Next.js and Tailwind CSS.

## Prerequisites

- Node.js 18+
- npm or yarn
- Backend running on http://localhost:8000

## Installation

```bash
cd web
npm install
```

## Environment Variables

Create `.env.local` in the web directory:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development

```bash
npm run dev
# Open http://localhost:3000
```

## Testing

```bash
npm run test      # Watch mode
npm run test:run  # Single run
```

## Build

```bash
npm run build
npm start
```

## Project Structure

```
web/
├── app/                 # Next.js App Router pages
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Dashboard page
│   ├── tasks/          # Tasks page
│   └── milestones/     # Milestones page
├── components/         # React components
│   ├── TaskForm.tsx
│   ├── MilestoneForm.tsx
│   ├── TaskList.tsx
│   ├── MilestoneList.tsx
│   ├── DashboardStats.tsx
│   ├── StatusBadge.tsx
│   ├── Modal.tsx
│   ├── Button.tsx
│   ├── Card.tsx
│   └── Header.tsx
├── lib/                # Utilities and API client
│   ├── api.ts          # API client functions
│   ├── types.ts        # TypeScript type definitions
│   └── utils.ts        # Utility functions
├── tests/              # Component tests
│   ├── setup.ts
│   ├── TaskForm.test.tsx
│   ├── MilestoneForm.test.tsx
│   ├── DashboardStats.test.tsx
│   ├── StatusBadge.test.tsx
│   ├── Modal.test.tsx
│   └── TEST_PLAN.md
├── public/             # Static assets
├── styles/             # Global styles
├── vitest.config.ts    # Vitest configuration
└── package.json
```

## Tech Stack

- Next.js 14.x
- React 18.x
- Tailwind CSS 3.4
- TypeScript 5.x
- Vitest + React Testing Library

## API Endpoints

The frontend communicates with the following backend endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dashboard` | GET | Fetch dashboard statistics |
| `/tasks` | GET | List all tasks |
| `/tasks` | POST | Create a new task |
| `/tasks/{id}` | GET | Get a task by ID |
| `/tasks/{id}` | PATCH | Update a task |
| `/tasks/{id}` | DELETE | Delete a task |
| `/milestones` | GET | List all milestones |
| `/milestones` | POST | Create a new milestone |
| `/milestones/{id}` | GET | Get a milestone by ID |
| `/milestones/{id}` | PATCH | Update a milestone |
| `/milestones/{id}` | DELETE | Delete a milestone |

## License

MIT © 2026 William Ceccon
