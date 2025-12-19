import { useEffect, useState } from "react";
import { FilterState } from "../types";

type FiltersProps = {
  value: FilterState;
  onChange: (value: FilterState) => void;
  onReset: () => void;
};

export const Filters: React.FC<FiltersProps> = ({
  value,
  onChange,
  onReset,
}) => {
  const [searchDraft, setSearchDraft] = useState(value.search);

  // Keep searchDraft in sync with value.search
  useEffect(() => {
    setSearchDraft(value.search);
  }, [value.search]);

  // Debounce search input changes
  useEffect(() => {
    const handle = setTimeout(() => {
      if (searchDraft !== value.search) {
        onChange({ ...value, search: searchDraft });
      }
    }, 300);
    return () => clearTimeout(handle);
  }, [searchDraft, value, onChange]);

  const handleSelectChange =
    (field: "severity" | "status" | "scope") =>
    (event: React.ChangeEvent<HTMLSelectElement>) => {
      const next = event.target.value as FilterState[typeof field];
      onChange({ ...value, [field]: next });
    };

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchDraft(event.target.value);
  };

  return (
    <form
      className="flex flex-wrap items-center gap-2"
      onSubmit={(e) => e.preventDefault()}
      aria-label="Alert filters"
    >
      <label className="flex items-center gap-1.5 text-xs text-slate-300">
        <span className="whitespace-nowrap">Scope</span>
        <select
          value={value.scope}
          onChange={handleSelectChange("scope")}
          aria-label="Filter by scope"
          className="rounded-md border border-slate-700 bg-slate-950/80 px-2 py-1 text-xs text-slate-100 outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/40"
        >
          <option value="direct">Direct reports</option>
          <option value="subtree">Subtree</option>
        </select>
      </label>

      <label className="flex items-center gap-1.5 text-xs text-slate-300">
        <span className="whitespace-nowrap">Severity</span>
        <select
          value={value.severity}
          onChange={handleSelectChange("severity")}
          aria-label="Filter by severity"
          className="rounded-md border border-slate-700 bg-slate-950/80 px-2 py-1 text-xs text-slate-100 outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/40"
        >
          <option value="all">All</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </label>

      <label className="flex items-center gap-1.5 text-xs text-slate-300">
        <span className="whitespace-nowrap">Status</span>
        <select
          value={value.status}
          onChange={handleSelectChange("status")}
          aria-label="Filter by status"
          className="rounded-md border border-slate-700 bg-slate-950/80 px-2 py-1 text-xs text-slate-100 outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/40"
        >
          <option value="all">All</option>
          <option value="open">Open</option>
          <option value="dismissed">Dismissed</option>
        </select>
      </label>

      <label className="relative flex-1 min-w-[160px] text-xs text-slate-300">
        <span className="sr-only">Search by employee name</span>
        <input
          type="search"
          value={searchDraft}
          onChange={handleSearchChange}
          placeholder="Search by employee name…"
          className="w-full rounded-md border border-slate-700 bg-slate-950/80 px-3 py-1.5 text-xs text-slate-100 outline-none placeholder:text-slate-500 focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/40"
        />
      </label>

      <button
        type="button"
        onClick={onReset}
        aria-label="Reset all filters"
        className="inline-flex items-center rounded-md border border-slate-700 bg-slate-900/80 px-2.5 py-1 text-xs font-medium text-slate-200 shadow-sm transition hover:border-slate-500 hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:ring-offset-2 focus:ring-offset-slate-950"
      >
        Reset
      </button>
    </form>
  );
};
