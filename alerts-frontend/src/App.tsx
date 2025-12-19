import React from "react";
import { AlertsDashboard } from "./components/AlertsDashboard";

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-4 pb-10 pt-8 sm:px-6 lg:px-8">
        <header className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight text-slate-50 sm:text-3xl">
              Alerts Dashboard
            </h1>
            <p className="mt-1 text-sm text-slate-400">
              Monitor employee alerts with filtering, search, and pagination.
            </p>
          </div>
          <div className="mt-2 flex items-center gap-2 text-xs text-slate-500 sm:mt-0">
            <span className="inline-flex h-2 w-2 rounded-full bg-emerald-400" />
            <span>Connected to Django Alerts API</span>
          </div>
        </header>

        <main>
          <AlertsDashboard />
        </main>
      </div>
    </div>
  );
};

export default App;
