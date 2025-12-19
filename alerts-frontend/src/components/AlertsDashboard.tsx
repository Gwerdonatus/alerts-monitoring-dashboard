import React, { useCallback, useEffect, useMemo, useState } from "react";
import { Alert, FilterState } from "../types";
import { Filters } from "./Filters";
import { AlertsTable } from "./AlertsTable";
import { fetchAlerts, dismissAlert } from "../services/api";

const INITIAL_MANAGER_ID = "MGR001";

export const AlertsDashboard: React.FC = () => {
  const [managerId, setManagerId] = useState<string>(INITIAL_MANAGER_ID);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [pagination, setPagination] = useState({
    count: 0,
    next: null as string | null,
    previous: null as string | null,
  });
  const [filters, setFilters] = useState<FilterState>({
    severity: "all",
    status: "all",
    scope: "direct",
    search: "",
  });
  const [pageUrl, setPageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState(0);
  const [dismissingId, setDismissingId] = useState<string | null>(null);

  const hasManagerId = managerId.trim().length > 0;

  const queryDescription = useMemo(() => {
    const parts: string[] = [];

    parts.push(filters.scope === "direct" ? "Direct reports" : "Full subtree");

    if (filters.severity !== "all") {
      parts.push(`Severity: ${filters.severity}`);
    }
    if (filters.status !== "all") {
      parts.push(`Status: ${filters.status}`);
    }
    if (filters.search.trim()) {
      parts.push(`Search: “${filters.search.trim()}”`);
    }

    return parts.join(" · ");
  }, [filters]);

  useEffect(() => {
    if (!hasManagerId) {
      setAlerts([]);
      setPagination({ count: 0, next: null, previous: null });
      return;
    }

    const controller = new AbortController();

    const loadAlerts = async () => {
      setLoading(true);
      setError(null);

      try {
        const data = await fetchAlerts(
          {
            managerId,
            scope: filters.scope,
            severity: filters.severity !== "all" ? filters.severity : undefined,
            status: filters.status !== "all" ? filters.status : undefined,
            search: filters.search.trim() || undefined,
            pageUrl: pageUrl || undefined,
          },
          controller.signal
        );

        setAlerts(data.results);
        setPagination({
          count: data.count,
          next: data.next,
          previous: data.previous,
        });
      } catch (err) {
        if (err instanceof DOMException && err.name === "AbortError") {
          return;
        }
        console.error("Error fetching alerts", err);
        setError(
          err instanceof Error ? err.message : "Unexpected error fetching alerts"
        );
      } finally {
        setLoading(false);
      }
    };

    loadAlerts();

    return () => controller.abort();
  }, [managerId, filters, pageUrl, hasManagerId, refreshToken]);

  const handleDismissAlert = useCallback(async (alertId: string) => {
    try {
      setDismissingId(alertId);
      setError(null);

      await dismissAlert(alertId);

      // Re-fetch current page to keep pagination & filters consistent
      setRefreshToken((prev) => prev + 1);
    } catch (err) {
      console.error("Error dismissing alert", err);
      setError(
        err instanceof Error ? err.message : "Unexpected error dismissing alert"
      );
    } finally {
      setDismissingId(null);
    }
  }, []);

  const handleFiltersChange = (next: FilterState) => {
    setFilters(next);
    setPageUrl(null);
  };

  const handleResetFilters = () => {
    setFilters({
      severity: "all",
      status: "all",
      scope: "direct",
      search: "",
    });
    setPageUrl(null);
  };

  const handlePageChange = (url: string | null) => {
    if (!url) return;
    setPageUrl(url);
  };

  const totalPages = useMemo(() => {
    if (pagination.count === 0) return 0;
    // We rely on the backend default page size of 10. In a more
    // advanced setup we would read this from the API.
    return Math.ceil(pagination.count / 10);
  }, [pagination.count]);

  return (
    <section
      aria-label="Alerts dashboard"
      className="flex flex-col gap-4 rounded-xl border border-slate-800 bg-slate-900/60 p-4 shadow-lg shadow-slate-950/40 sm:p-6"
    >
      <div className="flex flex-col gap-3 border-b border-slate-800 pb-4 sm:flex-row sm:items-end sm:justify-between">
        <div className="flex flex-col gap-2">
          <label
            htmlFor="manager-id"
            className="text-xs font-medium uppercase tracking-wide text-slate-400"
          >
            Manager ID
          </label>
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
            <input
              id="manager-id"
              type="text"
              value={managerId}
              onChange={(e) => {
                setManagerId(e.target.value);
                setPageUrl(null);
              }}
              className="w-full rounded-md border border-slate-700 bg-slate-950/60 px-3 py-2 text-sm text-slate-100 outline-none ring-0 transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/40 sm:max-w-xs"
              placeholder="e.g. MGR001"
            />
            <p className="text-xs text-slate-500">
              Seed data uses <code className="font-mono">MGR001</code>.
            </p>
          </div>
        </div>

        <div className="flex flex-col items-start gap-2 sm:items-end">
          <Filters
            value={filters}
            onChange={handleFiltersChange}
            onReset={handleResetFilters}
          />
          <p className="max-w-md text-xs text-slate-500">{queryDescription}</p>
        </div>
      </div>

      {error && (
        <div
          role="alert"
          className="rounded-md border border-red-500/40 bg-red-950/40 px-3 py-2 text-sm text-red-200"
        >
          <p className="font-medium">Unable to load alerts.</p>
          <p className="text-xs text-red-200/80">{error}</p>
        </div>
      )}

      {!hasManagerId && !error && (
        <div className="rounded-md border border-amber-500/40 bg-amber-950/40 px-3 py-2 text-sm text-amber-100">
          Enter a manager ID to view alerts.
        </div>
      )}

      <AlertsTable
        alerts={alerts}
        loading={loading}
        dismissingId={dismissingId}
        onDismiss={handleDismissAlert}
      />

      <div className="mt-2 flex flex-col items-center justify-between gap-3 text-xs text-slate-400 sm:flex-row">
        <div className="flex items-center gap-2">
          <span className="font-medium text-slate-200">
            {pagination.count.toLocaleString()}{" "}
          </span>
          <span>total alerts</span>
        </div>

        <div className="inline-flex items-center gap-2">
          <button
            type="button"
            onClick={() => handlePageChange(pagination.previous)}
            disabled={!pagination.previous || loading}
            aria-label="Go to previous page"
            className="inline-flex items-center gap-1 rounded-md border border-slate-700/80 bg-slate-900/80 px-3 py-1.5 text-xs font-medium text-slate-100 shadow-sm transition hover:border-slate-500 hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:ring-offset-2 focus:ring-offset-slate-950 disabled:cursor-not-allowed disabled:border-slate-800 disabled:bg-slate-900 disabled:text-slate-600 disabled:opacity-50"
          >
            ‹ Previous
          </button>
          <span className="text-slate-500" aria-live="polite">
            Page{" "}
            <span className="font-semibold text-slate-200">
              {pagination.count === 0 ? 0 : pageUrl ? "…" : 1}
            </span>{" "}
            of{" "}
            <span className="font-semibold text-slate-200">
              {totalPages}
            </span>
          </span>
          <button
            type="button"
            onClick={() => handlePageChange(pagination.next)}
            disabled={!pagination.next || loading}
            aria-label="Go to next page"
            className="inline-flex items-center gap-1 rounded-md border border-slate-700/80 bg-slate-900/80 px-3 py-1.5 text-xs font-medium text-slate-100 shadow-sm transition hover:border-slate-500 hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:ring-offset-2 focus:ring-offset-slate-950 disabled:cursor-not-allowed disabled:border-slate-800 disabled:bg-slate-900 disabled:text-slate-600 disabled:opacity-50"
          >
            Next ›
          </button>
        </div>
      </div>
    </section>
  );
};


