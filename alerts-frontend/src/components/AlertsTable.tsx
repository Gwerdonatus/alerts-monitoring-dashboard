import React from "react";
import { Alert } from "../types";
import { AlertRow } from "./AlertRow";

interface AlertsTableProps {
  alerts: Alert[];
  loading: boolean;
  dismissingId: string | null;
  onDismiss: (alertId: string) => void;
}

export const AlertsTable: React.FC<AlertsTableProps> = ({
  alerts,
  loading,
  dismissingId,
  onDismiss,
}) => {
  return (
    <div className="overflow-hidden rounded-lg border border-slate-800 bg-slate-950/40">
      <div className="overflow-x-auto">
        <table
          className="min-w-full border-separate border-spacing-0 text-left text-sm"
          aria-label="Alerts table"
        >
          <thead>
            <tr className="bg-slate-900/90 text-xs font-semibold uppercase tracking-wide text-slate-400">
              <th scope="col" className="px-4 py-3">
                Employee
              </th>
              <th scope="col" className="px-4 py-3">
                Severity
              </th>
              <th scope="col" className="px-4 py-3">
                Category
              </th>
              <th scope="col" className="px-4 py-3">
                Status
              </th>
              <th scope="col" className="px-4 py-3">
                Created At
              </th>
              <th scope="col" className="px-4 py-3 text-right">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr>
                <td
                  colSpan={6}
                  className="px-4 py-8 text-center text-sm text-slate-400"
                >
                  <span className="inline-flex items-center gap-2">
                    <span
                      className="h-4 w-4 animate-spin rounded-full border-2 border-emerald-400 border-t-transparent"
                      aria-hidden="true"
                    />
                    Loading alerts…
                  </span>
                </td>
              </tr>
            )}

            {!loading && alerts.length === 0 && (
              <tr>
                <td
                  colSpan={6}
                  className="px-4 py-8 text-center text-sm text-slate-400"
                >
                  No alerts found for the current filters.
                </td>
              </tr>
            )}

            {!loading &&
              alerts.map((alert, idx) => (
                <AlertRow
                  key={alert.id}
                  alert={alert}
                  isStriped={idx % 2 === 1}
                  onDismiss={
                    alert.status === "open"
                      ? () => onDismiss(alert.id)
                      : undefined
                  }
                  isDismissing={dismissingId === alert.id}
                />
              ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};


